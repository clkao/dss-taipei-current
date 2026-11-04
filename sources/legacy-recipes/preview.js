import * as THREE from 'three';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
import {mergeGeometries} from 'three/addons/utils/BufferGeometryUtils.js';
import {CatalogScene} from '../../scripts/lego_catalog_scene.js';
import {firstPieceHit} from '../../scripts/lego_piece_selection.js';
import {createPreviewMotion} from './preview_motion.js';
const {model,placements,catalog,summary}=window.PROTOTYPE;
const canvas=document.querySelector('canvas');
const scene=new THREE.Scene();scene.background=new THREE.Color('#f2eee7');
scene.add(new THREE.HemisphereLight(0xffffff,0xb8a99b,2.8));
const sun=new THREE.DirectionalLight(0xfff5e8,3.2);sun.position.set(25,50,30);scene.add(sun);
const fill=new THREE.DirectionalLight(0xffffff,1.5);fill.position.set(-20,15,-30);scene.add(fill);
// Bounded resolution; a 30 fps presentation loop, otherwise render on demand.
// Manual captures render and read back synchronously, so they need no retained buffer.
const renderer=new THREE.WebGLRenderer({canvas,antialias:true});
renderer.setPixelRatio(Math.min(devicePixelRatio,1.75));renderer.setSize(canvas.clientWidth,canvas.clientHeight,false);
const camera=new THREE.OrthographicCamera(-20,20,20,-20,.1,1000);
camera.aspect=canvas.clientWidth/canvas.clientHeight;
const controls=new OrbitControls(camera,canvas);controls.enableDamping=true;
let framePending=null,renderedFrames=0,sceneUpdates=0,totalUpdateMs=0,lastUpdateMs=0,cameraFits=0,resizeNotifications=0,bufferResizes=0;
const reducedMotion=matchMedia('(prefers-reduced-motion: reduce)');
let presentationMotion=null,animationEnabled=!reducedMotion.matches,motionEngaged=animationEnabled,animationTime=0,lastMotionFrame=null,lastDraw=0,canvasInView=true,interacting=false,orbitResumeAt=0,capturing=false;
const motionRunning=()=>animationEnabled&&presentationMotion?.shown&&!document.hidden&&canvasInView&&!capturing;
function requestRender(){if(framePending===null)framePending=requestAnimationFrame(frame)}
function renderNow(){renderer.render(scene,camera);renderedFrames++}
function frame(now){
 framePending=null;const running=motionRunning();
 if(running&&now-lastDraw<1000/30-1){requestRender();return}
 const dt=lastMotionFrame===null?0:Math.min((now-lastMotionFrame)/1000,.1);lastMotionFrame=running?now:null;
 if(running){animationTime+=dt;presentationMotion.pose(animationTime);if(!interacting&&now>orbitResumeAt){const offset=camera.position.clone().sub(controls.target);offset.applyAxisAngle(new THREE.Vector3(0,1,0),dt*.035);camera.position.copy(controls.target).add(offset)}}
 controls.update();renderNow();lastDraw=now;if(running)requestRender();
}
controls.addEventListener('change',requestRender);
controls.addEventListener('start',()=>{interacting=true});
controls.addEventListener('end',()=>{interacting=false;orbitResumeAt=performance.now()+5000});
const assembly=new CatalogScene(scene,catalog,placements,model.pieces,{depthBias:p=>model.render_depth_bias?.[p.id]??1});
const byId=new Map(model.pieces.map(p=>[p.id,p]));
const compactPanel=Boolean(document.querySelector('#build-controls'));
function setPanelMode(mode){
 for(const button of document.querySelectorAll('[data-panel-mode]')){
  const active=button.dataset.panelMode===mode;button.setAttribute('aria-selected',String(active));button.tabIndex=active?0:-1;
 }
 for(const panel of document.querySelectorAll('[data-panel-content]'))panel.hidden=panel.dataset.panelContent!==mode;
}
for(const button of document.querySelectorAll('[data-panel-mode]')){
 button.onclick=()=>setPanelMode(button.dataset.panelMode);
 button.onkeydown=e=>{if(e.key==='ArrowLeft'||e.key==='ArrowRight'){e.preventDefault();const next=button.dataset.panelMode==='build'?'inspect':'build';setPanelMode(next);document.querySelector(`[data-panel-mode="${next}"]`).focus()}};
}
window.setPanelMode=setPanelMode;
const wantedCopy=document.querySelector('#copy-wanted-xml');
if(wantedCopy)wantedCopy.onclick=async()=>{
 const status=document.querySelector('#wanted-copy-status');
 try{const response=await fetch('wanted-list.xml');if(!response.ok)throw Error('Wanted list unavailable');await navigator.clipboard.writeText(await response.text());status.textContent='Copied. Open BrickLink, choose Upload BrickLink XML format, and paste.'}
 catch{status.textContent='Clipboard unavailable. Use Download XML instead.'}
};
const hidden=new Set();let exploded=false,selected=null,visibleIds=null,highlightIds=null,showDecorations=true;
let showSuspensionBands=true;
let motionOffsets=new Map();
// Artwork is split at the actual tile boundaries. Cord is a declared craft
// accessory preview, separate from catalog inventory and MPD rigid geometry.
const decorations=[];
const hoodTexture=new THREE.TextureLoader().load('data:image/png;base64,'+window.PROTOTYPE.hoodArtwork,requestRender);hoodTexture.colorSpace=THREE.SRGBColorSpace;
const surfaceTextures=Object.fromEntries(Object.entries(window.PROTOTYPE.surfaceArtworks||{}).map(([k,raw])=>{const t=new THREE.TextureLoader().load('data:image/png;base64,'+raw,requestRender);t.colorSpace=THREE.SRGBColorSpace;return[k,t]}));
// Use the house viewer's geometry merge utility. Keep part ownership and module
// boundaries separate so instruction visibility and exploded views remain exact.
const decalGroups=new Map();
let decalTriangles=0;
function collectDecal(surface,hood=false){
 const module=hood?'hood':surface.module||'truck',pieceId=surface.piece_id,artwork=hood?'hood':surface.artwork;
 const key=JSON.stringify([hood,module,pieceId,artwork]);
 if(!decalGroups.has(key))decalGroups.set(key,{hood,module,pieceId,artwork,geometries:[]});
 const geo=new THREE.BufferGeometry();geo.setAttribute('position',new THREE.Float32BufferAttribute(surface.vertices.flat(),3));geo.setAttribute('uv',new THREE.Float32BufferAttribute(surface.uv.flat(),2));geo.setIndex(surface.indices||[0,1,2,0,2,3]);geo.computeVertexNormals();
 decalGroups.get(key).geometries.push(geo);
}
for(const surface of model.extra_decal_surfaces||[])collectDecal(surface);
if(model.decal_surfaces)for(const surface of model.decal_surfaces)collectDecal(surface,true);
for(const group of decalGroups.values()){
 const geometry=mergeGeometries(group.geometries);if(!geometry)throw Error('Incompatible decal patch geometry');
 decalTriangles+=geometry.index.count/3;
 group.geometries.forEach(geo=>geo.dispose());group.geometries=[];
 const transparent=group.hood?!!model.hood_artwork_transparent:true;
 const material=new THREE.MeshStandardMaterial({map:group.hood?hoodTexture:surfaceTextures[group.artwork],transparent,alphaTest:transparent?.02:0,roughness:group.hood?.7:.65,side:THREE.DoubleSide});
 const o=new THREE.Mesh(geometry,material);o.userData.module=group.module;o.userData.pieceId=group.pieceId;scene.add(o);decorations.push(o);
}
if(!model.decal_surfaces)for(const p of model.pieces.filter(p=>p.module==='truck'&&p.color==='orange'&&p.z===11&&p.x>=18)){
 const x=p.x,y=p.y,w=p.w,d=p.d;
 const geo=new THREE.BufferGeometry();
 geo.setAttribute('position',new THREE.Float32BufferAttribute([x,4.81,-y,x+w,4.81,-y,x+w,4.81,-(y+d),x,4.81,-(y+d)],3));
 geo.setAttribute('uv',new THREE.Float32BufferAttribute([y/8,(24-x)/6,y/8,(24-x-w)/6,(y+d)/8,(24-x-w)/6,(y+d)/8,(24-x)/6],2));geo.setIndex([0,1,2,0,2,3]);geo.computeVertexNormals();
 const o=new THREE.Mesh(geo,new THREE.MeshStandardMaterial({map:hoodTexture,roughness:.7,side:THREE.DoubleSide}));scene.add(o);decorations.push(o);
}
const ropeAnchors=model.rope_anchors||[[1,-.42,14],[8,-.42,15],[17,-.42,13.5],[23.8,-.42,12],[24.6,.5,11.5],[24.75,4,10.5],[24.6,7.5,11.5],[23.8,8.42,12],[17,8.42,13.5],[8,8.42,15],[1,8.42,14]];
const ropePoints=[];
for(let i=0;i<ropeAnchors.length-1;i++)for(let k=0;k<16;k++){
 const t=k/16,a=ropeAnchors[i],b=ropeAnchors[i+1],sag=model.rope_sag_plates?.[i]??(i<3||i>6?1.6:0),z=a[2]*(1-t)+b[2]*t-sag*4*t*(1-t);
 ropePoints.push(new THREE.Vector3(a[0]*(1-t)+b[0]*t,z*.4,-(a[1]*(1-t)+b[1]*t)));
}
const last=ropeAnchors.at(-1);ropePoints.push(new THREE.Vector3(last[0],last[2]*.4,-last[1]));
const cord=new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(ropePoints),300,.04,8,false),new THREE.MeshStandardMaterial({color:'#e8dcc6',roughness:1}));if(model.cord!==false){scene.add(cord);decorations.push(cord)}
for(const band of model.suspension_bands||[]){
 const [a,b]=band.centers_studs.map(([x,y,z])=>new THREE.Vector3(x,z,-y));
 const along=b.clone().sub(a).normalize(),up=new THREE.Vector3(0,1,0),radius=.3,points=[];
 // Routing guide around the two towballs, not an elastic force simulation.
 for(let k=0;k<=32;k++){const angle=Math.PI/2+k*Math.PI/32;points.push(a.clone().addScaledVector(along,Math.cos(angle)*radius).addScaledVector(up,Math.sin(angle)*radius))}
 for(let k=0;k<=32;k++){const angle=-Math.PI/2+k*Math.PI/32;points.push(b.clone().addScaledVector(along,Math.cos(angle)*radius).addScaledVector(up,Math.sin(angle)*radius))}
 const route=new THREE.CurvePath();for(let i=0;i<points.length;i++)route.add(new THREE.LineCurve3(points[i],points[(i+1)%points.length]));
 const guide=new THREE.Mesh(new THREE.TubeGeometry(route,160,.1,8,true),new THREE.MeshStandardMaterial({color:band.display_color||'#c91a09',roughness:.95}));
 guide.userData={module:'truck',suspensionBand:true,anchorIds:band.anchor_ids};scene.add(guide);decorations.push(guide);
}
const spread={hood:[6,3,0],'cab-roof':[3,5,0],deck:[-8,3,0],helm:[-6,10,0],banner:[-9,9,0],sail:[3,12,-3],
 'speaker-left':[10,5,5],'speaker-right':[10,5,-5],'ring-left':[-6,0,5],'ring-right':[-6,0,-5],candidate:[-10,9,-5],shield:[0,13,0]};
function update(){
 const started=performance.now();
 presentationMotion?.sync(motionEngaged&&!visibleIds&&!exploded&&!capturing,hidden);
 const overrides=new Map();
 for(const inst of placements.instances){const p=byId.get(inst.id),m=inst.matrix.map(r=>[...r]);
  const motion=motionOffsets.get(p.id);if(motion)for(let axis=0;axis<3;axis++)m[axis][3]+=motion[axis];
  if(exploded&&spread[p.module]){const [x,h,z]=spread[p.module];m[0][3]+=x*20;m[1][3]-=h*20;m[2][3]-=z*20}
  overrides.set(inst.id,{matrix:m});
 }
 assembly.update(p=>!hidden.has(p.module)&&(!visibleIds||visibleIds.has(p.id))&&!(presentationMotion?.shown&&presentationMotion.ids.has(p.id)),{overrides,newIds:selected?new Set([selected]):highlightIds||new Set()});
 if(presentationMotion?.shown)for(const id of presentationMotion.ids){const p=byId.get(id);if(!hidden.has(p.module))assembly.bounds.union(assembly.pieceBounds(p))}
 for(const o of decorations){const m=o.userData.module||'truck',id=o.userData.pieceId;const present=!visibleIds||(id?visibleIds.has(id):o.userData.anchorIds?o.userData.anchorIds.every(i=>visibleIds.has(i)):model.pieces.some(p=>p.module===m&&visibleIds.has(p.id)));o.visible=(o.userData.suspensionBand?showSuspensionBands:showDecorations)&&!hidden.has(m)&&present&&(o!==cord||!visibleIds||visibleIds.size===model.pieces.length);o.position.set(0,0,0);if(exploded&&spread[m])o.position.set(...spread[m])}
 requestRender();
 lastUpdateMs=performance.now()-started;totalUpdateMs+=lastUpdateMs;sceneUpdates++;
}
function fit(view='front',direction=null){
 cameraFits++;
 const box=assembly.bounds,center=box.getCenter(new THREE.Vector3()),size=box.getSize(new THREE.Vector3());
 const dir=new THREE.Vector3(...(direction||({front:[1,.68,1.15],'front-other':[1,.68,-1.15],rear:[-1,.6,-1.1],'rear-other':[-1,.6,1.1],underside:[1,-1.2,1.15],side:[0,.3,1.5],top:[.1,2,.1],figure:[1,.2,1]}[view]||[1,.7,1])));
 controls.target.copy(center);camera.position.copy(center).add(dir.normalize().multiplyScalar(150));camera.lookAt(center);camera.updateMatrixWorld(true);
 const corners=[];for(const x of [box.min.x,box.max.x])for(const y of [box.min.y,box.max.y])for(const z of [box.min.z,box.max.z])corners.push(new THREE.Vector3(x,y,z).applyMatrix4(camera.matrixWorldInverse));
 const projected=new THREE.Box3().setFromPoints(corners),height=Math.max(projected.max.y-projected.min.y,(projected.max.x-projected.min.x)/camera.aspect)*1.15,width=height*camera.aspect;
 const cx=(projected.min.x+projected.max.x)/2,cy=(projected.min.y+projected.max.y)/2;
 camera.left=cx-width/2;camera.right=cx+width/2;camera.top=cy+height/2;camera.bottom=cy-height/2;camera.zoom=1;camera.updateProjectionMatrix();controls.update();requestRender();
}
update();fit();
for(const [m,n] of Object.entries(summary.modules)){
 const label=document.createElement('label');label.innerHTML=`<input type="checkbox" checked data-module="${m}"><span>${({'truck':'Pickup chassis & body',hood:'Sloped hood',interior:'Driver seat & controls',driver:'Seated driver','cab-roof':'Lift-off cab roof',deck:'Removable stage',helm:'Helm console',banner:'Tall banner',sail:'Launch sail','speaker-left':'Left speaker','speaker-right':'Right speaker','ring-left':'Left life ring','ring-right':'Right life ring',candidate:'沈伯洋 lookalike',tsai:'小英 & speech bubble',shield:'Removable shield enclosure'})[m]||m}</span><small>${n}</small>`;
 document.querySelector('#modules').append(label);
 label.querySelector('input').onchange=e=>{const checked=e.target.checked,leaveBuild=compactPanel&&window.inspectInstructions?.().step;if(leaveBuild)window.setInstructionStep(0,{render:false});e.target.checked=checked;checked?hidden.delete(m):hidden.add(m);update();if(leaveBuild)fit()};
}
document.querySelector('#explode').onchange=e=>{const checked=e.target.checked;window.setInstructionStep?.(0,{render:false});e.target.checked=checked;exploded=checked;update();fit()};
document.querySelectorAll('[data-view]').forEach(b=>b.onclick=()=>fit(b.dataset.view));
document.querySelector('#road').onclick=()=>{window.setInstructionStep?.(0,{render:false});for(const m of ['banner','sail']){hidden.add(m);const input=document.querySelector(`[data-module="${m}"]`);if(input)input.checked=false}update();fit()};
document.querySelector('#cabin').onclick=()=>{window.setInstructionStep?.(0,{render:false});for(const m of ['cab-roof','banner','sail','speaker-left','speaker-right','candidate','helm']){hidden.add(m);const input=document.querySelector(`[data-module="${m}"]`);if(input)input.checked=false}update();fit('top')};
document.querySelector('#all').onclick=()=>{window.setInstructionStep?.(0,{render:false});hidden.clear();document.querySelectorAll('[data-module]').forEach(x=>x.checked=true);update();fit()};
let down;canvas.onpointerdown=e=>down=[e.clientX,e.clientY];
canvas.onpointerup=e=>{
 if(!down||Math.hypot(e.clientX-down[0],e.clientY-down[1])>5)return;
 const r=canvas.getBoundingClientRect(),mouse=new THREE.Vector2((e.clientX-r.left)/r.width*2-1,1-(e.clientY-r.top)/r.height*2),ray=new THREE.Raycaster();
 ray.setFromCamera(mouse,camera);const hit=firstPieceHit(ray.intersectObjects([...assembly.pickables,...(presentationMotion?.pickables||[])]));
 selected=hit?.piece.id||null;update();
 if(compactPanel){if(selected)setPanelMode('inspect');document.querySelector('#copy').disabled=!selected}
 document.querySelector('#selected').textContent=selected?`${model.revision} / #${selected}\n${byId.get(selected).label}\nPart ${byId.get(selected).part} · ${model.colors[byId.get(selected).color][2]}\n${byId.get(selected).module}\n${byId.get(selected).instance_id}`:'Click a piece to inspect its stable reference.';
};
document.querySelector('#copy').onclick=async()=>{await navigator.clipboard.writeText(document.querySelector('#selected').textContent)};
let canvasWidth=canvas.clientWidth,canvasHeight=canvas.clientHeight;
new ResizeObserver(()=>{resizeNotifications++;const width=canvas.clientWidth,height=canvas.clientHeight;if(width===canvasWidth&&height===canvasHeight)return;canvasWidth=width;canvasHeight=height;bufferResizes++;renderer.setSize(width,height,false);camera.aspect=width/height;const center=(camera.left+camera.right)/2,halfWidth=(camera.top-camera.bottom)*camera.aspect/2;camera.left=center-halfWidth;camera.right=center+halfWidth;camera.updateProjectionMatrix();requestRender()}).observe(canvas);
requestRender();
window.inspectPreviewPerformance=()=>({renderedFrames,scheduledFrame:framePending!==null,sceneUpdates,totalUpdateMs,lastUpdateMs,cameraFits,resizeNotifications,bufferResizes,pixelRatio:renderer.getPixelRatio(),calls:renderer.info.render.calls,triangles:renderer.info.render.triangles,geometryCache:true,instancedBatches:assembly.batches.length,decalPatches:(model.decal_surfaces?.length||0)+(model.extra_decal_surfaces?.length||0),decalMeshes:decalGroups.size,decalTriangles,preserveDrawingBuffer:renderer.getContext().getContextAttributes().preserveDrawingBuffer});
window.renderView=({view='front',explode=false,only=null,ids=null,newIds=[],decorations:decorate=true,bands=true,offsets=[],width=1400,height=1000}={})=>{
 capturing=true;
 motionOffsets=new Map(offsets.flatMap(m=>m.ids.map(id=>[id,m.ldraw])));
 hidden.clear();if(only)for(const m of Object.keys(summary.modules))if(!only.includes(m))hidden.add(m);
 visibleIds=ids?new Set(ids):null;highlightIds=new Set(newIds);showDecorations=decorate;showSuspensionBands=bands;
 exploded=explode;selected=null;renderer.setPixelRatio(1);renderer.setSize(width,height,false);camera.aspect=width/height;camera.updateProjectionMatrix();update();fit(view);renderNow();
 const result=renderer.domElement.toDataURL('image/png').split(',')[1];capturing=false;return result;
};
window.previewReady=true;
if(typeof window.capturePreviewInternals==='function')window.capturePreviewInternals({scene,camera,controls,assembly,renderer,renderNow,THREE});
if(model.instruction_plan){
 const steps=model.instruction_plan.steps;
 const panel=document.createElement('section');panel.className=compactPanel?'instruction-controls':'selection';
 panel.innerHTML=compactPanel?
 '<label class="control-label" for="instruction-step">Build step</label><div class="step-navigation"><button id="previous-step" aria-label="Previous step" disabled>←</button><select id="instruction-step"><option value="0">Complete model</option></select><button id="next-step" aria-label="Next step">→</button></div><div class="step-progress"><label for="step">Browse steps</label><output id="step-position" for="step">Complete model</output></div><input id="step" type="range" min="0" max="'+steps.length+'" step="1" value="0" aria-label="Build step"><div id="recipe-navigation" hidden><label class="control-label" for="recipe-frame">Local assembly</label><select id="recipe-frame" aria-label="Local assembly frame"></select><p id="recipe-copy-note"></p></div><div class="step-guidance"><h2 id="step-title" hidden></h2><p id="step-description">Choose a step to begin.</p><section id="step-parts" aria-label="Parts tray" hidden></section><p id="step-hold" hidden></p></div>':
 '<h2>Full build instructions</h2><div style="display:flex;gap:6px"><button id="previous-step">←</button><select id="instruction-step" style="width:100%"><option value="0">Complete model</option></select><button id="next-step">→</button></div><label for="step" style="display:flex;justify-content:space-between;margin-top:14px;font-size:12px">Build steps <output id="step-position" for="step">Complete model</output></label><input id="step" type="range" min="0" max="'+steps.length+'" step="1" value="0" style="width:100%;margin:9px 0" aria-label="Build step"><p id="step-description"></p><p id="step-parts"></p><p id="step-hold" style="color:#98441f"></p><p><a href="instructions.pdf">Instruction PDF</a> · <a href="yangliu-shape.mpd">Model MPD</a><br><a href="inventory.csv">Model inventory</a> · <a href="wanted-list.xml" download>BrickLink XML</a> · <a href="bricklink-inventory.csv">Purchase CSV</a></p><p style="font-size:12px">Wanted list: '+(window.PROTOTYPE.procurement?.purchase_lots??'see XML')+' lots / '+(window.PROTOTYPE.procurement?.purchase_units??'see CSV')+' purchase units. '+(model.physical_audit?'Includes two suspension bands; the steering assembly combines two rigid model components. Any user-excluded purchase parts are listed in the mapping report. Manufactured part/color combinations are catalog-checked. Physical fit remains untested.':'Color availability and physical fit remain under review.')+' <a href="bricklink-mapping.json">Mapping and limits</a> · <a href="digital-fit-audit.md">Digital audit</a> · <a href="sticker-artwork.zip">Sticker pack</a><br><a href="stickers-a4.pdf">A4 print + cut sheet</a> · <a href="stickers-compact.pdf">Compact sheet</a>.</p>';
 (document.querySelector('#build-controls')||document.querySelector('aside')).prepend(panel);
 if(compactPanel){const turn=document.createElement('p');turn.id='model-turn';turn.hidden=true;panel.querySelector('.step-guidance').prepend(turn)}
 if(compactPanel){
  const navigation=document.createElement('div');navigation.id='step-navigation-controls';
  while(panel.firstChild)navigation.append(panel.firstChild);
  const intro=document.createElement('div');intro.id='build-start';
  intro.innerHTML='<h2>Build your own</h2><p>Follow the illustrated steps, with parts trays and local assembly views.</p><button id="start-building">Start building</button>';
  const complete=document.createElement('button');complete.id='show-complete-model';complete.className='quiet-button';complete.textContent='View complete model';navigation.prepend(complete);
  panel.append(intro,navigation);
 }
 const select=panel.querySelector('select'),slider=panel.querySelector('#step'),position=panel.querySelector('#step-position');for(const s of steps){const opt=document.createElement('option');opt.value=s.number;opt.textContent=`${s.number}. ${s.manual.title}`;select.append(opt)}
 let recipeFrame=0,approachFrame=0,sliderFrame=null,sliderTarget=0;
 let instructionCameraMode='overview',mainCameraPhase=null,mainCameraDirection=null;
 const rememberMainCamera=()=>{if(instructionCameraMode==='main')mainCameraDirection=camera.position.clone().sub(controls.target).normalize().toArray()};
 const fitMainInstruction=s=>{
  if(!s){mainCameraPhase=null;mainCameraDirection=null;instructionCameraMode='overview';fit();return}
  const phase=s.manual.view||'front';fit(phase,phase===mainCameraPhase?mainCameraDirection:null);
  mainCameraPhase=phase;instructionCameraMode='main';rememberMainCamera();
 };
 window.inspectInstructionCamera=()=>({mode:instructionCameraMode,phase:mainCameraPhase,direction:camera.position.clone().sub(controls.target).normalize().toArray()});
 const tray=(s,ids,frame=0)=>{
  const host=panel.querySelector('#step-parts');host.replaceChildren();
  if(!s){host.hidden=true;return}
  const title=document.createElement('h3');title.textContent=frame?'Parts for one copy':'Parts in this step';host.append(title);
  const frames=s.manual.instance_frames||s.manual.frames||[];
  const supplied=frame?frames.find(f=>f.number===frame)?.preassembled:s.manual.preassembled;
  if(supplied||(frames.length&&!frame)){
   const card=document.createElement('div');card.className='part-card completed-unit';
   const src=supplied?window.PROTOTYPE.preassembledIcons?.[s.module]:window.PROTOTYPE.recipeIcons?.[s.number];if(src){const image=document.createElement('img');image.src=src;image.alt=supplied?'Preassembled minifigure':'Completed '+(s.manual.unit_name||'local assembly');card.append(image)}
   const name=document.createElement('strong'),copies=supplied?1:s.copies||1;name.textContent=copies+' × '+(supplied?'preassembled minifigure':'completed '+(s.manual.unit_name||'unit')+(copies>1?'s':''));card.append(name);host.append(card);
  }else{
   const lots=new Map();for(const id of ids){const p=byId.get(id),key=p.part+'|'+p.color;const lot=lots.get(key)||{p,key,quantity:0};lot.quantity++;lots.set(key,lot)}
   const list=document.createElement('div');list.className='parts-tray';
   for(const {p,key,quantity}of lots.values()){
    const card=document.createElement('div');card.className='part-card';card.dataset.part=p.part;card.dataset.lot=key;card.dataset.quantity=quantity;
    const src=window.PROTOTYPE.partIcons?.[key];if(src){const image=document.createElement('img');image.src=src;image.alt=p.label;card.append(image)}
    const count=document.createElement('strong');count.textContent=quantity+' ×';card.append(count);
    const name=document.createElement('span');name.textContent=p.label;card.append(name);
    const detail=document.createElement('small');detail.textContent=p.part+' · '+model.colors[p.color][2];card.append(detail);list.append(card);
   }
   host.append(list);
  }
  if(s.manual.catalog_accessory){const note=document.createElement('p');note.textContent=s.manual.catalog_accessory;host.append(note)}
  host.hidden=!ids.length&&!s.manual.catalog_accessory;
 };
 window.setInstructionStep=(n,{render=true}={})=>{rememberMainCamera();if(sliderFrame!==null){cancelAnimationFrame(sliderFrame);sliderFrame=null}n=Math.max(0,Math.min(steps.length,n));select.value=n;slider.value=n;position.textContent=n?`${n} / ${steps.length}`:'Complete model';const s=steps[n-1];
  if(compactPanel){const turn=panel.querySelector('#model-turn');turn.hidden=!s?.manual.turn_model;turn.textContent=s?.manual.turn_model?'↻ '+s.manual.turn_model:''}
  if(!n){mainCameraPhase=null;mainCameraDirection=null;instructionCameraMode='overview'}
  recipeFrame=0;approachFrame=0;motionOffsets.clear();
  visibleIds=s?new Set(s.manual.ids):null;highlightIds=new Set(s?.new_ids||[]);hidden.clear();exploded=false;selected=null;showDecorations=!s||!!s.manual.accessory||!!s.manual.decorations;showSuspensionBands=!s||!!s.manual.bands_installed;if(render){update();fitMainInstruction(s)}
  document.querySelector('#step-description').textContent=s?s.manual.note:`All ${model.pieces.length} rigid parts. Choose a step for construction views.`;
  document.querySelector('#step-hold').textContent=s?.manual.hold?'FIT REVIEW: '+s.manual.hold:'';
  const quantities={};for(const id of s?.new_ids||[]){const p=byId.get(id),key=p.part+' · '+model.colors[p.color][2];quantities[key]=(quantities[key]||0)+1}
  document.querySelector('#step-parts').textContent=s?.manual.catalog_accessory||Object.entries(quantities).map(([p,q])=>`${q} × ${p}`).join(' / ');
  if(compactPanel){
   panel.querySelector('#build-start').hidden=Boolean(n);panel.querySelector('#step-navigation-controls').hidden=!n;
   tray(s,s?.new_ids||[]);
   const frames=s?.manual.instance_frames||s?.manual.frames||[],nav=panel.querySelector('#recipe-navigation'),recipe=panel.querySelector('#recipe-frame');
   nav.hidden=!frames.length;recipe.replaceChildren(new Option('Install completed unit','0'));
   for(const frame of frames){if(s.manual.repeat_prefix_from&&frame.number<=s.manual.repeat_prefix_frames)continue;recipe.add(new Option(`${n}${String.fromCharCode(96+frame.number)}. ${frame.title}`,String(frame.number)))}
   for(const frame of s?.manual.approach_frames||[])recipe.add(new Option(frame.title,'approach-'+frame.number));
   panel.querySelector('#recipe-copy-note').textContent=s?.manual.repeat_prefix_from?`Use the other running board made at step ${s.manual.repeat_prefix_from}, then finish this opposite side.`:s?.repeat_count>1?`Make ${s.repeat_count} identical copies. Local trays show parts for one copy.`:s?.manual.repeat_prefix_count?`Make ${s.manual.repeat_prefix_count} running boards in frames a–d. Finish this side in frames e–g.`:'';
   document.querySelectorAll('[data-module]').forEach(input=>input.checked=true);
   document.querySelector('#explode').checked=false;
   const title=panel.querySelector('#step-title');title.hidden=!s;title.textContent=s?.manual.title||'';
   panel.querySelector('#step-description').textContent=s?s.manual.note:'Choose a step to begin.';
   panel.querySelector('#step-description').hidden=Boolean(s&&!s.manual.note);
   panel.querySelector('#step-hold').hidden=!s?.manual.hold;
   document.querySelector('#previous-step').disabled=n<=1&&!(s?.manual.frames?.length);document.querySelector('#next-step').disabled=n===steps.length;
   document.querySelector('#selected').textContent='Select a piece in the model to see its reference.';document.querySelector('#copy').disabled=true;
  }
  return {step:n,shown:visibleIds?.size||model.pieces.length,newParts:s?.new_ids.length||0};
 };
 if(compactPanel){
  panel.querySelector('#start-building').onclick=()=>{const frames=steps[0].manual.frames||[];window.setInstructionStep(1,{render:!frames.length});if(frames.length)window.setRecipeFrame(frames[0].number)};
  panel.querySelector('#show-complete-model').onclick=()=>window.setInstructionStep(0);
  window.setRecipeFrame=value=>{
   const s=steps[Number(select.value)-1],frames=s?.manual.instance_frames||s?.manual.frames||[],frame=frames.find(f=>f.number===Number(value));
   if(!frame)return window.setInstructionStep(Number(select.value));
   rememberMainCamera();instructionCameraMode='recipe';
   panel.querySelector('#model-turn').hidden=true;
   recipeFrame=frame.number;approachFrame=0;motionOffsets.clear();panel.querySelector('#recipe-frame').value=recipeFrame;
   visibleIds=new Set(frame.shown_ids);highlightIds=new Set(frame.ids);hidden.clear();exploded=false;selected=null;showDecorations=s.module==='tsai';showSuspensionBands=false;
   update();fit(frame.view||s.manual.view||'front');
   panel.querySelector('#step-title').textContent=`${s.number}${String.fromCharCode(96+frame.number)}. ${frame.title}`;
   panel.querySelector('#step-description').hidden=true;panel.querySelector('#step-hold').hidden=true;tray(s,frame.ids,recipeFrame);
   document.querySelector('#previous-step').disabled=s.number===1&&frame.number===(frames[0]?.number||1);
   return{step:s.number,recipeFrame,shown:visibleIds.size,newParts:frame.ids.length};
  };
  window.setApproachFrame=value=>{
   const s=steps[Number(select.value)-1],frame=s?.manual.approach_frames?.find(f=>f.number===Number(value));
   if(!frame)return window.setInstructionStep(Number(select.value));
   rememberMainCamera();instructionCameraMode='approach';
   panel.querySelector('#model-turn').hidden=true;
   recipeFrame=0;approachFrame=frame.number;panel.querySelector('#recipe-frame').value='approach-'+approachFrame;
   visibleIds=new Set(s.manual.ids);highlightIds=new Set(s.new_ids);hidden.clear();exploded=false;selected=null;showDecorations=false;showSuspensionBands=!!s.manual.bands_installed;
   motionOffsets=new Map(frame.offsets.flatMap(m=>m.ids.map(id=>[id,m.ldraw])));update();fit(s.manual.view||'rear');
   panel.querySelector('#step-title').textContent=frame.title;panel.querySelector('#step-description').hidden=true;panel.querySelector('#step-hold').hidden=true;tray(s,s.new_ids);
   document.querySelector('#previous-step').disabled=false;
   return{step:s.number,approachFrame,offsets:frame.offsets};
  };
  panel.querySelector('#recipe-frame').onchange=e=>e.target.value.startsWith('approach-')?window.setApproachFrame(Number(e.target.value.slice(9))):window.setRecipeFrame(Number(e.target.value));
 }
 select.onchange=()=>window.setInstructionStep(Number(select.value));
 slider.oninput=()=>{sliderTarget=Number(slider.value);if(sliderFrame===null)sliderFrame=requestAnimationFrame(()=>{sliderFrame=null;window.setInstructionStep(sliderTarget)})};
 slider.onchange=()=>{if(sliderFrame!==null||Number(select.value)!==Number(slider.value))window.setInstructionStep(Number(slider.value))};
 const localFrames=s=>(s?.manual.instance_frames||s?.manual.frames||[]).filter(f=>!s.manual.repeat_prefix_from||f.number>s.manual.repeat_prefix_frames);
 document.querySelector('#previous-step').onclick=()=>{
  const n=Number(select.value),s=steps[n-1],frames=localFrames(s),approaches=s?.manual.approach_frames||[];
  if(compactPanel&&approachFrame){if(approachFrame>1)return window.setApproachFrame(approachFrame-1);if(frames.length)return window.setRecipeFrame(frames.at(-1).number)}
  else if(compactPanel&&!recipeFrame&&approaches.length)return window.setApproachFrame(approaches.at(-1).number);
  if(compactPanel&&recipeFrame){const index=frames.findIndex(f=>f.number===recipeFrame);if(index>0)return window.setRecipeFrame(frames[index-1].number)}
  else if(compactPanel&&frames.length)return window.setRecipeFrame(frames.at(-1).number);
  window.setInstructionStep(n-1);
 };
 document.querySelector('#next-step').onclick=()=>{
  const n=Number(select.value),s=steps[n-1],frames=localFrames(s),approaches=s?.manual.approach_frames||[];
  if(compactPanel&&approachFrame)return approachFrame<approaches.length?window.setApproachFrame(approachFrame+1):window.setApproachFrame(0);
  if(compactPanel&&recipeFrame){const index=frames.findIndex(f=>f.number===recipeFrame);return index<frames.length-1?window.setRecipeFrame(frames[index+1].number):approaches.length?window.setApproachFrame(approaches[0].number):window.setRecipeFrame(0)}
  const next=steps[n],first=compactPanel&&next?.manual.frames?.length?localFrames(next)[0]:null;
  window.setInstructionStep(n+1,{render:!first});if(first)window.setRecipeFrame(first.number);
 };
 window.inspectInstructions=()=>({steps:steps.length,step:Number(select.value),recipeFrame,approachFrame,slider:Number(slider.value),visible:visibleIds?[...visibleIds].sort((a,b)=>a-b):model.pieces.map(p=>p.id),newIds:highlightIds?[...highlightIds]:[],offsets:[...motionOffsets].map(([id,ldraw])=>({id,ldraw}))});
 if(compactPanel)window.setInstructionStep(0,{render:false});
}
if(compactPanel&&byId.has(400)&&byId.has(254)){
 presentationMotion=createPreviewMotion({scene,assembly,pieces:model.pieces,decorations});
 const button=document.createElement('button');button.id='toggle-animation';button.type='button';document.querySelector('.toolbar').append(button);
 const label=()=>{button.textContent=animationEnabled?'Pause animation':'Play animation';button.setAttribute('aria-pressed',String(animationEnabled));button.title='Flags, tires, walking, waving and slow camera orbit; paused during building'};
 const setEnabled=value=>{animationEnabled=Boolean(value);if(animationEnabled)motionEngaged=true;lastMotionFrame=null;label();update()};
 button.onclick=()=>setEnabled(!animationEnabled);
 reducedMotion.addEventListener('change',e=>setEnabled(!e.matches));
 document.addEventListener('visibilitychange',()=>{lastMotionFrame=null;if(!document.hidden)requestRender()});
 new IntersectionObserver(([entry])=>{canvasInView=entry.isIntersecting;lastMotionFrame=null;if(canvasInView)requestRender()}).observe(canvas);
 window.setPreviewAnimation=setEnabled;
 window.inspectPreviewAnimation=()=>({enabled:animationEnabled,running:Boolean(motionRunning()),reducedMotion:reducedMotion.matches,camera:camera.position.toArray(),target:controls.target.toArray(),...presentationMotion.inspect()});
 label();update();
}
