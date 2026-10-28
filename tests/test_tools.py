import importlib.util
import json
from pathlib import Path
import struct
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FrameTests(unittest.TestCase):
    def setUp(self):
        self.mod = load('analyze_frames')

    def test_linear_percentile_not_floor_index(self):
        self.assertAlmostEqual(self.mod.percentile([1, 2, 3, 100], .99), 97.09)

    def test_streak_does_not_cross_blocks(self):
        result = self.mod.summarize([[10, 10, 20], [20, 10, 10]], 16.67)
        self.assertEqual(result['longest_long_streak'], 1)
        self.assertEqual(result['p99_ms'], 20)
        self.assertEqual(result['long_frames'], 2)

    def test_fps_is_frames_divided_by_elapsed(self):
        result = self.mod.summarize([[10, 30]], 16.67)
        self.assertEqual(result['mean_fps'], 50)

    def test_invalid_samples_fail_instead_of_becoming_zero(self):
        for bad in ([], [[]], [[0]], [[-1]], [[float('nan')]], [[float('inf')]], [[True]]):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                self.mod.summarize(bad, 16.67)

    def test_invalid_threshold_rejected(self):
        with self.assertRaises(ValueError):
            self.mod.summarize([[10]], 0)

    def test_per_view_and_session_regression_not_hidden_by_pooling(self):
        rows = []
        for view, a, b in [('whole', 10, 8), ('detail', 1, 2)]:
            for arm, value in [('original', a), ('candidate', b)]:
                rows.append(dict(session='s1', view=view, arm=arm, block='b1', frame_ms=[value]*20))
        data = dict(measurement='screen', environment=dict(device='test', resolution=[1920,1080]), rows=rows)
        result = self.mod.analyze(data, 16.67, .05, .2)
        self.assertFalse(result['all_measured_comparisons_pass'])
        self.assertEqual(result['comparisons'][1]['view'], 'whole')
        self.assertFalse(next(r for r in result['comparisons'] if r['view']=='detail')['pass'])
        self.assertFalse(result['full_acceptance_proven'])

    def test_duplicate_block_rejected(self):
        row = dict(session='s', view='v', arm='original', block='b', frame_ms=[1])
        with self.assertRaises(ValueError):
            self.mod.analyze(dict(measurement='screen', environment={'device':'x'}, rows=[row,row]),16,.05,.2)

    def test_missing_arm_unknown_not_pass(self):
        data = dict(measurement='offscreen_sync', environment={'device':'x'}, rows=[dict(session='s',view='v',arm='original',block='a',frame_ms=[1])])
        result = self.mod.analyze(data,16,.05,.2)
        self.assertIsNone(result['comparisons'][0]['pass'])
        self.assertFalse(result['all_measured_comparisons_pass'])


class GLBTests(unittest.TestCase):
    def setUp(self):
        self.mod = load('audit_glb')

    def doc(self):
        return dict(asset={'version':'2.0'},accessors=[{'count':1000},{'count':3000}],
                    meshes=[{'primitives':[{'attributes':{'POSITION':0},'indices':1}]}],
                    nodes=[{'mesh':0},{'mesh':0}],scenes=[{'nodes':[0,1]}],scene=0)

    def test_instances_separate_from_unique(self):
        r=self.mod.audit(self.doc())
        self.assertEqual(r['primitive_position_count'],1000)
        self.assertEqual(r['scene_instance_position_count'],2000)
        self.assertEqual(r['scene_instance_triangles'],2000)
        self.assertEqual(r['scene_mesh_nodes'],2)

    def test_primitive_sum_not_geometric_unique_count(self):
        d=self.doc();d['meshes'][0]['primitives']*=2
        r=self.mod.audit(d)
        self.assertEqual(r['primitive_position_count'],2000)
        self.assertIsNone(r['geometric_unique_vertices'])

    def test_strip_is_counted_as_strip(self):
        d=self.doc();d['meshes'][0]['primitives'][0]['mode']=5;d['accessors'][1]['count']=8
        self.assertEqual(self.mod.audit(d)['primitive_triangles'],6)

    def test_cycle_fails(self):
        d=self.doc();d['nodes'][0]['children']=[0]
        with self.assertRaises(ValueError):self.mod.audit(d)

    def test_compression_is_flagged_not_decoded(self):
        d=self.doc();d['extensionsUsed']=['KHR_draco_mesh_compression']
        r=self.mod.audit(d)
        self.assertFalse(r['decoded_geometry_validated'])
        self.assertIn('KHR_draco_mesh_compression',r['extensions_used'])

    def test_real_glb_reader_rejects_truncated_data(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'bad.glb';path.write_bytes(b'glTF')
            with self.assertRaises(ValueError):self.mod.read_glb(path)

    def test_real_glb_reader(self):
        raw=json.dumps(self.doc()).encode();raw+=b' '*((-len(raw))%4)
        blob=struct.pack('<4sII',b'glTF',2,20+len(raw))+struct.pack('<II',len(raw),0x4e4f534a)+raw
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'a.glb';path.write_bytes(blob)
            self.assertEqual(self.mod.audit(self.mod.read_glb(path))['scene_instance_triangles'],2000)


if __name__=='__main__':
    unittest.main()
