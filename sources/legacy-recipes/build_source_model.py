"""Photo-based source reconstruction in metres, independent of LEGO geometry."""
import bpy, math, json, hashlib
from mathutils import Vector
from pathlib import Path
H=Path(__file__).resolve().parent;OUT=H/'sources/model-v1';OUT.mkdir(parents=True,exist_ok=True)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
scene=bpy.context.scene;scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1
def mat(name,color,metal=0,rough=.45):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough;return m
brown=mat('Wood wrap - dusty reddish brown',(.32,.16,.12));black=mat('Black trim',(.025,.033,.042));rubber=mat('Tyre rubber',(.016,.021,.027),0,.8)
white=mat('White campaign framework',(.91,.92,.87));silver=mat('Aluminium and machined wheels',(.39,.45,.49),.7,.28)
red=mat('Orange red fabric',(.8,.10,.045));rope=mat('Cream natural rope',(.66,.57,.39));wood=mat('Helm timber',(.24,.075,.021),0,.3)
orange=mat('Campaign orange',(.93,.25,.12));lamp=mat('Headlamp lenses',(.73,.85,.89),.4,.2)
glass=mat('Smoked blue glazing',(.11,.21,.27),.15,.18);glass.node_tree.nodes.get('Principled BSDF').inputs['Alpha'].default_value=.43;glass.surface_render_method='DITHERED'
def tag(o,module,evidence='inferred from photographs'):
 o['module']=module;o['evidence']=evidence;o['source_model_revision']='source-v1';return o
def bevel(o,width=.03):
 m=o.modifiers.new('Soft manufactured edges','BEVEL');m.width=width;m.segments=3
 o.modifiers.new('Weighted normals','WEIGHTED_NORMAL');return o
def cube(name,loc,size,material,module,bev=.02):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.dimensions=size;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(material);tag(o,module)
 if bev:bevel(o,bev)
 return o
def cyl(name,a,b,r,material,module,vertices=40):
 a,b=Vector(a),Vector(b);delta=b-a;bpy.ops.mesh.primitive_cylinder_add(vertices=vertices,radius=r,depth=delta.length,location=(a+b)/2);o=bpy.context.object;o.name=name;o.rotation_euler=delta.to_track_quat('Z','Y').to_euler();o.data.materials.append(material);tag(o,module)
 for p in o.data.polygons:p.use_smooth=True
 return o
def path(name,points,r,material,module):
 c=bpy.data.curves.new(name,'CURVE');c.dimensions='3D';c.bevel_depth=r;c.bevel_resolution=3;s=c.splines.new('POLY');s.points.add(len(points)-1)
 for p,v in zip(s.points,points):p.co=(*v,1)
 o=bpy.data.objects.new(name,c);scene.collection.objects.link(o);o.data.materials.append(material);tag(o,module);return o
def mesh(name,verts,faces,material,module,solid=0):
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(name,me);scene.collection.objects.link(o);o.data.materials.append(material);tag(o,module)
 if solid:s=o.modifiers.new('Panel thickness','SOLIDIFY');s.thickness=solid
 return o
def panel(name,verts,material,module,thick=.02):return mesh(name,verts,[list(range(len(verts)))],material,module,thick)
def torus(name,center,major,minor,material,module,rot=(math.pi/2,0,0)):
 bpy.ops.mesh.primitive_torus_add(major_radius=major,minor_radius=minor,major_segments=64,minor_segments=16,location=center,rotation=rot);o=bpy.context.object;o.name=name;o.data.materials.append(material);tag(o,module)
 for p in o.data.polygons:p.use_smooth=True
 return o
def decal(name,verts,art,module):
 m=bpy.data.materials.new(name+' artwork');m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');im=bpy.data.images.load(str(H/'sources/artwork-v1'/f'{art}.png'));im.pack();t=m.node_tree.nodes.new('ShaderNodeTexImage');t.image=im;m.node_tree.links.new(t.outputs['Color'],p.inputs['Base Color']);p.inputs['Roughness'].default_value=.55
 o=panel(name,verts,m,module,0);uv=o.data.uv_layers.new(name='Artwork UV')
 for poly in o.data.polygons:
  for loop,co in zip(poly.loop_indices,[(0,0),(1,0),(1,1),(0,1)]):uv.data[loop].uv=co
 return o

# Ford T6-generation double cab envelope; axle spacing is the dimensional anchor.
body=cube('Pickup lower body shell',(0,0,.94),(5.25,1.82,.72),brown,'body',.07)
for x in [-1.72,1.50]:
 cutter=cyl('temporary wheel-well cutter',(x,-1.15,.405),(x,1.15,.405),.465,black,'temporary',64)
 mod=body.modifiers.new('Real wheel arch void','BOOLEAN');mod.object=cutter;mod.operation='DIFFERENCE';bpy.context.view_layer.objects.active=body
 bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cutter,do_unlink=True)
 for s in [-1,1]:
  y=s*.825
  torus('All terrain tyre',(x,y,.405),.302,.101,rubber,'wheels')
  cyl('Alloy wheel barrel',(x,y-s*.09,.405),(x,y+s*.11,.405),.226,silver,'wheels')
  cyl('Recessed hub',(x,y+s*.112,.405),(x,y+s*.121,.405),.184,black,'wheels')
  for k in range(6):
   a=k*math.tau/6;cyl('Machined wheel spoke',(x+.065*math.sin(a),y+s*.128,.405+.065*math.cos(a)),(x+.213*math.sin(a+.1),y+s*.13,.405+.213*math.cos(a+.1)),.021,silver,'wheels',12)
  cyl('Wheel centre cap',(x,y+s*.13,.405),(x,y+s*.145,.405),.067,silver,'wheels')
  # The white flare follows the cut-out instead of crossing the wheel opening.
  pts=[(x+.481*math.cos(a),s*.936,.405+.481*math.sin(a)) for a in [math.pi*i/48 for i in range(49)]]
  path('White wheel-arch flare',pts,.044,white,'body')
  for k in range(48):
   a=k*math.tau/48
   o=cube('Tyre tread',(x+.398*math.sin(a),y,.405+.398*math.cos(a)),(.038,.17,.018),rubber,'wheels',.005);o.rotation_euler[1]=a
cube('Chassis and undertray',(0,0,.43),(4.66,1.22,.17),black,'body')
# Drop the front shell beneath the sloping hood, preserving the visible hood wrap.
cutter=cube('temporary hood clearance',(2.02,0,1.44),(1.50,2.4,.60),black,'temporary',0)
mod=body.modifiers.new('Hood underside clearance','BOOLEAN');mod.object=cutter;mod.operation='DIFFERENCE';bpy.context.view_layer.objects.active=body
bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cutter,do_unlink=True)
# Hollow cabin and bed: the source vehicle has real interior volumes.
for name,loc,size in [('Cabin cavity',(.20,0,1.215),(2.15,1.60,.55)),('Cargo bed cavity',(-1.75,0,1.20),(1.55,1.60,.48))]:
 cutter=cube('temporary '+name,loc,size,black,'temporary',0)
 mod=body.modifiers.new(name,'BOOLEAN');mod.object=cutter;mod.operation='DIFFERENCE';bpy.context.view_layer.objects.active=body
 bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cutter,do_unlink=True)
for s in [-1,1]:cube('Running board',(-.05,s*.99,.47),(2.38,.17,.085),black,'body')

# Hood, proper sloping windshield, framed side windows, double-cab doors.
hood=mesh('Sculpted hood',[(1.27,-.87,1.30),(2.58,-.83,1.19),(2.58,.83,1.19),(1.27,.87,1.30),
 (1.27,-.87,1.23),(2.58,-.83,1.13),(2.58,.83,1.13),(1.27,.87,1.23)],[(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)],orange,'body');bevel(hood,.025)
decal('Hood campaign wrap',[(2.52,-.80,1.204),(2.52,.80,1.204),(1.31,.84,1.307),(1.31,-.84,1.307)],'hood','decals')
cube('Cab roof',(-.04,0,1.794),(1.82,1.50,.075),brown,'cab-roof',.07)
front=[(1.39,-.84,1.31),(1.39,.84,1.31),(.86,.72,1.775),(.86,-.72,1.775)]
panel('Sloping front windshield',front,glass,'glazing',.009)
path('Windshield rubber surround',front+[front[0]],.022,black,'glazing')
for s in [-1,1]:
 pts=[(-.92,s*.88,1.29),(1.36,s*.88,1.29),(.84,s*.745,1.75),(-.76,s*.745,1.75)]
 panel('Double-cab side glazing',pts,glass,'glazing',.008);path('Side glass surround',pts+[pts[0]],.026,black,'body')
 for x in [-.84,.10]:cyl('Cab pillar',(x,s*.886,1.29),(x+.03,s*.75,1.75),.033,brown,'body')
 for x in [-.87,.12,1.32]:path('Door seam',[(x,s*.916,.63),(x,s*.923,1.23)],.004,black,'body')
 path('Door sill seam',[(-.87,s*.921,.63),(1.35,s*.921,.63)],.004,black,'body')
 for x in [-.58,.98]:cube('Door handle',(x,s*.949,1.17),(.18,.035,.04),black,'body',.018)
 cyl('Side mirror stalk',(1.19,s*.88,1.35),(1.19,s*1.075,1.38),.027,black,'body')
 cube('Side mirror',(1.19,s*1.10,1.40),(.25,.16,.17),black,'body',.045)
panel('Cab rear window',[(-.94,-.70,1.33),(-.94,.70,1.33),(-.82,.68,1.73),(-.82,-.68,1.73)],glass,'glazing',.01)

# Interior, with accessible roof and separate driver/passenger seats.
cube('Cab floor',(.10,0,.91),(2.16,1.58,.09),black,'interior')
for x in [.32,-.58]:
 for y in [-.43,.43]:
  cube('Driver seat cushion' if x>.0 and y<0 else 'Passenger seat cushion',(x,y,1.025),(.46,.46,.13),black,'interior',.055)
  o=cube('Padded seat back',(x-.20,y,1.28),(.14,.47,.52),black,'interior',.055);o.rotation_euler[1]=-.10
  cube('Headrest',(x-.22,y,1.58),(.13,.28,.16),black,'interior',.045)
cube('Dashboard',(1.06,0,1.25),(.35,1.52,.17),black,'interior',.05)
cyl('Steering column',(.83,-.43,1.14),(.71,-.43,1.36),.03,black,'interior')
torus('Driver steering wheel',(.71,-.43,1.36),.145,.018,black,'interior',(0,math.pi/2-.38,0))
cube('Centre console',(.28,0,1.02),(.68,.15,.21),black,'interior')
cyl('Gear selector',(.56,0,1.12),(.56,0,1.24),.019,silver,'interior')

# Recognizable Ranger front mask, grille mesh, lamps, and bumper.
cube('Front bumper',(2.58,0,.66),(.20,1.87,.31),black,'body',.09)
cube('Silver skid plate',(2.68,0,.48),(.045,1.02,.105),silver,'body',.025)
cube('Front grille surround',(2.665,0,1.01),(.08,1.08,.41),silver,'body',.11)
cube('Black grille opening',(2.712,0,1.01),(.035,.96,.32),black,'body',.095)
for y in [-.38,-.25,-.12,.01,.14,.27,.40]:cube('Grille vertical mesh',(2.735,y,1.01),(.014,.014,.27),silver,'body',.003)
for z in [.94,1.06]:cube('Grille crossbar',(2.747,0,z),(.023,.88,.038),black,'body',.01)
for s in [-1,1]:
 cube('Headlamp housing',(2.626,s*.705,1.09),(.10,.43,.245),black,'body',.06)
 cube('Headlamp clear lens',(2.687,s*.705,1.10),(.025,.375,.19),lamp,'body',.045)
 cyl('Projector headlamp',(2.70,s*.67,1.1),(2.72,s*.67,1.1),.068,silver,'body')
 cube('Lower fog lamp',(2.68,s*.68,.70),(.034,.27,.10),lamp,'body',.025)
cube('Front campaign plate',(2.732,0,.73),(.018,.40,.19),orange,'body',.01)
decal('Front plate lettering',[(2.745,-.195,.64),(2.745,.195,.64),(2.745,.195,.82),(2.745,-.195,.82)],'plate','decals')
cube('Tailgate',(-2.63,0,1.015),(.075,1.79,.55),brown,'body',.03)
for s in [-1,1]:cube('Tail lamp',(-2.677,s*.79,1.03),(.035,.17,.34),red,'body',.03)
cube('Rear bumper',(-2.67,0,.59),(.13,1.9,.14),black,'body')

# Wood wrap slat pattern; individual seams remain visible in the source model.
for s in [-1,1]:
 for z in [.65,.73,.81,.89,.97,1.05,1.13,1.21]:
  for a,b in [(-2.56,-2.18),(-1.25,1.04),(1.97,2.49)]:path('Wood wrap horizontal grain',[(a,s*.918,z),(b,s*.918,z+.003)],.0035,wood,'decals')

# Bed standing floor and roof-height removable campaign framework.
cube('Cargo bed platform floor',(-1.73,0,.99),(1.67,1.61,.07),wood,'platform')
for s in [-1,1]:
 for x in [-2.52,-.96]:cyl('Campaign platform upright',(x,s*.91,1.05),(x,s*.91,1.85),.035,white,'platform')
 cube('White upper side rail',(-1.74,s*.91,1.80),(1.64,.10,.16),white,'platform',.015)
 for z in [1.42,1.52,1.62]:cube('Ship-style side cladding',(-1.74,s*.899,z),(1.57,.035,.078),rope,'platform',.005)
cube('Upper front rail and speaker shelf',(.10,0,1.855),(2.20,1.89,.10),white,'roof-rack',.035)
# Open rear footwell is preserved; the roof rack is above the cab, not the bed.
for s in [-1,1]:
 torus('Red life ring',(-1.92,s*.98,1.33),.235,.043,red,'life-rings')
 for a in [0,math.pi/2,math.pi,math.pi*1.5]:
  pts=[(-1.92+.235*math.cos(t),s*1.025,1.33+.235*math.sin(t)) for t in [a-.14+i*.028 for i in range(11)]]
  path('Life ring white binding',pts,.048,white,'life-rings')
 # Thick perimeter rope follows hood and bed gunwale.
 path('Perimeter nautical rope',[(-2.56,s*.95,1.28),(-1.1,s*.95,1.29),(1.35,s*.93,1.30),(2.53,s*.84,1.21)],.026,rope,'rigging')
path('Front perimeter rope',[(2.53,-.84,1.21),(2.63,0,1.20),(2.53,.84,1.21)],.026,rope,'rigging')

# Ship wheel and pedestal, kept as an independent removable module.
cube('Helm pedestal',(-.70,0,1.70),(.25,.24,.80),wood,'helm',.035)
torus('Wooden ship helm',(-.40,0,2.06),.305,.031,wood,'helm',(0,math.pi/2,0))
cyl('Helm axle',(-.72,0,2.06),(-.34,0,2.06),.048,wood,'helm')
for k in range(8):
 a=k*math.tau/8;cyl('Helm spoke and handle',(-.38,0,2.06),(-.38,.39*math.sin(a),2.06+.39*math.cos(a)),.019,wood,'helm',20)
for s in [-1,1]:
 cube('PA speaker enclosure',(1.03,s*.74,2.015),(.21,.32,.25),black,'speakers',.045)
 cyl('Speaker cone',(1.14,s*.74,2.015),(1.151,s*.74,2.015),.084,black,'speakers')

# Launch mast and triangular sail, plus a tall narrow aft banner.
for name,x,y,base,top in [('aft-banner',-2.38,-.85,1.78,3.62),('forward-sail',.54,-.85,1.88,3.08)]:
 cyl(name+' aluminium mast',(x,y,base),(x,y,top),.018,silver,name)
 if name=='aft-banner':
  verts=[(x+.035,y,2.02),(x+.59,y,2.02),(x+.59,y,3.57),(x+.035,y,3.57)]
  decal('Tall 洋流 banner',verts,'banner',name)
  path('Banner lower spar',[(x,y,2.02),(x+.62,y,2.02)],.013,silver,name)
 else:
  panel('Triangular red launch sail',[(x+.025,y,3.02),(x+.025,y,1.98),(x+.89,y,1.98)],red,name,.004)
  # Small rectangular emblem is on the triangular cloth, clear of its edge.
  decal('Sail 順 emblem',[(x+.045,y-.006,2.02),(x+.37,y-.006,2.02),(x+.37,y-.006,2.40),(x+.045,y-.006,2.40)],'sail',name)
  path('Sail lower spar',[(x,y,1.97),(x+.92,y,1.97)],.015,silver,name)
 path(name+' guy rope',[(x,y,top),(x+.94,y+.09,base)],.009,rope,'rigging')

# Light kit seen on the later road setup; optional and separately selectable.
for s in [-1,1]:
 cyl('Road light stand',(-1.58,s*.76,1.04),(-1.58,s*.76,2.50),.018,silver,'road-light-kit')
cube('Road light crossbar',(-1.58,0,2.50),(.035,1.55,.035),silver,'road-light-kit')
for s in [-1,1]:cube('Road LED panel',(-1.58,s*.57,2.49),(.065,.33,.19),lamp,'road-light-kit',.012)
for o in bpy.data.objects:
 if o.get('module')=='road-light-kit':o.hide_render=True

# Studio setup and deterministic complementary source-model views.
scene.render.engine='CYCLES';scene.cycles.samples=32;scene.cycles.use_denoising=True
scene.render.resolution_x=1500;scene.render.resolution_y=1050;scene.render.resolution_percentage=100
scene.world.color=(.65,.65,.65);scene.view_settings.view_transform='AgX'
floor=mat('Studio floor',(.73,.71,.66),0,.9);cube('Studio ground',(0,0,-.055),(200,200,.1),floor,'studio',0)
for name,loc,energy,size in [('Key',(2,-5,8),1500,6),('Fill',(-4,3,6),1100,5),('Rim',(5,4,5),900,4)]:
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.name=name;o.data.energy=energy;o.data.shape='DISK';o.data.size=size;o.rotation_euler=(Vector((0,0,1.2))-o.location).to_track_quat('-Z','Y').to_euler();tag(o,'studio')
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Review camera';cam.data.type='ORTHO';scene.camera=cam
def view(name,loc,target=(0,0,1.7),scale=7.2):
 cam.location=loc;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=scale;scene.render.filepath=str(OUT/(name+'.png'));bpy.ops.render.render(write_still=True)

# Save the authoring model and an independent mesh export for the next adapter.
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'yangliu-source-v1.blend'))
objects=[o for o in scene.objects if o.get('module') not in ['studio','temporary'] and o.type in ['MESH','CURVE']]
bpy.ops.object.select_all(action='DESELECT')
for o in objects:o.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(OUT/'yangliu-source-v1.glb'),export_format='GLB',use_selection=True,export_extras=True,export_apply=True)
depsgraph=bpy.context.evaluated_depsgraph_get();parts=[]
for o in objects:
 e=o.evaluated_get(depsgraph);me=e.to_mesh();me.calc_loop_triangles()
 parts.append(dict(name=o.name,role=o['module'],evidence=o['evidence'],vertices=[list(o.matrix_world@v.co) for v in me.vertices],triangles=[list(t.vertices) for t in me.loop_triangles]))
 e.to_mesh_clear()
(OUT/'source-geometry.json').write_text(json.dumps(dict(revision='source-v1',units='metres',orientation='X forward, Y left, Z up',
 nominal_vehicle_dimensions_m=[5.362,1.860,1.821],wheelbase_m=3.220,parts=parts),separators=(',',':')))
view('front',(7,-8,5));view('rear',(-7,7,4.5))
for o in objects:
 if o.get('module') in ['cab-roof','roof-rack','speakers','forward-sail','aft-banner','rigging','glazing']:o.hide_render=True
view('interior',(4,-5,5),(.3,0,1.25),4.0)
for o in objects:
 if o.get('module') in ['cab-roof','roof-rack','speakers','forward-sail','aft-banner','rigging','glazing']:o.hide_render=False
view('side',(0,-10,3.1),(0,0,1.65),6.4)
print('SOURCE_MODEL_READY',len(objects),str(OUT))
