"""Replay campaign changes against a donor profile without editing either source.

Blender --background --python replay_campaign.py -- [--profile relative.json]
    [--out sources/donor-campaign-v1] [--skip-render]
"""
import argparse
import hashlib
import json
import math
import sys
from pathlib import Path
import bpy
from mathutils import Matrix, Vector
from mathutils.bvhtree import BVHTree

H = Path(__file__).resolve().parent
ap = argparse.ArgumentParser()
ap.add_argument('--profile', default='design/donor-profiles/public-ranger-v1.json')
ap.add_argument('--out', default='sources/donor-campaign-v1')
ap.add_argument('--skip-render', action='store_true')
args = ap.parse_args(sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else [])
profile = json.loads((H / args.profile).read_text())
recipe_path = H / 'design/campaign-modifications.json'
recipe = json.loads(recipe_path.read_text())
OUT = H / args.out
OUT.mkdir(parents=True, exist_ok=True)
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert sha(H / profile['base_blend']) == profile['base_sha256'], 'Donor file changed; review profile'
assert sha(H / recipe['source_blend']) == recipe['source_sha256'], 'Module source changed; review recipe'
bpy.ops.wm.open_mainfile(filepath=str(H / profile['base_blend']))
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.scale_length = 1
donor = [o for o in scene.objects if o.get('donor_source')]
for o in donor:
    o['module'] = 'wheels' if o.name.startswith('Wheel ') else 'glazing' if 'blinn2' in o.name else 'cab-roof' if profile['selectors']['roof'] in o.name else 'body'
    o['evidence'] = 'Existing donor geometry, retained for approved V1 base'
    o['modification_id'] = '00-original-donor'
    o['source_model_revision'] = recipe['revision']
with bpy.data.libraries.load(str(H / recipe['source_blend']), link=False) as (src, dst):
    dst.objects = src.objects
assets = [o for o in dst.objects if o]

def frame_matrix(key):
    f = profile['frames'][key]
    return Matrix.Translation(Vector(f['target_origin'])) @ Matrix.Diagonal((*f['scale'], 1)) @ Matrix.Translation(-Vector(f['source_origin']))

def snapshot(o):
    return {'name': o.name, 'module': o.get('module'), 'matrix': [list(row) for row in o.matrix_world]}

def image_material(original, texture='sources/donor-campaign-v1/wood-wrap-atlas.png'):
    m = original.copy()
    m.name = 'Campaign wood wrap / original UV atlas'
    for n in m.node_tree.nodes:
        if n.type == 'TEX_IMAGE':
            n.image = bpy.data.images.load(str(H / texture), check_existing=True)
            n.image.pack()
    return m

def readable_flag_material(material):
    """Read lettering on both faces instead of mirroring a single UV print."""
    m = material.copy()
    nodes, links = m.node_tree.nodes, m.node_tree.links
    textures = [n for n in nodes if n.type == 'TEX_IMAGE']
    if not textures:
        return m
    texture = textures[0]
    reverse = nodes.new('ShaderNodeTexImage')
    reverse.image = texture.image
    uv = nodes.new('ShaderNodeTexCoord')
    flip = nodes.new('ShaderNodeVectorMath')
    flip.operation = 'MULTIPLY_ADD'
    flip.inputs[1].default_value = (-1, 1, 1)
    flip.inputs[2].default_value = (1, 0, 0)
    links.new(uv.outputs['UV'], flip.inputs[0])
    links.new(flip.outputs[0], reverse.inputs['Vector'])
    geometry = nodes.new('ShaderNodeNewGeometry')
    mix = nodes.new('ShaderNodeMixRGB')
    links.new(geometry.outputs['Backfacing'], mix.inputs[0])
    links.new(texture.outputs['Color'], mix.inputs[1])
    links.new(reverse.outputs['Color'], mix.inputs[2])
    links.new(mix.outputs[0], nodes.get('Principled BSDF').inputs['Base Color'])
    return m

applied = []
imported = []
replaced = []
for op in recipe['operations']:
    record = {'id': op['id'], 'type': op['type'], 'description': op['description'], 'objects': []}
    if op.get('enabled') is False:
        record['skipped'] = 'superseded by ' + op.get('superseded_by', 'recipe setting')
        applied.append(record)
        continue
    if op['type'] == 'paint_atlas':
        tokens = profile['selectors'][op['selector']]
        cache = {}
        for o in donor:
            if not any(t in o.name for t in tokens):
                continue
            for slot in o.material_slots:
                key = slot.material.name
                if key not in cache:
                    cache[key] = image_material(slot.material,op.get('texture_override','sources/donor-campaign-v1/wood-wrap-atlas.png'))
                slot.material = cache[key]
            o['modification_id'] = op['id']
            record['objects'].append(snapshot(o))
    elif op['type'] == 'paint_solid':
        material = bpy.data.materials.new(op['material_name'])
        material.use_nodes = True
        shader = material.node_tree.nodes.get('Principled BSDF')
        shader.inputs['Base Color'].default_value = (*op['color'], 1)
        shader.inputs['Roughness'].default_value = .28
        for o in donor:
            if profile['selectors'][op['selector']] not in o.name:
                continue
            o.data.materials.clear()
            o.data.materials.append(material)
            o['modification_id'] = op['id']
            record['objects'].append(snapshot(o))
    elif op['type'] == 'smooth_flares':
        assert sha(H/op['generator']) == op['generator_sha256'], 'Flare generator changed; review recipe'
        sys.path.insert(0,str(H))
        from smooth_flares import build
        made = build(scene,profile,op,H)
        imported.extend(made)
        bpy.context.view_layer.update()
        record['objects'] = [snapshot(o) for o in made]
    elif op['type'] == 'glass':
        for o in donor:
            if profile['selectors'][op['selector']] not in o.name:
                continue
            m = o.data.materials[0].copy()
            m.name = 'Transparent donor glazing'
            m.diffuse_color = (.11, .21, .27, op['alpha'])
            p = m.node_tree.nodes.get('Principled BSDF')
            p.inputs['Base Color'].default_value = (.11, .21, .27, 1)
            p.inputs['Alpha'].default_value = op['alpha']
            m.surface_render_method = 'DITHERED'
            o.data.materials[0] = m
            o['modification_id'] = op['id']
            record['objects'].append(snapshot(o))
    elif op['type'] == 'append':
        selected = [o for o in assets if o.get('module') == op['module'] and
                    (not op.get('name_prefix') or o.name.startswith(op['name_prefix']))]
        assert selected, f'No source objects for {op["id"]}'
        for original in selected:
            o = original.copy()
            if original.data:
                o.data = original.data.copy()
            scene.collection.objects.link(o)
            key = op['frame']
            if key == 'axles':
                # Paths store their coordinates in their spline, with a zero object origin.
                x = original.data.splines[0].points[0].co.x if original.type == 'CURVE' else original.location.x
                key = 'front-axle' if x > 0 else 'rear-axle'
            if op['module'] == 'rigging':
                key = 'bed' if original.name.startswith('aft-banner') else 'cab' if original.name.startswith('forward-sail') else key
            transform = frame_matrix(key)
            if op.get('translate'):
                transform = Matrix.Translation(Vector(op['translate'])) @ transform
            # Library objects are unlinked, so their evaluated matrix_world is stale.
            # These module assets are unparented; reconstruct their saved local pose.
            assert original.parent is None, 'Parented assets require hierarchy-aware replay'
            saved_pose = Matrix.LocRotScale(original.location, original.rotation_euler.to_quaternion(), original.scale)
            o.matrix_world = transform @ saved_pose
            if op.get('rotate_about_world_z'):
                cfg = op['rotate_about_world_z']
                pivot = Vector(cfg['pivot_m'])
                o.matrix_world = (Matrix.Translation(pivot) @
                    Matrix.Rotation(math.radians(cfg['degrees']), 4, 'Z') @
                    Matrix.Translation(-pivot) @ o.matrix_world)
            adjustment = None
            if op.get('extend_pedestal_to_bed') and original.name.startswith('Helm pedestal'):
                bottom = min((o.matrix_world @ Vector(c)).z for c in o.bound_box)
                top = max((o.matrix_world @ Vector(c)).z for c in o.bound_box)
                floor = profile['frames']['bed']['target_origin'][2]
                factor = (top - floor) / (top - bottom)
                o.location.z = floor + (o.location.z - bottom) * factor
                o.scale.z *= factor
                adjustment = {'pedestal_original_bottom_m': bottom, 'bed_floor_m': floor,
                              'top_preserved_m': top, 'vertical_scale': factor}
            if op.get('decorative_sag') and original.name.startswith(('Perimeter nautical rope', 'Front perimeter rope')):
                cfg = op['decorative_sag']
                anchors = [o.matrix_world @ Vector(p.co[:3]) for p in o.data.splines[0].points]
                for p in anchors:
                    if abs(p.y) > .1:
                        p.y += math.copysign(cfg['outboard_offset_m'], p.y)
                    if p.x > 2.4:
                        p.x = cfg.get('front_corner_x_m' if abs(p.y)>.1 else 'front_center_x_m', p.x+cfg['front_offset_m'])
                        p.z = cfg.get('front_attachment_z_m', p.z)
                front_span=original.name.startswith('Front perimeter rope')
                if front_span:anchors=[anchors[0],anchors[-1]]
                points = []
                for a, b in zip(anchors, anchors[1:]):
                    sag = cfg.get('front_sag_m',.075) if front_span else cfg['sag_m'] * min(1.2, max(.5, (b-a).length / 1.4))
                    for k in range(cfg['samples_per_span']):
                        t = k / cfg['samples_per_span']
                        p = a.lerp(b, t)
                        p.z -= 4*t*(1-t)*sag
                        if front_span:p.x += 4*t*(1-t)*(cfg['front_center_x_m']-cfg['front_corner_x_m'])
                        points.append(p)
                points.append(anchors[-1])
                for spline in list(o.data.splines):
                    o.data.splines.remove(spline)
                spline = o.data.splines.new('POLY')
                spline.points.add(len(points)-1)
                inv = o.matrix_world.inverted()
                for point, world in zip(spline.points, points):
                    point.co = (*(inv @ world), 1)
                o.data.bevel_depth=cfg.get('radius_m',o.data.bevel_depth)
                o.data.use_fill_caps=True
                adjustment = {'decorative_sag': cfg, 'world_attachment_points': [list(p) for p in anchors]}
            o['modification_id'] = op['id']
            o['source_component'] = original.name
            o['attachment_frame'] = key
            o['source_model_revision'] = recipe['revision']
            o['evidence'] = 'Photo-based campaign addition; donor fitting from explicit anchor profile'
            o.hide_render = bool(op.get('optional'))
            if op.get('readable_flag_faces'):
                for slot in o.material_slots:
                    slot.material = readable_flag_material(slot.material)
                if original.name.startswith('Sail 順 emblem'):
                    reverse = o.copy()
                    reverse.data = o.data.copy()
                    reverse.name = 'Sail 順 emblem / opposite face'
                    scene.collection.objects.link(reverse)
                    reverse.matrix_world = Matrix.Translation(Vector((0,-.011,0))) @ o.matrix_world
                    imported.append(reverse)
                    record['objects'].append(snapshot(reverse))
            if op.get('artwork_override'):
                artwork = H / op['artwork_override']
                assert sha(artwork) == op['artwork_sha256'], 'Artwork changed; review recipe'
                m = o.data.materials[0].copy()
                m.name = op['id'] + ' corrected artwork'
                for node in m.node_tree.nodes:
                    if node.type == 'TEX_IMAGE':
                        node.image = bpy.data.images.load(str(artwork), check_existing=True)
                        node.image.pack()
                        if op.get('transparent_artwork'):
                            m.node_tree.links.new(node.outputs['Alpha'],m.node_tree.nodes.get('Principled BSDF').inputs['Alpha'])
                            m.surface_render_method='DITHERED'
                o.data.materials[0] = m
            if op.get('project_to'):
                target = next(o for o in donor if profile['selectors'][op['project_to']] in o.name)
                # Subdivide the artwork so it follows the actual donor hood, not a floating plane.
                bpy.ops.object.select_all(action='DESELECT')
                o.select_set(True)
                bpy.context.view_layer.objects.active = o
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.subdivide(number_cuts=24)
                bpy.ops.object.mode_set(mode='OBJECT')
                bpy.context.view_layer.update()
                tree = BVHTree.FromObject(target, bpy.context.evaluated_depsgraph_get())
                inv = o.matrix_world.inverted()
                for vertex in o.data.vertices:
                    world = o.matrix_world @ vertex.co
                    start = target.matrix_world.inverted() @ Vector((world.x, world.y, 3.0))
                    hit, normal, face, distance = tree.ray_cast(start, Vector((0,0,-1)), 5.0)
                    if hit is None:
                        # Curved hood corners can fall outside the vertical-ray footprint.
                        # Keep their edge height on the nearest donor surface rather than
                        # leaving the old flat quad floating above the bonnet.
                        hit, normal, face, distance = tree.find_nearest(target.matrix_world.inverted() @ Vector((world.x,world.y,1.05)))
                    if hit is not None:
                        pos = target.matrix_world @ hit
                        pos.z += op.get('projection_offset_m',.008)
                        vertex.co = inv @ pos
                o.data.update()
            imported.append(o)
            bpy.context.view_layer.update()
            record['objects'].append({**snapshot(o), 'source_component': original.name,
                                      'frame': key, 'frame_transform': [list(r) for r in transform],
                                      'local_fit': adjustment})
    elif op['type'] == 'front_fascia':
        assert sha(H/op['generator']) == op['generator_sha256'], 'Front generator changed; review recipe'
        assert sha(H/op['plate_artwork']) == op['plate_artwork_sha256'], 'Front plate artwork changed'
        cfg = profile['front_fascia']
        assert cfg['enabled'], 'This profile does not use the donor front correction'
        for o in list(donor):
            if any(token in o.name for token in cfg['replacement_selectors']):
                o.hide_render=True;o.hide_viewport=True
                replaced.append(o.name);donor.remove(o)
        hood=next(o for o in donor if profile['selectors']['hood'] in o.name)
        for vertex in hood.data.vertices:
            world=hood.matrix_world@vertex.co
            t=max(0,min(1,(world.x-cfg['hood_ramp_start_x_m'])/(cfg['hood_ramp_end_x_m']-cfg['hood_ramp_start_x_m'])))
            vertex.co.z += cfg['hood_raise_front_m']*t
        hood.data.update()
        sys.path.insert(0,str(H))
        from front_fascia import build
        made=build(scene,profile,op,H)
        imported.extend(made)
        bpy.context.view_layer.update()
        record['objects']=[snapshot(o) for o in made]
        record['replaced_donor_objects']=list(replaced)
        record['hood_deformation']=cfg
    assert record['objects'], f'Empty operation: {op["id"]}'
    applied.append(record)

# Free unused appended objects without touching their native .blend library.
for o in assets:
    bpy.data.objects.remove(o, do_unlink=True)
objects = donor + imported
bpy.context.view_layer.update()
scene.render.resolution_x = 1500
scene.render.resolution_y = 1050
scene.render.resolution_percentage = 100
scene.cycles.samples = 24
scene.cycles.use_denoising = True
cam = scene.camera
cam.data.ortho_scale = 7.3
def pose(loc, target=(0, 0, 1.65), scale=7.3):
    cam.location = loc
    cam.rotation_euler = (Vector(target) - cam.location).to_track_quat('-Z', 'Y').to_euler()
    cam.data.ortho_scale = scale
pose((7, -8, 5))
bpy.ops.wm.save_as_mainfile(filepath=str(OUT / 'yangliu-donor-v1.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in objects:
    o.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(OUT / 'yangliu-donor-v1.glb'), export_format='GLB',
                          use_selection=True, export_extras=True, export_apply=True)
depsgraph = bpy.context.evaluated_depsgraph_get()
parts = []
for o in objects:
    e = o.evaluated_get(depsgraph)
    me = e.to_mesh()
    me.calc_loop_triangles()
    parts.append({'name': o.name, 'role': o['module'], 'modification_id': o['modification_id'],
                  'vertices': [list(o.matrix_world @ v.co) for v in me.vertices],
                  'triangles': [list(t.vertices) for t in me.loop_triangles]})
    e.to_mesh_clear()
geometry = {'revision': recipe['revision'], 'donor': profile['id'], 'units': 'metres',
            'orientation': profile['orientation'], 'wheelbase_m': profile['wheelbase_m'], 'parts': parts}
(OUT / 'source-geometry.json').write_text(json.dumps(geometry, separators=(',', ':')))
geometry_sha = sha(OUT / 'source-geometry.json')
report = {'revision': recipe['revision'], 'profile': args.profile, 'base_sha256': profile['base_sha256'],
          'module_source_sha256': recipe['source_sha256'], 'recipe_sha256': sha(recipe_path),
          'script_sha256': sha(__file__), 'geometry_sha256': geometry_sha,
          'texture_generator_sha256': sha(H / 'prepare_donor_wrap.py'),
          'copied_texture_sha256': sha(H / 'sources/donor-campaign-v1/wood-wrap-atlas.png'),
          'source_files_unchanged': sha(H / profile['base_blend']) == profile['base_sha256'] and
                                    sha(H / recipe['source_blend']) == recipe['source_sha256'],
          'donor_objects': len(donor), 'added_objects': len(imported),
          'replaced_donor_objects': replaced,
          'operations': applied, 'limits': recipe['limits']}
(OUT / 'modification-log.json').write_text(json.dumps(report, indent=2) + '\n')
if not args.skip_render:
    for name, loc in [('front', (7, -8, 5)), ('rear', (-7, 7, 4.5)), ('side', (0, -10, 3.1))]:
        pose(loc)
        scene.render.filepath = str(OUT / (name + '.png'))
        bpy.ops.render.render(write_still=True)
    for o in objects:
        if o['module'] in ['cab-roof', 'roof-rack', 'speakers', 'forward-sail', 'aft-banner', 'rigging', 'glazing']:
            o.hide_render = True
    pose((4, -5, 5), (.25, 0, 1.15), 3.6)
    scene.render.filepath = str(OUT / 'interior.png')
    bpy.ops.render.render(write_still=True)
print('CAMPAIGN_REPLAY_READY', len(applied), len(objects), geometry_sha)
