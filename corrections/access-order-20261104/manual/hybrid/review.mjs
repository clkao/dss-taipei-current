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
  const r=await call('Runtime.evaluate',{expression:'({previewReady:!!window.previewReady,hookInstalled:!!window.__dssHookInstalled,callbackInvoked:!!window.__dssCallbackInvoked,observer:typeof window.__dssR2ReviewAccessories,hybrid:!!document.querySelector("#ordered-prefix-inspect")})',returnByValue:true});
  const state=r.result?.value;const encoded=JSON.stringify(state);if(encoded!==lastState){note('readiness-state',{state});lastState=encoded;}
  if(state?.previewReady&&state.observer==='function'&&state.hybrid){ready=true;break;}
  if(errors.length)throw Error(JSON.stringify(errors));await new Promise(r=>setTimeout(r,100));
 }
 if(!ready)throw Error('Readiness deadline15s; see separately observed states');
 note('ready-for-assertions');
 const defaultShots=out.includes('/sources/')?[['web-front',{}],['web-rear',{view:'rear'}],['web-exploded',{explode:true}],['web-interior',{inside:true}],['web-side',{view:'side'}]]:[['front',{}],['rear',{view:'rear'}],['body-side',{view:'side',only:['truck','hood','interior','driver','cab-roof'],width:1400,height:700}],['exploded',{explode:true}],['figure',{view:'figure',only:['candidate'],width:800,height:1000}],['helm',{only:['helm'],width:800,height:700}],['interior',{view:'top',only:['truck','hood','interior','driver'],width:1200,height:850}]];
 const shots=process.argv[3]?JSON.parse(fs.readFileSync(process.argv[3])):defaultShots;
 await new Promise(r=>setTimeout(r,150));
 const nav=await call('Runtime.evaluate',{expression:`(()=>{
 const trace=[],failures=[],same=(a,b)=>JSON.stringify([...a].sort((x,y)=>x-y))===JSON.stringify([...b].sort((x,y)=>x-y));
 const box=()=>document.querySelector('#ordered-prefix-diagram');
 function check(name,ids,diagram){const state=window.inspectInstructions();if(!same(state.visible,ids))failures.push(name+' membership');if(box().hidden===diagram)failures.push(name+' diagram visibility');trace.push({name,state,diagram:!box().hidden,tray:document.querySelector('#step-parts').textContent});}
 const buttons=()=>[...document.querySelector('#ordered-prefix-inspect').querySelectorAll('button')];
 document.querySelector('#start-building').click();check('start diagram',[172,178,216,231],true);
 if(!document.querySelector('#step-parts').textContent.includes('2 × 32018 black beams · 2 × 2780 black pins'))failures.push('one2+2tray');
 for(let i=1;i<=3;i++){buttons()[i].click();check('inspect'+i,[[172],[172,216,231],[172,216,231,178]][i-1],false);buttons()[0].click();check('diagram return'+i,[172,178,216,231],true);}
 document.querySelector('#next-step').click();check('Next4',window.PROTOTYPE.model.instruction_plan.steps[0].manual.frames[3].shown_ids,false);if(window.inspectInstructions().recipeFrame!==4)failures.push('Next4');
 document.querySelector('#previous-step').click();check('Previous diagram',[172,178,216,231],true);
 window.setRecipeFrame(0);if(!box().hidden)failures.push('overview hides diagram');
 const select=document.querySelector('#recipe-frame');select.value='3';select.dispatchEvent(new Event('change'));check('selector diagram',[172,178,216,231],true);
 if([...select.options].some(o=>['1','2'].includes(o.value)))failures.push('duplicate primary options');
 window.setInstructionStep(11);if(!box().hidden)failures.push('root hides diagram');const root=window.inspectInstructions();if(!root.visible.includes(169)||root.visible.includes(190)||window.__dssR2ReviewAccessories().filter(b=>b.visible).length!==2)failures.push('main11 bands/root');
 window.setRecipeFrame(2);if(!same(window.inspectInstructions().visible,[190])||window.__dssR2ReviewAccessories().some(b=>b.visible))failures.push('local seed');
 window.setInstructionStep(17);window.setRecipeFrame(1);if(!document.querySelector('#step-description').textContent.includes('Make 2 identical lower bases'))failures.push('2xprefix');
 window.setInstructionStep(17);document.querySelector('#next-step').click();if(window.inspectInstructions().step!==18||window.inspectInstructions().recipeFrame!==5)failures.push('secondcopyreturn');
 return {trace,failures,physical_tested:false};
 })()`,returnByValue:true});
 if(nav.exceptionDetails)throw Error(JSON.stringify(nav.exceptionDetails));
 fs.writeFileSync(`${out}/r2-navigation.json`,JSON.stringify(nav.result.value,null,2));
 if(nav.result.value.failures.length)throw Error(JSON.stringify(nav.result.value.failures));
 const captures=[['diagram',0,1600,1050],['inspect1',1,1600,1050],['inspect2',2,1600,1050],['inspect3',3,1600,1050],['next4',4,1600,1050],['diagram-narrow',0,900,1000]];
 for(const [name,action,width,height] of captures){
  await call('Emulation.setDeviceMetricsOverride',{width,height,deviceScaleFactor:1,mobile:false});
  const result=await call('Runtime.evaluate',{expression:`(async()=>{window.setInstructionStep(1);window.setRecipeFrame(1);const b=[...document.querySelector('#ordered-prefix-inspect').querySelectorAll('button')];if(${action}>0&&${action}<4)b[${action}].click();if(${action}===4)document.querySelector('#next-step').click();const img=document.querySelector('#ordered-prefix-diagram img');await img.decode();await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));return {loaded:img.naturalWidth>0,title:document.querySelector('#step-title').textContent,description:document.querySelector('#step-description').textContent,note:document.querySelector('#recipe-copy-note').textContent,expectedActionTitle:${action}>0?('1'+String.fromCharCode(96+${action})+'. '+window.PROTOTYPE.model.instruction_plan.steps[0].manual.frames[${action}-1].title):null};})()`,awaitPromise:true,returnByValue:true});
  if(result.exceptionDetails||!result.result?.value?.loaded)throw Error('Image not loaded '+name);
  const settled=result.result.value;note('settled-reader-text',{name,...settled});
  if(action===0){
   if(settled.title!=='Actions 1–3 · Build the chassis core'||settled.description!=='1. Start with one beam. 2. Fit both pins. 3. Seat the second beam on BOTH exposed pins.'||settled.note!=='One diagram · collect these four parts once.')throw Error('Grouped settled reader text '+name);
  }else if(settled.title!==settled.expectedActionTitle)throw Error('Exact inspect/action caption '+name);
  const shot=await call('Page.captureScreenshot',{format:'png'});fs.writeFileSync(`${out}/r2-${name}.png`,Buffer.from(shot.data,'base64'));
 }
 fs.writeFileSync(`${out}/r2-browser-check.json`,JSON.stringify({errors,screenshots:captures,trace_count:nav.result.value.trace.length},null,2));
 if(errors.length)throw Error(JSON.stringify(errors));
 console.log('PASS: hybrid primary/inspect/return and retained R2 regression assertions');
}catch(error){telemetry.failure=String(error?.stack||error);note('failure',{error:telemetry.failure});throw error;}finally{
 note('before-owned-chrome-close',{chromePid:chrome.pid,exitCode:chrome.exitCode,stderrTail:chromeLog});ws?.close();
 if(chrome.exitCode===null){try{chrome.kill('SIGTERM');}catch(error){note('chrome-close-error',{error:String(error)});}}
 await Promise.race([chrome.exitCode!==null?Promise.resolve():once(chrome,'exit'),new Promise(resolve=>setTimeout(resolve,3000))]);
 note('finally-complete',{chromeExitCode:chrome.exitCode,chromeSignal:chrome.signalCode});
}
