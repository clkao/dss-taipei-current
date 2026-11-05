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
const viewer=path.resolve('builds/clear-logical/candidate/viewer.html');
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
 await ready('Boolean(window.inspectGuide)');
 const checks=[];
 for(const page of [1,8,9,10,12,14,16,24,25,30,32,40,49,50,51,69,71,72,73,80]){
  await evaluate(`(()=>{const s=document.querySelector('#pages');s.value='${page}';s.dispatchEvent(new Event('change'));return true})()`);
  await ready(`window.inspectGuide().page===${page}&&window.inspectGuide().imageLoaded`);
  checks.push(await evaluate('window.inspectGuide()'));
 }
 await evaluate("document.querySelector('#prev').click()");await ready('window.inspectGuide().page===79&&window.inspectGuide().imageLoaded');
 await evaluate("document.querySelector('#next').click()");await ready('window.inspectGuide().page===80&&window.inspectGuide().imageLoaded');
 await evaluate("(()=>{const s=document.querySelector('#pages');s.value='49';s.dispatchEvent(new Event('change'));return true})()");await ready('window.inspectGuide().page===49&&window.inspectGuide().imageLoaded');
 for(const width of [1400,390]){
  await call('Emulation.setDeviceMetricsOverride',{width,height:900,deviceScaleFactor:1,mobile:false});
  const layout=await evaluate('({viewport:innerWidth,scroll:document.documentElement.scrollWidth,image:document.querySelector("#diagram").getBoundingClientRect().width})');
  if(layout.scroll>layout.viewport+1)throw Error('Horizontal overflow');
  const shot=await call('Page.captureScreenshot',{format:'png'});fs.writeFileSync(path.join(out,'guide-'+width+'.png'),Buffer.from(shot.data,'base64'));checks.push(layout);
 }
 await call('Page.navigate',{url:'file://'+path.resolve('builds/clear-logical/candidate/model-viewer.html')});
 await ready('Boolean(window.previewReady&&window.setInstructionStep)');
 await evaluate('window.setInstructionStep(41)');checks.push(await evaluate('window.inspectInstructions()'));
 await call('Page.navigate',{url:'file://'+viewer+'#page=49'});await ready('Boolean(window.inspectGuide&&window.inspectGuide().page===49&&window.inspectGuide().imageLoaded)');
 if(errors.length)throw Error(JSON.stringify(errors));
 fs.writeFileSync(path.join(out,'browser-check.json'),JSON.stringify({checks,errors,headless:true,live_user_review:false,return_to_guide:true},null,2));
 note('all-assets-captured');
}finally{
 ws?.close();
 if(chrome.exitCode===null&&chrome.signalCode===null){try{chrome.kill('SIGTERM');}catch(error){note('chrome-close-error',{error:String(error)});}}
 if(chrome.exitCode===null&&chrome.signalCode===null)await Promise.race([once(chrome,'exit'),new Promise((_,reject)=>setTimeout(()=>reject(Error('Chrome close timeout')),5000))]);
 note('finished',{chromeExit:telemetry.chromeExit,stderr:chromeLog});
}
