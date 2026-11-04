"""Update source artwork/material transparency while preserving every mesh and pose."""
import bpy,hashlib,json
from pathlib import Path
H=Path(__file__).resolve().parent;REV='v10';OUT=H/('sources/donor-campaign-'+REV);OUT.mkdir(exist_ok=True)
SOURCE=H/'sources/donor-campaign-v1/yangliu-donor-v1.blend';bpy.ops.wm.open_mainfile(filepath=str(SOURCE))
def geometry_hash():
 rows=[]
 for o in bpy.context.scene.objects:
  if o.type=='MESH':rows.append([o.name,[list(v.co) for v in o.data.vertices],[list(r) for r in o.matrix_world]])
 return hashlib.sha256(json.dumps(sorted(rows),separators=(',',':')).encode()).hexdigest()
before=geometry_hash();changes=[]
for o in bpy.context.scene.objects:
 role=o.get('module','')
 art='hood-band.png' if o.get('modification_id')=='14-hood-decal' else ('banner.png' if role=='aft-banner' else ('wedge-tile.png' if role=='forward-sail' else None))
 if not art:continue
 for slot in o.material_slots:
  original=slot.material
  if not original or not original.use_nodes:continue
  if not any(n.type=='TEX_IMAGE' for n in original.node_tree.nodes):continue
  m=original.copy();slot.material=m;nodes=m.node_tree.nodes;links=m.node_tree.links;p=nodes.get('Principled BSDF')
  textures=[n for n in nodes if n.type=='TEX_IMAGE']
  for t in textures:t.image=bpy.data.images.load(str(H/('sources/artwork-'+REV)/art),check_existing=True);t.image.pack()
  alpha=textures[0].outputs['Alpha']
  if len(textures)>1:
   geometry=next((n for n in nodes if n.type=='NEW_GEOMETRY'),None) or nodes.new('ShaderNodeNewGeometry')
   switch=nodes.new('ShaderNodeMixRGB');links.new(geometry.outputs['Backfacing'],switch.inputs[0]);links.new(textures[0].outputs['Alpha'],switch.inputs[1]);links.new(textures[1].outputs['Alpha'],switch.inputs[2]);alpha=switch.outputs[0]
  if role=='aft-banner':
   # The source banner is a single cloth plane. Composite transparent ink over
   # its red fabric material, rather than cutting holes through the fabric.
   color=p.inputs['Base Color'].links[0].from_socket if p.inputs['Base Color'].is_linked else textures[0].outputs['Color']
   mix=nodes.new('ShaderNodeMixRGB');mix.inputs[1].default_value=(.8,.10,.045,1);links.new(alpha,mix.inputs[0]);links.new(color,mix.inputs[2]);links.new(mix.outputs[0],p.inputs['Base Color'])
   for link in list(p.inputs['Alpha'].links):links.remove(link)
   p.inputs['Alpha'].default_value=1;mode='Ink composited over source red cloth material'
  else:
   links.new(alpha,p.inputs['Alpha']);m.surface_render_method='DITHERED';mode='Transparent decal over existing hood or sail geometry'
  changes.append(dict(object=o.name,role=role,artwork=art,transparency=mode))
assert changes and before==geometry_hash()
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/('yangliu-source-'+REV+'.blend')))
(OUT/'artwork-modification-log.json').write_text(json.dumps(dict(source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),geometry_sha256_before=before,geometry_sha256_after=geometry_hash(),changes=changes,artwork_revision='artwork-'+REV,scope='Artwork and alpha/material composition only. No mesh or pose changes.'),indent=2)+'\n')
s=bpy.context.scene;s.render.resolution_x=1200;s.render.resolution_y=850;s.render.resolution_percentage=100
if hasattr(s,'cycles'):s.cycles.samples=24
s.render.filepath=str(OUT/'front.png');bpy.ops.render.render(write_still=True)
