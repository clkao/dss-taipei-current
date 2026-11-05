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
 let tabs;for(let i=0;i<100;i++){ 
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
 const call=(method,params={})=>new Promise((resolve,reject)=>{const id=++seq;note('before-cdp-wait',{method,id});const timer=setTimeout(()=>{pending.delete(id);note('cdp-timeout',{method,id});reject(Error(method+' timeout'));},5000);pending.set(id,{resolve,reject,timer,method,started:Date.now()});ws.send(JSON.stringify({id,method,params}))});
 await call('Runtime.enable');
 await call('Page.enable');
 const evaluate=async expression=>{const r=await call('Runtime.evaluate',{expression,returnByValue:true});if(r.exceptionDetails)throw Error(JSON.stringify(r.exceptionDetails));return r.result.value};
 async function ready(expression){const start=Date.now();while(Date.now()-start<15000){if(await evaluate(expression))return;if(errors.length)throw Error(JSON.stringify(errors));await new Promise(r=>setTimeout(r,100));}throw Error('15s readiness timeout');}
 await call('Emulation.setDeviceMetricsOverride',{width:1400,height:1000,deviceScaleFactor:1,mobile:false});
 await call('Page.addScriptToEvaluateOnNewDocument',{source:'window.capturePreviewInternals=x=>{window.__i2Observation=x};'});
 await call('Page.navigate',{url:'file://'+viewer});await ready('Boolean(window.previewReady&&window.__i2Observation)');
 const jobs=JSON.parse(fs.readFileSync(path.join(sourceDir,'jobs-feet-top.json')));const locations={};
 for(const job of jobs){
  const result=await evaluate(`(()=>{const j=${JSON.stringify(job)},h=window.__i2Observation,{camera,renderer,scene,assembly,THREE,controls}=h;
   const model=window.PROTOTYPE.model,records=JSON.stringify(model.pieces);
   window.renderView({...j,decorations:true,width:1400,height:1000});
   const box=new THREE.Box3();for(const id of j.focus){const p=model.pieces.find(p=>p.id===id);box.union(assembly.pieceBounds(p));}
   const center=box.getCenter(new THREE.Vector3()),size=box.getSize(new THREE.Vector3());
   const dirs={top:[.02,1,.02],front:[1,.68,1.15],'front-other':[1,.68,-1.15],underside:[1,-1.2,1.15],'rear-other':[-1,.6,1.1]};
   camera.position.copy(center).add(new THREE.Vector3(...(j.direction||dirs[j.view])).normalize().multiplyScalar(150));camera.lookAt(center);camera.updateMatrixWorld(true);controls.target.copy(center);
   const corners=[];for(const x of [box.min.x,box.max.x])for(const y of [box.min.y,box.max.y])for(const z of [box.min.z,box.max.z])corners.push(new THREE.Vector3(x,y,z).applyMatrix4(camera.matrixWorldInverse));
   const b=new THREE.Box3().setFromPoints(corners),height=Math.max(j.minHeight||4,b.max.y-b.min.y,(b.max.x-b.min.x)/1.4)*(j.margin||1.65),width=height*1.4;
   const cx=(b.min.x+b.max.x)/2,cy=(b.min.y+b.max.y)/2;Object.assign(camera,{left:cx-width/2,right:cx+width/2,top:cy+height/2,bottom:cy-height/2,zoom:1});camera.updateProjectionMatrix();camera.updateMatrixWorld(true);
   if(j.cord){const rope=scene.children.find(o=>o.geometry?.type==='TubeGeometry'&&!o.userData.suspensionBand);if(!rope)throw Error('Cord missing');rope.visible=true;rope.material=rope.material.clone();rope.material.color.set('#bd1263');}
   const targets=j.targets.map(t=>{const p=model.pieces.find(p=>p.id===t.id);const world=new THREE.Vector3(...(t.local||[0,0,0])).applyMatrix4(assembly.matrix(p)),q=world.clone().project(camera);return {...t,x:(q.x+1)/2,y:(1-q.y)/2,world:world.toArray()};});
   const polygons=(j.polygons||[]).map(poly=>({...poly,points:poly.local.map(v=>{const p=model.pieces.find(p=>p.id===poly.id);const q=new THREE.Vector3(...v).applyMatrix4(assembly.matrix(p)).project(camera);return {x:(q.x+1)/2,y:(1-q.y)/2};})}));
   renderer.render(scene,camera);if(records!==JSON.stringify(model.pieces))throw Error('Source changed');
   return {png:renderer.domElement.toDataURL('image/png').split(',')[1],targets,polygons,selection:j.ids,newIds:j.newIds,bands:j.bands,source_unchanged:true};})()`);
  fs.writeFileSync(path.join(out,job.name+'.png'),Buffer.from(result.png,'base64'));delete result.png;
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
