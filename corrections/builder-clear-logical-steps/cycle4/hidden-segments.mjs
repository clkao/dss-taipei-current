import fs from 'node:fs';
import path from 'node:path';
import {spawn} from 'node:child_process';
import {once} from 'node:events';
import {createHash} from 'node:crypto';
const out=path.resolve(process.argv[2]||'projects/yangliu-vehicle/prototypes/v1');
const telemetry={started:new Date().toISOString(),nodePid:process.pid,phase:'start',events:[],chromeExit:null};
const telemetryPath=path.join(out,'r2-telemetry.json');
function note(phase,detail={}){telemetry.phase=phase;telemetry.events.push({time:Date.now(),phase,...detail});fs.writeFileSync(telemetryPath,JSON.stringify(telemetry,null,2));}
note('before-chrome-spawn');
const sourceDir=path.dirname(new URL(import.meta.url).pathname);
const root=process.cwd();
const viewer=path.resolve('builds/clear-logical/simplification-package-retry1/viewer.html');
const numbers=path.join(sourceDir,'numbers-only.html');
const key=createHash('sha256').update(out).digest('hex').slice(0,8);
const port=19000+parseInt(key,16)%1000;
const chrome=spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',[
 '--headless=new','--no-first-run','--no-default-browser-check','--disable-background-networking',
 '--remote-debugging-port='+port,'--user-data-dir='+path.resolve('tmp/yangliu-preview-chrome-'+key),
 'file://'+viewer],{stdio:['ignore','ignore','pipe']});
telemetry.chromePid=chrome.pid;note('chrome-spawned',{pid:chrome.pid});
chrome.on('exit',(code,signal)=>{telemetry.chromeExit={code,signal};note('chrome-exit',{code,signal});});
let chromeLog='';chrome.stderr.on('data',b=>{chromeLog=(chromeLog+b.toString()).slice(-2500)});
let ws;const errors=[];
try{
 note('before-target-discovery');
 let tabs;for(let i=0;i<200;i++){ 
  try{tabs=await(await fetch(`http://127.0.0.1:${port}/json`)).json();if(tabs.some(t=>t.url==='file://'+viewer))break}catch{}
  await new Promise(r=>setTimeout(r,100));
  if(chrome.exitCode!==null)throw Error('Renderer browser exited: '+chromeLog);
 }
 if(!tabs?.some(t=>t.url==='file://'+viewer))throw Error('Renderer browser unavailable: '+chromeLog);
 note('target-found');
 ws=new WebSocket(tabs.find(t=>t.url==='file://'+viewer).webSocketDebuggerUrl);await Promise.race([once(ws,'open'),new Promise((_,reject)=>setTimeout(()=>reject(Error('WebSocket open timeout')),5000))]);note('websocket-open');
 let seq=0;const pending=new Map();
 ws.addEventListener('message',({data})=>{const r=JSON.parse(data);
  if(r.method==='Runtime.exceptionThrown'){errors.push(r.params);note('runtime-exception',{details:r.params});}
  if(['Runtime.consoleAPICalled','Page.loadEventFired','Page.frameNavigated'].includes(r.method))note('browser-event',{method:r.method,details:r.params});
  const p=pending.get(r.id);if(p){pending.delete(r.id);clearTimeout(p.timer);note('cdp-result',{method:p.method,elapsed:Date.now()-p.started,error:r.error||null});r.error?p.reject(Error(JSON.stringify(r.error))):p.resolve(r.result)}
 });
 const call=(method,params={})=>new Promise((resolve,reject)=>{const id=++seq;note('before-cdp-wait',{method,id});const timer=setTimeout(()=>{pending.delete(id);note('cdp-timeout',{method,id});reject(Error(method+' timeout'));},30000);pending.set(id,{resolve,reject,timer,method,started:Date.now()});ws.send(JSON.stringify({id,method,params}))});
 await call('Runtime.enable');
 await call('Page.enable');
 const evaluate=async expression=>{const r=await call('Runtime.evaluate',{expression,returnByValue:true});if(r.exceptionDetails)throw Error(JSON.stringify(r.exceptionDetails));return r.result.value};
 async function ready(expression){const start=Date.now();while(Date.now()-start<15000){if(await evaluate(expression))return;if(errors.length)throw Error(JSON.stringify(errors));await new Promise(r=>setTimeout(r,100));}throw Error('15s readiness timeout');}
 await call('Emulation.setDeviceMetricsOverride',{width:1400,height:1000,deviceScaleFactor:1,mobile:false});
 await call('Page.addScriptToEvaluateOnNewDocument',{source:'window.capturePreviewInternals=x=>{window.__i2Observation=x};'});
 await call('Page.navigate',{url:'file://'+viewer});await ready('Boolean(window.previewReady&&window.__i2Observation)');
 const jobs=JSON.parse(fs.readFileSync(process.argv[3]||path.join(sourceDir,'jobs.json')));const locations={};
 for(const job of jobs){
  const result=await evaluate(`(()=>{const j=${JSON.stringify(job)},h=window.__i2Observation,{camera,renderer,scene,assembly,THREE,controls}=h;
   const model=window.PROTOTYPE.model,records=JSON.stringify(model.pieces);
   window.renderView({...j,decorations:true,width:1400,height:j.height||1000});
   const offset=id=>{const v=j.offsets?.find(o=>o.ids.includes(id))?.ldraw||[0,0,0];return new THREE.Vector3(v[0]*.05,-v[1]*.05,-v[2]*.05)}; const box=new THREE.Box3();for(const id of j.focus){const p=model.pieces.find(p=>p.id===id);box.union(assembly.pieceBounds(p).clone());}
   for(const t of j.targets||[]){const p=model.pieces.find(p=>p.id===t.id);box.expandByPoint(new THREE.Vector3(...(t.local||[0,0,0])).applyMatrix4(assembly.matrix(p)).add(offset(t.id)));} const center=box.getCenter(new THREE.Vector3()),size=box.getSize(new THREE.Vector3());
   const aspect=1400/(j.height||1000);const dirs={top:[.02,1,.02],front:[1,.68,1.15],'front-other':[1,.68,-1.15],underside:[1,-1.2,1.15],'rear-other':[-1,.6,1.1]};
   camera.position.copy(center).add(new THREE.Vector3(...(j.direction||dirs[j.view])).normalize().multiplyScalar(150));camera.lookAt(center);camera.updateMatrixWorld(true);controls.target.copy(center);
   const corners=[];for(const x of [box.min.x,box.max.x])for(const y of [box.min.y,box.max.y])for(const z of [box.min.z,box.max.z])corners.push(new THREE.Vector3(x,y,z).applyMatrix4(camera.matrixWorldInverse));
   const b=new THREE.Box3().setFromPoints(corners),height=Math.max(j.minHeight||4,b.max.y-b.min.y,(b.max.x-b.min.x)/aspect)*(j.margin||1.65),width=height*aspect;
   const cx=(b.min.x+b.max.x)/2,cy=(b.min.y+b.max.y)/2;Object.assign(camera,{left:cx-width/2,right:cx+width/2,top:cy+height/2,bottom:cy-height/2,zoom:1});camera.updateProjectionMatrix();camera.updateMatrixWorld(true);
   if(j.cord){const rope=scene.children.find(o=>o.geometry?.type==='TubeGeometry'&&!o.userData.suspensionBand);if(!rope)throw Error('Cord missing');rope.visible=true;rope.material=rope.material.clone();rope.material.color.set('#bd1263');}
   const targets=j.targets.map(t=>{const p=model.pieces.find(p=>p.id===t.id);const world=new THREE.Vector3(...(t.local||[0,0,0])).applyMatrix4(assembly.matrix(p)).add(offset(t.id)),q=world.clone().project(camera);return {...t,x:(q.x+1)/2,y:(1-q.y)/2,world:world.toArray()};});
   const polygons=(j.polygons||[]).map(poly=>({...poly,points:poly.local.map(v=>{const p=model.pieces.find(p=>p.id===poly.id);const q=new THREE.Vector3(...v).applyMatrix4(assembly.matrix(p)).project(camera);return {x:(q.x+1)/2,y:(1-q.y)/2};})}));
   const regions=(j.regions||[]).map(id=>{const p=model.pieces.find(p=>p.id===id),b=assembly.pieceBounds(p);const pts=[];for(const x of [b.min.x,b.max.x])for(const y of [b.min.y,b.max.y])for(const z of [b.min.z,b.max.z]){const q=new THREE.Vector3(x,y,z).project(camera);pts.push({x:(q.x+1)/2,y:(1-q.y)/2});}return {id,x0:Math.min(...pts.map(p=>p.x)),x1:Math.max(...pts.map(p=>p.x)),y0:Math.min(...pts.map(p=>p.y)),y1:Math.max(...pts.map(p=>p.y))};});renderer.render(scene,camera);if(records!==JSON.stringify(model.pieces))throw Error('Source changed');
   scene.updateMatrixWorld(true);
   const meshes=[];scene.traverse(o=>{if(!o.isMesh)return;for(let p=o;p;p=p.parent)if(!p.visible)return;meshes.push(o)});
   const ray=new THREE.Raycaster(),segments=[];
   const pairs=j.axisPairs;
   for(const [ai,bi] of pairs){
    const a=new THREE.Vector3(...targets[ai].world),b=new THREE.Vector3(...targets[bi].world);
    const length=Math.hypot((targets[bi].x-targets[ai].x)*1400,(targets[bi].y-targets[ai].y)*1000),N=Math.ceil(length*2);
    const hidden=t=>{const p=a.clone().lerp(b,t),q=p.clone().project(camera);ray.setFromCamera(new THREE.Vector2(q.x,q.y),camera);const depth=p.clone().sub(ray.ray.origin).dot(ray.ray.direction);const hit=ray.intersectObjects(meshes,false)[0];return !!hit&&hit.distance<depth-.00001;};
    const runs=[];let start=0,last=hidden(0);
    for(let n=1;n<=N;n++){const t=n/N,v=hidden(t);if(v!==last){let lo=(n-1)/N,hi=t;for(let k=0;k<10;k++){const mid=(lo+hi)/2;if(hidden(mid)===last)lo=mid;else hi=mid}const edge=(lo+hi)/2;runs.push({from:start,to:edge,hidden:last});start=edge;last=v}}
    runs.push({from:start,to:1,hidden:last});segments.push({from_target:ai,to_target:bi,sample_spacing_pixels:length/N,transition_precision_pixels:length/N/1024,runs});
   }
   return {targets,segments,mesh_count:meshes.length,mesh_types:meshes.slice(0,4).map(o=>({name:o.name,userData:o.userData,type:o.geometry.type})),source_unchanged:records===JSON.stringify(model.pieces)};})()`);

  locations[job.name]=result;note('receiver-pair-captured',{name:job.name});
 }
 if(errors.length)throw Error(JSON.stringify(errors));
 fs.writeFileSync(path.join(out,'receiver-locations.json'),JSON.stringify(locations,null,2));
 fs.writeFileSync(path.join(out,'asset-check.json'),JSON.stringify({pairs:Object.keys(locations),errors,source_unchanged:true,physical_verified:false},null,2));
 note('all-assets-captured');
}finally{
 ws?.close();
 if(chrome.exitCode===null&&chrome.signalCode===null){try{chrome.kill('SIGTERM');}catch(error){note('chrome-close-error',{error:String(error)});}}
 if(chrome.exitCode===null&&chrome.signalCode===null)await Promise.race([once(chrome,'exit'),new Promise((_,reject)=>setTimeout(()=>reject(Error('Chrome close timeout')),5000))]);
 note('finished',{chromeExit:telemetry.chromeExit,stderr:chromeLog});
}
