"""Real Blender integration on generated geometry; no teacher assets. Run with host Python."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile

ROOT=Path(__file__).resolve().parents[1]


def run(blender,script,*args):
    r=subprocess.run([blender,'--background','--factory-startup','--python-exit-code','9','--python',str(script),'--',*map(str,args)],capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=120)
    if r.returncode:raise AssertionError(r.stdout[-3000:]+r.stderr[-3000:])


def main():
    p=argparse.ArgumentParser();p.add_argument('--blender',required=True);a=p.parse_args()
    with tempfile.TemporaryDirectory(prefix='mesh-skill-test-') as tmp:
        w=Path(tmp);fixture=w/'fixture.py'
        fixture.write_text('''import bpy,sys
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
bpy.ops.mesh.primitive_uv_sphere_add(segments=48,ring_count=24);bpy.context.object.name='Body'
bpy.ops.mesh.primitive_torus_add(major_segments=32,minor_segments=12,location=(3,0,0));bpy.context.object.name='Rim'
bpy.ops.mesh.primitive_cylinder_add(vertices=12,radius=.02,depth=2,location=(0,3,0));bpy.context.object.name='Pin'
bpy.ops.wm.save_as_mainfile(filepath=sys.argv[-1])
''',encoding='utf-8')
        source=w/'source.blend';run(a.blender,fixture,source)
        before=hashlib.sha256(source.read_bytes()).hexdigest()
        helper=ROOT/'scripts/blender_candidate.py';out=w/'candidate'
        run(a.blender,helper,'--input',source,'--output-dir',out,'--objects','Body','--ratio','.3')
        report=json.loads((out/'candidate_report.json').read_text())
        assert report['after']['objects']['Body']['triangles']<report['before']['objects']['Body']['triangles']
        assert report['after']['objects']['Body']['vertices']<report['before']['objects']['Body']['vertices']
        for name in ('Rim','Pin'):
            assert report['before']['objects'][name]['mesh_sha256']==report['after']['objects'][name]['mesh_sha256']
        assert hashlib.sha256(source.read_bytes()).hexdigest()==before
        assert report['acceptance']=='UNVALIDATED_CANDIDATE'
        verify=w/'verify.py';verify.write_text('''import bpy,sys,json
bpy.ops.wm.open_mainfile(filepath=sys.argv[-2])
assert set(o.name for o in bpy.context.scene.objects if o.type=='MESH')=={'Body','Rim','Pin'}
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=sys.argv[-1])
assert len([o for o in bpy.context.scene.objects if o.type=='MESH'])==3
print('REAL_ROUNDTRIP_OK')
''',encoding='utf-8')
        run(a.blender,verify,out/'candidate.blend',out/'candidate.glb')
        # Existing output is refused, rather than overwriting a reviewed candidate.
        try:run(a.blender,helper,'--input',source,'--output-dir',out,'--objects','Body','--ratio','.3')
        except AssertionError as e:assert 'output directory must be new' in str(e)
        else:raise AssertionError('existing output was overwritten')
        linked_fixture=w/'linked_fixture.py'
        linked_fixture.write_text('''import bpy,sys
lib,source=sys.argv[-2:]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.mesh.primitive_cube_add();bpy.context.object.data.name='ExternalMesh'
bpy.ops.wm.save_as_mainfile(filepath=lib)
bpy.ops.wm.read_factory_settings(use_empty=True)
with bpy.data.libraries.load(lib,link=True) as (available,loaded):loaded.meshes=['ExternalMesh']
ob=bpy.data.objects.new('LinkedBody',loaded.meshes[0]);bpy.context.scene.collection.objects.link(ob)
assert ob.library is None and ob.data.library is not None
bpy.ops.wm.save_as_mainfile(filepath=source)
''',encoding='utf-8')
        linked_source=w/'linked_source.blend'
        run(a.blender,linked_fixture,w/'library.blend',linked_source)
        try:run(a.blender,helper,'--input',linked_source,'--output-dir',w/'linked-output','--objects','LinkedBody','--ratio','.5')
        except AssertionError as e:assert 'linked libraries' in str(e)
        else:raise AssertionError('linked Mesh data was accepted despite documented rejection')
        print(json.dumps(dict(status='PASS',source_unchanged=True,protected_parts_byte_equal=True,
                              before=report['before']['objects']['Body']['triangles'],
                              after=report['after']['objects']['Body']['triangles'],
                              before_vertices=report['before']['objects']['Body']['vertices'],
                              after_vertices=report['after']['objects']['Body']['vertices'],
                              linked_mesh_data_rejected=True,blend_and_glb_reimported=True,performance_validated=False)))


if __name__=='__main__':main()
