// DSS correction notes and completed-child trays; no geometry or movement changes.
const correctionTimer=setInterval(()=>{
 if(!window.previewReady||!window.setRecipeFrame)return;
 clearInterval(correctionTimer);
 const original=window.setRecipeFrame,main=window.setInstructionStep;
 window.setRecipeFrame=value=>{
  const result=original(value),state=window.inspectInstructions();
  const s=window.PROTOTYPE.model.instruction_plan.steps[state.step-1];
  if(!s?.manual.corrected)return result;
  const f=s.manual.frames.find(f=>f.number===state.recipeFrame);
  if(!f)return result;
  const description=document.querySelector('#step-description');description.hidden=false;
  description.textContent=(f.note||'')+' '+(f.child?'Use the completed '+f.child.replaceAll('-',' ')+'. ':'')+'Installed view; insertion clearance remains unverified.';
  const tray=document.querySelector('#step-parts');
  if(f.child){tray.replaceChildren();const title=document.createElement('h3');title.textContent='Completed unit - no new loose stock';const label=document.createElement('p');label.textContent='1 × '+f.child.replaceAll('-',' ')+' ('+f.ids.length+' pieces)';tray.append(title,label);tray.hidden=false;}
  return result;
 };
 window.setInstructionStep=(n,options)=>{
  const result=main(n,options),s=window.PROTOTYPE.model.instruction_plan.steps[n-1];
  if(s?.manual.corrected){const tray=document.querySelector('#step-parts');tray.textContent='Review the ordered panels above; each panel shows its own loose parts or completed unit.';tray.hidden=false;document.querySelector('#recipe-copy-note').textContent='Follow all panels in order. Each side has its own complete recipe.';}
  return result;
 };
},50);
