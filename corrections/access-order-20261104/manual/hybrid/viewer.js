// DSS presentation only. Exact source replay remains in the existing viewer.
(()=>{
 const timer=setInterval(()=>{
  if(!window.previewReady||!window.setRecipeFrame||!document.querySelector('#recipe-frame'))return;
  clearInterval(timer);
  const frame=window.setRecipeFrame,step=window.setInstructionStep;
  const box=document.createElement('section');box.id='ordered-prefix-diagram';box.hidden=true;
  box.style.cssText='position:fixed;z-index:5;background:#f5f7fa;overflow:auto;box-sizing:border-box;padding:12px';
  box.innerHTML='<img src="ordered-prefix.png" alt="1 Start with one beam. 2 Fit both pins. 3 Add the second beam." style="width:100%;height:calc(100% - 72px);object-fit:contain"><p style="text-align:center;color:#27333b">3. Seat the second beam on BOTH exposed pins.</p>';
  document.body.append(box);
  const actions=document.createElement('div');actions.id='ordered-prefix-inspect';actions.hidden=true;
  document.querySelector('#recipe-navigation').append(actions);
  const fit=()=>{const r=document.querySelector('canvas').getBoundingClientRect();Object.assign(box.style,{left:r.left+'px',top:r.top+'px',width:r.width+'px',height:r.height+'px'});};
  window.addEventListener('resize',fit);
  function inspect(n){box.hidden=true;frame(n);actions.hidden=false;document.querySelector('#recipe-copy-note').textContent='';}
  function diagram(){
   frame(3);fit();box.hidden=false;actions.hidden=false;
   // The retained notes wrapper may be outside this wrapper (independent readiness timers).
   // Apply grouped text after that synchronous call chain; never overwrite Inspect mode.
   queueMicrotask(()=>{
    const state=window.inspectInstructions();if(box.hidden||state.step!==1||state.recipeFrame!==3)return;
    const title=document.querySelector('#step-title'),description=document.querySelector('#step-description');
    title.hidden=false;title.textContent='Actions 1–3 · Build the chassis core';
    description.hidden=false;description.textContent='1. Start with one beam. 2. Fit both pins. 3. Seat the second beam on BOTH exposed pins.';
    document.querySelector('#recipe-copy-note').textContent='One diagram · collect these four parts once.';
   });
   const tray=document.querySelector('#step-parts');tray.replaceChildren();
   const title=document.createElement('h3');title.textContent='Collect once';
   const parts=document.createElement('p');parts.textContent='2 × 32018 black beams · 2 × 2780 black pins';tray.append(title,parts);tray.hidden=false;
  }
  for(const [label,fn] of [['Diagram',diagram],['Inspect action 1',()=>inspect(1)],['Inspect action 2',()=>inspect(2)],['Inspect action 3 / installed',()=>inspect(3)]]){const b=document.createElement('button');b.type='button';b.textContent=label;b.onclick=fn;actions.append(b);}
  window.setRecipeFrame=n=>{
   const s=window.inspectInstructions();box.hidden=true;actions.hidden=true;
   if(s.step===1&&[1,2,3].includes(Number(n)))return diagram();
   return frame(n);
  };
  window.setInstructionStep=(n,opts)=>{
   box.hidden=true;actions.hidden=true;const result=step(n,opts);
   if(Number(n)===1){const select=document.querySelector('#recipe-frame');for(const o of [...select.options]){if(['1','2'].includes(o.value))o.remove();else if(o.value==='3')o.textContent='Actions 1–3 · one diagram';}}
   return result;
  };
  // Inspected source states are optional; primary Next continues after the prefix.
  const next=document.querySelector('#next-step'),originalNext=next.onclick;
  next.onclick=e=>{const s=window.inspectInstructions();if(s.step===1&&[1,2,3].includes(s.recipeFrame))return window.setRecipeFrame(4);return originalNext.call(next,e);};
 },60);
})();
