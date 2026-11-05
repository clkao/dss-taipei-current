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
const viewer=path.resolve('builds/clear-logical/cycle2/package/viewer.html');
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
 await call('Emulation.setDeviceMetricsOverride',{width:390,height:900,deviceScaleFactor:1,mobile:false});
 await ready('Boolean(window.inspectGuide&&window.inspectGuide().imageLoaded)');
 const checks=[];
 async function clickSelector(selector,client=call,evalFn=evaluate){
  const q=await evalFn(`(()=>{const e=document.querySelector(${JSON.stringify(selector)}),r=e.getBoundingClientRect();return {x:r.x+r.width/2,y:r.y+r.height/2}})()`);
  await client('Input.dispatchMouseEvent',{type:'mousePressed',x:q.x,y:q.y,button:'left',clickCount:1});
  await client('Input.dispatchMouseEvent',{type:'mouseReleased',x:q.x,y:q.y,button:'left',clickCount:1});
 }
 async function popupClient(tab){
  const socket=new WebSocket(tab.webSocketDebuggerUrl);await once(socket,'open');let next=0;const waits=new Map();
  socket.addEventListener('message',({data})=>{const r=JSON.parse(data);if(r.method==='Runtime.exceptionThrown')errors.push(r.params);const p=waits.get(r.id);if(p){waits.delete(r.id);clearTimeout(p.timer);r.error?p.reject(Error(JSON.stringify(r.error))):p.resolve(r.result)}});
  const client=(method,params={})=>new Promise((resolve,reject)=>{const id=++next;const timer=setTimeout(()=>{waits.delete(id);reject(Error(method+' popup timeout'))},5000);waits.set(id,{resolve,reject,timer});socket.send(JSON.stringify({id,method,params}))});
  const ev=async expression=>{const r=await client('Runtime.evaluate',{expression,returnByValue:true});if(r.exceptionDetails)throw Error(JSON.stringify(r.exceptionDetails));return r.result.value};
  await client('Runtime.enable');await client('Page.enable');return {socket,client,ev};
 }
 for(const page of [10,36]){
  await evaluate(`(()=>{const s=document.querySelector('#pages');s.value='${page}';s.dispatchEvent(new Event('change'));return true})()`);
  await ready(`window.inspectGuide().page===${page}&&window.inspectGuide().imageLoaded`);
  const link=await evaluate("document.querySelector('#enlarge').href");await clickSelector('#enlarge');
  let pop;for(let k=0;k<60;k++){const list=await(await fetch(`http://127.0.0.1:${port}/json`)).json();pop=list.find(t=>t.url===link);if(pop)break;await new Promise(r=>setTimeout(r,100))}
  if(!pop)throw Error('Actual enlargement link did not open an image tab');
  const {socket,client,ev}=await popupClient(pop);
  try{
   await client('Emulation.setDeviceMetricsOverride',{width:390,height:900,deviceScaleFactor:1,mobile:false});
   for(let k=0;k<60;k++){if(await ev('Boolean(document.images[0]?.complete&&document.images[0]?.naturalWidth)'))break;await new Promise(r=>setTimeout(r,100))}
   const state=()=>ev('(()=>{const i=document.images[0],r=i.getBoundingClientRect();return {naturalWidth:i.naturalWidth,width:r.width,height:r.height,scrollX,scrollY,url:location.href}})()');
   const fit=await state();
   await clickSelector('img',client,ev);
   const enlarged=await state();if(enlarged.width<enlarged.naturalWidth*.99)throw Error('Native image click did not enlarge to source pixels');
   // Scroll within the actual enlarged browser image to the detail being reviewed.
   await ev(`window.scrollTo(${page===36?620:400},0)`);
   const shot=await client('Page.captureScreenshot',{format:'png'});fs.writeFileSync(path.join(out,'enlarged-'+page+'.png'),Buffer.from(shot.data,'base64'));
   checks.push({page,actual_link:link,fit,enlarged:await state(),interaction:'Actual Enlarge page link click, then native image click and browser scrolling'});
  }finally{await client('Page.close');socket.close()}
 }
 await clickSelector('a[href="model-viewer.html"]');await ready('Boolean(window.previewReady&&window.setInstructionStep)');
 const threeURL=await evaluate('location.href');
 const history=await call('Page.getNavigationHistory');if(history.currentIndex<1)throw Error('No browser history entry for guide');
 const back=history.entries[history.currentIndex-1];await call('Page.navigateToHistoryEntry',{entryId:back.id});
 await ready('Boolean(window.inspectGuide&&window.inspectGuide().page===36&&window.inspectGuide().imageLoaded)');
 checks.push({actual_3D_link:threeURL,back_history_entry:back,returned_guide:await evaluate('window.inspectGuide()'),interaction:'Actual 3D inspection anchor click, then Page.navigateToHistoryEntry for Back'});
 const shot=await call('Page.captureScreenshot',{format:'png'});fs.writeFileSync(path.join(out,'returned-guide-390.png'),Buffer.from(shot.data,'base64'));
 if(errors.length)throw Error(JSON.stringify(errors));
 fs.writeFileSync(path.join(out,'browser-check.json'),JSON.stringify({checks,errors,headless:true,native_browser_image_viewer:true,human_testing:false,default_fit_detail_readability_claimed:false,enlarged_readability:'Author image inspection required for the captured natural-pixel state'},null,2));
 note('all-assets-captured');
}finally{
 ws?.close();
 if(chrome.exitCode===null&&chrome.signalCode===null){try{chrome.kill('SIGTERM');}catch(error){note('chrome-close-error',{error:String(error)});}}
 if(chrome.exitCode===null&&chrome.signalCode===null)await Promise.race([once(chrome,'exit'),new Promise((_,reject)=>setTimeout(()=>reject(Error('Chrome close timeout')),5000))]);
 note('finished',{chromeExit:telemetry.chromeExit,stderr:chromeLog});
}
