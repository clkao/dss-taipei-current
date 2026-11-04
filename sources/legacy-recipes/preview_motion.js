import * as THREE from 'three';

// Display-only rigs reuse catalog geometry and materials. No model records,
// assembly matrices, bounds, or instruction poses are changed per frame.
export function createPreviewMotion({scene,assembly,pieces,decorations}){
 const byId=new Map(pieces.map(p=>[p.id,p])),ids=new Set(),pickables=[],rigs=[],hosts=new Map();
 const root=new THREE.Group();scene.add(root);root.visible=false;
 const matrix=id=>assembly.matrix(byId.get(id));
 const origin=id=>new THREE.Vector3().setFromMatrixPosition(matrix(id));
 const axis=(id,v)=>new THREE.Vector3(...v).transformDirection(matrix(id));
 const rig=(pivot=new THREE.Vector3(),parent=root)=>{const group=new THREE.Group();group.position.copy(pivot);parent.add(group);rigs.push(group);return{group,pivot}};
 function add(id,host,component=null){
  const piece=byId.get(id);if(!piece)return;
  ids.add(id);hosts.set(id,host);
  const batches=assembly.batches.filter(b=>b.pieces.some(p=>p.id===id));
  const partId=assembly.placements.get(id).part,part=assembly.parts.get(partId);
  for(let i=0;i<part.meshes.length;i++){
   if(component!==null&&i!==component)continue;
   const mesh=new THREE.Mesh(part.meshes[i].geometry,batches[i].mesh.material);
   mesh.matrixAutoUpdate=false;mesh.matrix.copy(matrix(id)).premultiply(new THREE.Matrix4().makeTranslation(...host.pivot.clone().negate().toArray()));
   mesh.userData.piece=piece;host.group.add(mesh);pickables.push(mesh);
   // Catalog edge arrays follow the same submesh boundaries, including hips/legs.
   const edges=assembly.catalog.parts[partId].edges[i];if(edges){const geometry=new THREE.BufferGeometry();geometry.setAttribute('position',new THREE.Float32BufferAttribute(edges,3));const lines=new THREE.LineSegments(geometry,assembly.outlines.material);lines.matrixAutoUpdate=false;lines.matrix.copy(mesh.matrix);host.group.add(lines)}
  }
 }
 const rims=pieces.filter(p=>p.part==='55981');
 const wheels=pieces.filter(p=>p.part==='92402').map(tire=>{
  const center=origin(tire.id),rim=rims.reduce((a,b)=>origin(a.id).distanceToSquared(center)<origin(b.id).distanceToSquared(center)?a:b);
  const r=rig(origin(rim.id));add(rim.id,r);add(tire.id,r);return{...r,ids:[rim.id,tire.id]};
 });
 const flags=[266,267].filter(id=>byId.has(id)).map(id=>{const r=rig(origin(id));add(id,r);return r});
 const sail=rig(new THREE.Vector3(9.5,13.02,-3.5));for(const id of [302,303,304,305,306])add(id,sail);
 const wave=rig(origin(257));for(const id of [257,259])add(id,wave);const shoulderAxis=axis(256,[1,0,0]);
 const walker=new THREE.Group();root.add(walker);walker.matrixAutoUpdate=false;
 const body=rig(new THREE.Vector3(),walker);
 for(const id of [401,406,407])add(id,body);
 const hip=rig(new THREE.Vector3(),walker);add(400,hip,0);
 const hipPivot=new THREE.Vector3(0,12,0).applyMatrix4(matrix(400));
 const legs=[1,2].map(component=>{const r=rig(hipPivot,walker);add(400,r,component);return r});
 const legAxis=axis(400,[1,0,0]);
 const freeArm=rig(origin(402),walker);for(const id of [402,404])add(id,freeArm);
 const bannerArm=rig(origin(403),walker);for(const id of [403,405,408,409])add(id,bannerArm);
 const walkingCenter=origin(400),translation=new THREE.Matrix4(),rotation=new THREE.Matrix4(),negativeCenter=new THREE.Matrix4().makeTranslation(...walkingCenter.clone().negate().toArray());
 let shown=false,time=0;
 const animatedDecorations=decorations.filter(o=>hosts.has(o.userData.pieceId));
 function pose(seconds){
  time=seconds;
  // The vehicle faces +X: rolling forward requires a negative world-Z spin.
  wheels.forEach(r=>r.group.rotation.z=-time*.7);
  flags.forEach((r,i)=>r.group.rotation.y=.14*Math.sin(time*1.9+i*.8));
  sail.group.rotation.y=.1*Math.sin(time*1.6+.3);
  wave.group.quaternion.setFromAxisAngle(shoulderAxis,3.65+.3*Math.sin(time*3.4));
  const stride=Math.sin(time*4.8);
  translation.makeTranslation(walkingCenter.x,walkingCenter.y+.06*Math.abs(stride),walkingCenter.z);
  rotation.identity();walker.matrix.copy(translation).multiply(rotation).multiply(negativeCenter);
  legs.forEach((r,i)=>r.group.quaternion.setFromAxisAngle(legAxis,.42*stride*(i?-1:1)));
  freeArm.group.quaternion.setFromAxisAngle(legAxis,-.23*stride);
  bannerArm.group.quaternion.setFromAxisAngle(legAxis,.1*stride);
  root.updateMatrixWorld(true);
  for(const o of animatedDecorations){const host=hosts.get(o.userData.pieceId);o.matrixAutoUpdate=false;o.matrix.copy(host.group.matrixWorld).multiply(new THREE.Matrix4().makeTranslation(...host.pivot.clone().negate().toArray()));o.matrixWorldNeedsUpdate=true}
 }
 function sync(active,hidden){
  shown=active;root.visible=active;
  for(const o of pickables)o.parent.visible=!hidden.has(o.userData.piece.module);
  if(active)pose(time);
  else for(const o of animatedDecorations){o.matrixAutoUpdate=true;o.position.set(0,0,0);o.quaternion.identity();o.scale.set(1,1,1);o.updateMatrix()}
 }
 return{ids,pickables,pose,sync,get shown(){return shown},inspect:()=>({time,shown,animatedIds:[...ids],rigs:rigs.length,meshCount:pickables.length,walkingLegComponents:2,walkingHeading:0,walkingPosition:walkingCenter.toArray(),wheels:wheels.map(r=>({ids:r.ids,angle:r.group.rotation.z,center:r.pivot.toArray()}))})};
}
