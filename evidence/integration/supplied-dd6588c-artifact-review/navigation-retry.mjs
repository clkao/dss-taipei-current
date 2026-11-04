// One-off failed-only retry. PREPARED ONLY: requires a separate runtime lease.
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {createRequire} from 'node:module';
import {pathToFileURL, fileURLToPath} from 'node:url';
import {execFileSync} from 'node:child_process';
const evidence=path.dirname(fileURLToPath(import.meta.url));
const h=JSON.parse(fs.readFileSync(path.join(evidence,'../supplied-dd6588c-preparation/frozen-handoff.json')));
const pkg=h.paths.package;
const out=process.argv[2];
assert.ok(out,'Supply a fresh DSS evidence output directory');
fs.mkdirSync(out,{recursive:false});
const {chromium}=createRequire(h.invocation_cwd+'/package.json')('playwright-core');
const start=performance.now();
const errors=[],network=[];
const result={mode:'headless offline only; no live or human acceptance',states:[],events:[],page_errors:errors,http_requests:network,console:[],request_failures:[],process_samples:[],node_pid:process.pid,node_version:process.version,environment:{TMPDIR:process.env.TMPDIR,XDG_CACHE_HOME:process.env.XDG_CACHE_HOME},status:'running'};
const event=(name,detail={})=>result.events.push({name,ms:performance.now()-start,...detail});
const save=()=>fs.writeFileSync(path.join(out,'navigation.json'),JSON.stringify(result,null,2)+'\n');
const known=new Set([process.pid]);
function sampleProcesses(){
 try{
  const rows=execFileSync('/bin/ps',['-axo','pid=,ppid=,pgid=,command='],{encoding:'utf8',timeout:1000,maxBuffer:8*1024*1024}).split('\n').map(line=>line.trim().match(/^(\d+)\s+(\d+)\s+(\d+)\s+(.+)$/)).filter(Boolean).map(m=>({pid:Number(m[1]),ppid:Number(m[2]),pgid:Number(m[3]),command:m[4]}));
  let added=true;while(added){added=false;for(const row of rows)if(known.has(row.ppid)&&!known.has(row.pid)){known.add(row.pid);added=true;}}
  const owned=rows.filter(row=>known.has(row.pid)&&!row.command.startsWith('/bin/ps '));
  for(const row of owned){const match=row.command.match(/--user-data-dir=(.+?) --/);if(match)row.profile=match[1];}
  result.process_samples.push({ms:performance.now()-start,owned});
 }catch(error){event('process-sample-error',{message:String(error)});}
}
let browser,context,timer;
try{
 event('launch-start');sampleProcesses();timer=setInterval(sampleProcesses,1000);
 browser=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true,timeout:20000,args:['--enable-webgl','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--allow-file-access-from-files']});
 event('launch-complete',{browser_version:browser.version()});sampleProcesses();
 context=await browser.newContext({offline:true,viewport:{width:1100,height:1100}});
 const page=await context.newPage();page.setDefaultTimeout(12000);
 page.on('domcontentloaded',()=>event('domcontentloaded'));
 page.on('load',()=>event('load'));
 page.on('crash',()=>event('page-crash'));
 page.on('console',message=>result.console.push({ms:performance.now()-start,type:message.type(),text:message.text(),location:message.location()}));
 page.on('pageerror',error=>{errors.push(error.message);event('pageerror',{message:error.message,stack:error.stack});});
 page.on('request',request=>{if(/^https?:/.test(request.url()))network.push(request.url());});
 page.on('requestfailed',request=>result.request_failures.push({ms:performance.now()-start,url:request.url(),failure:request.failure()}));
 event('goto-start');
 await page.goto(pathToFileURL(path.join(pkg,'viewer.html')).href,{waitUntil:'load',timeout:30000});
 event('goto-complete');
 await page.waitForFunction(()=>window.instructionReady);
 event('readiness-observed');
 const snapshots={};
for(const [id,count] of [['collect-candidate',8],['collect-tsai',16],['attach-banner',18]]){event('step-start',{id});await page.locator('#selector').selectOption(id);const state=await page.evaluate(()=>({binding:window.currentBinding,tray:window.currentTray}));assert.equal(state.binding.step,id);assert.equal(state.binding.cumulative.length,count);assert.equal(await page.locator('#approach').isDisabled(),true);assert.equal(await page.locator('#callouts button').count(),0);assert.equal(await page.locator('footer strong').innerText(),'Draft — construction unverified');
const entries=state.tray.entries;if(id==='attach-banner'){assert.ok(entries.every(e=>e.kind==='loose'));assert.equal(entries.reduce((n,e)=>n+e.quantity,0),2);assert.deepEqual(state.binding.new,['o/17','o/18']);}else{assert.equal(entries.length,1);assert.equal(entries[0].kind,'supplied');assert.equal(entries[0].quantity,1);assert.equal(entries[0].occurrences.length,8);}
snapshots[id]=state;result.states.push({...state,visible:{title:await page.locator('#title').innerText(),parts:await page.locator('#parts').innerText(),caption:await page.locator('#caption').innerText(),limits:await page.locator('#limits').innerText()}});await page.screenshot({path:path.join(out,id+'.png'),fullPage:true});}
await page.locator('#previous').click();assert.deepEqual(await page.evaluate(()=>({binding:window.currentBinding,tray:window.currentTray})),snapshots['collect-tsai']);await page.locator('#next').click();assert.deepEqual(await page.evaluate(()=>({binding:window.currentBinding,tray:window.currentTray})),snapshots['attach-banner']);result.previous_next_exact=true;assert.deepEqual(errors,[]);assert.deepEqual(network,[]);
 result.status='passed';event('assertions-complete');
}catch(error){
 result.status='failed';result.failure={name:error.name,message:error.message,stack:error.stack};event('failure',result.failure);throw error;
}finally{
 clearInterval(timer);sampleProcesses();save();
 try{if(context)await context.close();event('context-closed');}
 catch(error){result.cleanup_error=String(error);event('context-close-error',{message:String(error)});}
 try{if(browser)await browser.close();event('browser-closed');}
 finally{sampleProcesses();event('collector-finished');save();}
}
console.log(JSON.stringify(result));
