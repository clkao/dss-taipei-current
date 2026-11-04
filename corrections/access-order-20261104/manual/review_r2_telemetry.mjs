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
const expectedPieces=JSON.parse(fs.readFileSync(path.join(out,'model.json'))).pieces.length;
const key=createHash('sha256').update(out).digest('hex').slice(0,8);
const port=19000+parseInt(key,16)%1000;
const chrome=spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',[
 '--headless=new','--no-first-run','--no-default-browser-check','--disable-background-networking',
 '--remote-debugging-port='+port,'--user-data-dir='+path.resolve('tmp/yangliu-preview-chrome-'+key),
 'file://'+out+'/viewer.html'],{stdio:['ignore','ignore','pipe']});
telemetry.chromePid=chrome.pid;note('chrome-spawned',{pid:chrome.pid});
chrome.on('exit',(code,signal)=>{telemetry.chromeExit={code,signal};note('chrome-exit',{code,signal});});
let chromeLog='';chrome.stderr.on('data',b=>{chromeLog=(chromeLog+b.toString()).slice(-2500)});
let ws;const errors=[];
try{
 note('before-target-discovery');
 let tabs;for(let i=0;i<100;i++){ 
  try{tabs=await(await fetch(`http://127.0.0.1:${port}/json`)).json();if(tabs.some(t=>t.url==='file://'+out+'/viewer.html'))break}catch{}
  await new Promise(r=>setTimeout(r,100));
  if(chrome.exitCode!==null)throw Error('Renderer browser exited: '+chromeLog);
 }
 if(!tabs?.some(t=>t.url==='file://'+out+'/viewer.html'))throw Error('Renderer browser unavailable: '+chromeLog);
 note('target-found');
 ws=new WebSocket(tabs.find(t=>t.url==='file://'+out+'/viewer.html').webSocketDebuggerUrl);await Promise.race([once(ws,'open'),new Promise((_,reject)=>setTimeout(()=>reject(Error('WebSocket open timeout')),5000))]);note('websocket-open');
 let seq=0;const pending=new Map();
 ws.addEventListener('message',({data})=>{const r=JSON.parse(data);
  if(r.method==='Runtime.exceptionThrown'){errors.push(r.params);note('runtime-exception',{details:r.params});}
  if(['Runtime.consoleAPICalled','Page.loadEventFired','Page.frameNavigated'].includes(r.method))note('browser-event',{method:r.method,details:r.params});
  const p=pending.get(r.id);if(p){pending.delete(r.id);clearTimeout(p.timer);note('cdp-result',{method:p.method,elapsed:Date.now()-p.started,error:r.error||null});r.error?p.reject(Error(JSON.stringify(r.error))):p.resolve(r.result)}
 });
 const call=(method,params={})=>new Promise((resolve,reject)=>{const id=++seq;note('before-cdp-wait',{method,id});const timer=setTimeout(()=>{pending.delete(id);note('cdp-timeout',{method,id});reject(Error(method+' timeout'));},5000);pending.set(id,{resolve,reject,timer,method,started:Date.now()});ws.send(JSON.stringify({id,method,params}))});
 await call('Runtime.enable');
 await call('Page.enable');
 // One-run observer injected before reload; no API is added to the shipped viewer.
 await call('Page.addScriptToEvaluateOnNewDocument',{source:`window.__dssHookInstalled=true;window.__dssCallbackInvoked=false;window.capturePreviewInternals=({scene})=>{window.__dssCallbackInvoked=true;window.__dssR2ReviewAccessories=()=>scene.children.filter(o=>o.userData?.suspensionBand).map(o=>{const ancestors=[];for(let p=o.parent;p;p=p.parent)ancestors.push({type:p.type,visible:p.visible});return {anchorIds:o.userData.anchorIds,selfVisible:o.visible,ancestors,visible:o.visible&&ancestors.every(a=>a.visible)};});};`});
 await call('Page.reload',{ignoreCache:true});
 await call('Emulation.setDeviceMetricsOverride',{width:1600,height:1050,deviceScaleFactor:1,mobile:false});
 const readyStart=Date.now();let ready=false,lastState='';
 while(Date.now()-readyStart<15000){
  const r=await call('Runtime.evaluate',{expression:'({previewReady:!!window.previewReady,hookInstalled:!!window.__dssHookInstalled,callbackInvoked:!!window.__dssCallbackInvoked,observer:typeof window.__dssR2ReviewAccessories})',returnByValue:true});
  const state=r.result?.value;const encoded=JSON.stringify(state);if(encoded!==lastState){note('readiness-state',{state});lastState=encoded;}
  if(state?.previewReady&&state.observer==='function'){ready=true;break;}
  if(errors.length)throw Error(JSON.stringify(errors));await new Promise(r=>setTimeout(r,100));
 }
 if(!ready)throw Error('Readiness deadline15s; see separately observed states');
 note('ready-for-assertions');
 const defaultShots=out.includes('/sources/')?[['web-front',{}],['web-rear',{view:'rear'}],['web-exploded',{explode:true}],['web-interior',{inside:true}],['web-side',{view:'side'}]]:[['front',{}],['rear',{view:'rear'}],['body-side',{view:'side',only:['truck','hood','interior','driver','cab-roof'],width:1400,height:700}],['exploded',{explode:true}],['figure',{view:'figure',only:['candidate'],width:800,height:1000}],['helm',{only:['helm'],width:800,height:700}],['interior',{view:'top',only:['truck','hood','interior','driver'],width:1200,height:850}]];
 const shots=process.argv[3]?JSON.parse(fs.readFileSync(process.argv[3])):defaultShots;
 await new Promise(r=>setTimeout(r,150));
 const nav=await call('Runtime.evaluate',{expression:`(()=>{
 const model=window.PROTOTYPE.model,trace=[],failures=[];
 const same=(a,b)=>JSON.stringify([...a].sort((x,y)=>x-y))===JSON.stringify([...b].sort((x,y)=>x-y));
 function check(label,expectedIds,expectedBands){const st=window.inspectInstructions(),bands=window.__dssR2ReviewAccessories();if(!same(st.visible,expectedIds))failures.push(label+' membership');if(bands.filter(b=>b.visible).length!==expectedBands)failures.push(label+' bands');trace.push({label,state:st,bands,copyNote:document.querySelector('#recipe-copy-note').textContent,tray:document.querySelector('#step-parts').textContent});}
 const group11=model.instruction_plan.steps[10];window.setInstructionStep(11);check('11 main',group11.manual.ids,2);if(!group11.manual.ids.includes(169)||group11.manual.ids.includes(190))failures.push('11 root selection');
 window.setRecipeFrame(2);check('11 separate seed',[190],0);document.querySelector('#next-step').click();check('11 local return',group11.manual.ids,2);document.querySelector('#previous-step').click();check('11 previous seed',[190],0);
 for(const s of model.instruction_plan.steps.filter(s=>s.manual.corrected)){
  window.setInstructionStep(s.number);
  const frames=s.manual.frames.filter(f=>!(s.manual.repeat_prefix_from&&f.number<=s.manual.repeat_prefix_frames));
  window.setRecipeFrame(frames[0].number);
  for(const f of frames){const bandCount=f.bands_installed?model.suspension_bands.filter(b=>b.anchor_ids.every(i=>f.shown_ids.includes(i))).length:0;check(s.number+' panel '+f.number,f.shown_ids,bandCount);if(window.inspectInstructions().recipeFrame!==f.number)failures.push('ordered traversal '+s.number+' '+f.number);document.querySelector('#next-step').click();}
  check(s.number+' overview return',s.manual.ids,s.manual.bands_installed?2:0);
 }
 const left=model.instruction_plan.steps[16],right=model.instruction_plan.steps[17];
 window.setInstructionStep(17);window.setRecipeFrame(1);
 for(const f of left.manual.frames.slice(0,4)){
  if(f.copy_count!==2||f.copy_new_ids.length!==2)failures.push('two-copy binding '+f.number);
  const expected={};for(const i of f.ids){const p=model.pieces.find(p=>p.id===i),k=p.part+'|'+p.color;expected[k]=(expected[k]||0)+1;}
  const actual={};document.querySelectorAll('#step-parts [data-lot]').forEach(e=>actual[e.dataset.lot]=Number(e.dataset.quantity));
  if(JSON.stringify(Object.entries(expected).sort())!==JSON.stringify(Object.entries(actual).sort()))failures.push('per-copy quantity '+f.number);
  if(!document.querySelector('#step-description').textContent.includes('Make 2 identical lower bases'))failures.push('2x reader label '+f.number);
  document.querySelector('#next-step').click();
 }
 window.setInstructionStep(18);
 if([...document.querySelector('#recipe-frame').options].some(o=>[1,2,3,4].includes(Number(o.value))))failures.push('duplicate right prefix options');
 if(!document.querySelector('#recipe-copy-note').textContent.includes('second lower base'))failures.push('right copy return note');
 window.setInstructionStep(17);document.querySelector('#next-step').click();if(window.inspectInstructions().step!==18||window.inspectInstructions().recipeFrame!==5)failures.push('right entry must skip common prefix');
 if(!same(left.manual.common_prefix_copies[1],right.manual.frames[3].shown_ids))failures.push('distinct remaining copy');
 return {trace,failures,physical_tested:false};
 })()`,returnByValue:true});
 if(nav.exceptionDetails)throw Error(JSON.stringify(nav.exceptionDetails));
 note('assertions-returned');
 fs.writeFileSync(`${out}/r2-navigation.json`,JSON.stringify(nav.result.value,null,2));
 if(nav.result.value.failures.length)throw Error(JSON.stringify(nav.result.value.failures));
 const captures=[['rear-bands',10,1],['bumper-root-overview',11,0],['separate-bumper-seed',11,2],['bumper-receiver-bands',12,6],['two-copy-base',17,4],['left-carrier-receiver-bands',17,15],['second-base-return',18,5],['right-carrier-installed-bands',18,16]];
 for(const [name,step,panel]of captures){
  note('before-screenshot',{name,step,panel});
  await call('Runtime.evaluate',{expression:`(async()=>{window.setInstructionStep(${step});if(${panel})window.setRecipeFrame(${panel});await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));})()`,awaitPromise:true,returnByValue:true});
  const shot=await call('Page.captureScreenshot',{format:'png'});fs.writeFileSync(`${out}/r2-${name}.png`,Buffer.from(shot.data,'base64'));
 }
 fs.writeFileSync(`${out}/r2-browser-check.json`,JSON.stringify({errors,screenshots:captures,trace_count:nav.result.value.trace.length},null,2));
 if(errors.length)throw Error(JSON.stringify(errors));
 console.log('PASS: actual accessory visibility, root overview return, 2x common-prefix quantities and distinct-copy return');
}catch(error){telemetry.failure=String(error?.stack||error);note('failure',{error:telemetry.failure});throw error;}finally{
 note('before-owned-chrome-close',{chromePid:chrome.pid,exitCode:chrome.exitCode,stderrTail:chromeLog});ws?.close();
 if(chrome.exitCode===null){try{chrome.kill('SIGTERM');}catch(error){note('chrome-close-error',{error:String(error)});}}
 await Promise.race([chrome.exitCode!==null?Promise.resolve():once(chrome,'exit'),new Promise(resolve=>setTimeout(resolve,3000))]);
 note('finally-complete',{chromeExitCode:chrome.exitCode,chromeSignal:chrome.signalCode});
}
