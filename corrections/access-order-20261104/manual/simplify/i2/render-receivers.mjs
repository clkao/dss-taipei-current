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
const viewer=path.resolve('builds/access-corrected-hybrid-prefix/viewer.html');
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
 const reusedNumber=path.resolve('builds/simplification-i2-assets/numbers-only.png');
 if(createHash('sha256').update(fs.readFileSync(reusedNumber)).digest('hex')!=='81510ce86c45ee948366fda805ace64ea5d564b35d05ec69941f11bc192fb35f')throw Error('Reused number asset mismatch');
 const numberCheck={reused_path:reusedNumber,sha256:'81510ce86c45ee948366fda805ace64ea5d564b35d05ec69941f11bc192fb35f',no_rerender:true};
 await call('Page.addScriptToEvaluateOnNewDocument',{source:'window.capturePreviewInternals=x=>{window.__i2Observation=x};'});
 await call('Page.navigate',{url:'file://'+viewer});await ready('Boolean(window.previewReady&&window.__i2Observation)');
 const jobs=JSON.parse(fs.readFileSync(path.join(sourceDir,'receiver-jobs.json')));const locations={};
 for(const job of jobs){
  const result=await evaluate(`(()=>{const j=${JSON.stringify(job)},h=window.__i2Observation,{camera,renderer,scene,assembly,THREE}=h;
   const model=window.PROTOTYPE.model;const records=JSON.stringify(model.pieces);const opts=f=>({view:j.view,ids:f.shown_ids,newIds:f.kind==='receiver-context'?[]:f.ids,bands:!!f.bands_installed,width:1600,height:1000});
   window.renderView(opts(j.after));const locked={position:camera.position.toArray(),quaternion:camera.quaternion.toArray(),type:camera.type,left:camera.left,right:camera.right,top:camera.top,bottom:camera.bottom,zoom:camera.zoom,near:camera.near,far:camera.far,fov:camera.fov,aspect:camera.aspect,projection:camera.projectionMatrix.toArray()};
   const targets=j.targets.map(([moving,receiver],index)=>{if(!j.before.shown_ids.includes(receiver))throw Error('Missing receiver '+receiver);if(!j.after.shown_ids.includes(moving))throw Error('Missing moving piece '+moving);const source=j.step===12?receiver:moving;const piece=model.pieces.find(p=>p.id===source);const world=new THREE.Vector3(0,0,0).applyMatrix4(assembly.matrix(piece));const q=world.clone().project(camera);return {label:String(index+1),moving,receiver,source_origin:source,world:world.toArray(),x:(q.x+1)/2,y:(1-q.y)/2,meaning:'source origin locator, not connector or insertion proof'};});
   const after=renderer.domElement.toDataURL('image/png').split(',')[1];
   window.renderView(opts(j.before));camera.position.fromArray(locked.position);camera.quaternion.fromArray(locked.quaternion);if(camera.type!==locked.type||!camera.isOrthographicCamera)throw Error('Unexpected camera type');Object.assign(camera,{left:locked.left,right:locked.right,top:locked.top,bottom:locked.bottom,zoom:locked.zoom,near:locked.near,far:locked.far,aspect:locked.aspect});camera.updateProjectionMatrix();camera.updateMatrixWorld();if(JSON.stringify(camera.projectionMatrix.toArray())!==JSON.stringify(locked.projection))throw Error('Projection restoration mismatch');const beforeTargets=targets.map(t=>{const q=new THREE.Vector3(...t.world).project(camera);return {label:t.label,x:(q.x+1)/2,y:(1-q.y)/2};});if(beforeTargets.some((t,i)=>Math.abs(t.x-targets[i].x)>1e-12||Math.abs(t.y-targets[i].y)>1e-12))throw Error('Paired target projection mismatch');renderer.render(scene,camera);
   const before=renderer.domElement.toDataURL('image/png').split(',')[1];if(records!==JSON.stringify(model.pieces))throw Error('Source mutated');
   return {before,after,targets,before_targets:beforeTargets,projection_equal:true,camera:locked,selection_before:j.before.shown_ids,selection_after:j.after.shown_ids,source_unchanged:true};})()`);
  for(const state of ['before','after']){fs.writeFileSync(path.join(out,job.name+'-'+state+'.png'),Buffer.from(result[state],'base64'));delete result[state];}
  locations[job.name]=result;note('receiver-pair-captured',{name:job.name});
 }
 if(errors.length)throw Error(JSON.stringify(errors));
 fs.writeFileSync(path.join(out,'receiver-locations.json'),JSON.stringify(locations,null,2));
 fs.writeFileSync(path.join(out,'asset-check.json'),JSON.stringify({numbers:numberCheck,pairs:Object.keys(locations),errors,source_unchanged:true,physical_verified:false},null,2));
 note('all-assets-captured');
}finally{
 ws?.close();
 if(chrome.exitCode===null&&chrome.signalCode===null){try{chrome.kill('SIGTERM');}catch(error){note('chrome-close-error',{error:String(error)});}}
 if(chrome.exitCode===null&&chrome.signalCode===null)await Promise.race([once(chrome,'exit'),new Promise((_,reject)=>setTimeout(()=>reject(Error('Chrome close timeout')),5000))]);
 note('finished',{chromeExit:telemetry.chromeExit,stderr:chromeLog});
}
