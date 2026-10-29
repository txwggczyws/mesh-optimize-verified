"""Blender-only, opt-in per-object Decimate baseline; NEVER an acceptance certificate.
blender --background --factory-startup --python-exit-code 9 --python SCRIPT -- --help
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys
import bpy


def mesh_digest(mesh):
    # All relevant authored streams for protected objects; digest is not a visual test.
    values=dict(vertices=[list(v.co) for v in mesh.vertices],
                edges=[(list(e.vertices),e.use_seam,e.use_edge_sharp) for e in mesh.edges],
                polygons=[(list(p.vertices),p.material_index,p.use_smooth) for p in mesh.polygons],
                corner_normals=[list(n.vector) for n in mesh.corner_normals],
                uv={layer.name:[list(v.uv) for v in layer.data] for layer in mesh.uv_layers},
                colors={layer.name:[list(v.color) for v in layer.data] for layer in mesh.color_attributes},
                materials=[m.name if m else None for m in mesh.materials])
    return hashlib.sha256(json.dumps(values,sort_keys=True,allow_nan=False).encode()).hexdigest()


def snapshot():
    result={};unique={}
    for ob in bpy.context.scene.objects:
        if ob.type!='MESH':continue
        me=ob.data;me.calc_loop_triangles()
        row=dict(vertices=len(me.vertices),triangles=len(me.loop_triangles),mesh_sha256=mesh_digest(me),
                 transform=[list(r) for r in ob.matrix_world],materials=len(me.materials))
        result[ob.name]=row;unique[me.as_pointer()]=row
    return dict(objects=result,mesh_objects=len(result),unique_meshes=len(unique),
                unique_vertices=sum(r['vertices'] for r in unique.values()),
                unique_triangles=sum(r['triangles'] for r in unique.values()),
                instance_vertices=sum(r['vertices'] for r in result.values()),
                instance_triangles=sum(r['triangles'] for r in result.values()),
                count_scope='Blender mesh vertices; not exported GLB or Unity render vertices')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input',required=True,type=Path);p.add_argument('--output-dir',required=True,type=Path)
    p.add_argument('--objects',required=True,nargs='+',help='Exact mesh object names permitted to change; all others protected')
    p.add_argument('--ratio',required=True,type=float,help='Retained triangle fraction requested, 0<ratio<=1; not an error tolerance')
    args=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    source=args.input.resolve();out=args.output_dir.resolve()
    if not source.is_file() or source.suffix.lower() not in ('.blend','.glb','.fbx'):
        raise ValueError('input must be an existing .blend, .glb or .fbx')
    if out.exists() or out==source or out in source.parents:
        raise ValueError('output directory must be new, and cannot contain the source')
    if not math.isfinite(args.ratio) or not 0<args.ratio<=1:raise ValueError('ratio must be in (0,1]')
    original_hash=hashlib.sha256(source.read_bytes()).hexdigest()
    # Do not execute auto-run Python embedded in .blend files.
    bpy.context.preferences.filepaths.use_scripts_auto_execute=False
    if source.suffix.lower()=='.blend':bpy.ops.wm.open_mainfile(filepath=str(source),use_scripts=False)
    else:
        bpy.ops.wm.read_factory_settings(use_empty=True)
        if source.suffix.lower()=='.glb':bpy.ops.import_scene.gltf(filepath=str(source))
        else:bpy.ops.import_scene.fbx(filepath=str(source))
    targets=[]
    for name in args.objects:
        ob=bpy.context.scene.objects.get(name)
        if not ob or ob.type!='MESH':raise ValueError('missing mesh object: '+name)
        if ob.data.shape_keys or ob.modifiers or ob.vertex_groups or ob.library or ob.data.library:
            raise ValueError('baseline helper does not handle modifiers, shape keys, weights or linked libraries: '+name)
        targets.append(ob)
    if len(set(args.objects))!=len(args.objects):raise ValueError('duplicate object selection')
    before=snapshot()
    for ob in targets:
        ob.data=ob.data.copy() # Shared protected instances must not change.
        bpy.ops.object.select_all(action='DESELECT');ob.select_set(True);bpy.context.view_layer.objects.active=ob
        modifier=ob.modifiers.new('SkillDecimateBaseline','DECIMATE')
        modifier.decimate_type='COLLAPSE';modifier.ratio=args.ratio;modifier.use_collapse_triangulate=True
        bpy.ops.object.modifier_apply(modifier=modifier.name)
    after=snapshot()
    for name,row in before['objects'].items():
        if name not in args.objects and row!=after['objects'][name]:raise RuntimeError('protected mesh changed: '+name)
        if row['transform']!=after['objects'][name]['transform']:raise RuntimeError('object transform changed: '+name)
    out.mkdir(parents=True,exist_ok=False)
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'candidate.blend'))
    bpy.ops.export_scene.gltf(filepath=str(out/'candidate.glb'),export_format='GLB')
    if hashlib.sha256(source.read_bytes()).hexdigest()!=original_hash:raise RuntimeError('source changed')
    report=dict(tool='Blender Decimate opt-in baseline',blender=bpy.app.version_string,
                source_filename=source.name,source_sha256=original_hash,objects_changed=args.objects,
                requested_ratio=args.ratio,before=before,after=after,acceptance='UNVALIDATED_CANDIDATE',
                source_unchanged=True,limitations=['Decimate can damage holes, thin walls, seams, normals and silhouette.',
                'GLB export may change unsupported shaders/materials and split render vertices.',
                'Reimport each target format, compare geometry/images, profile target device, and review manually.',
                'Protected digest covers authored mesh data, not every dependency or complete application behavior.'])
    with (out/'candidate_report.json').open('x',encoding='utf-8') as f:json.dump(report,f,ensure_ascii=False,indent=2,allow_nan=False)
    print('UNVALIDATED_CANDIDATE',after['instance_vertices'],after['instance_triangles'])


if __name__=='__main__':main()
