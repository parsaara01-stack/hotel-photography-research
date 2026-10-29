import copy
import hashlib
import math
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'analysis'))
from analyze import validate_release,validate_record,summarize,categories,score
from power import sample_size

class AnalysisTests(unittest.TestCase):
    def setUp(self):
        # Fabricated unit structures only. These do not represent participants or approvals.
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)
        self.release=dict(status='approved_for_collection',schema_version=2,protocol_version='0.2',stimulus_version='fixture-only',
            review_reference='unit-fixture',preregistration_reference='unit-fixture',assignment_ceiling=1000,
            items=[dict(id=f'item_{j}',options=['yes','no','cannot_tell'],correct='yes') for j in range(6)],
            answerability=[dict(item_id=f'item_{j}',narrower='not_established',broader='established') for j in range(6)],stimuli=[])
        for arm in [0,1]:
            for slot in range(1,7):
                path=f'{arm}-{slot}.jpg';raw=f'nonimage-test-bytes-{arm}-{slot}'.encode();(self.root/path).write_bytes(raw)
                self.release['stimuli'].append(dict(coverage=arm,slot=slot,path=path,sha256=hashlib.sha256(raw).hexdigest()))
        self.row=dict(schema_version=2,data_kind='observed',environment='approved_study',protocol_version='0.2',stimulus_version='fixture-only',
            participant_id='fixture_000',consent=True,eligible=True,coverage=0,answers=['yes']*6,confidence=80,coverage_rating=4,technical_failure=False)
    def rows(self,values):
        return [dict(self.row,participant_id=f'fixture_{arm}_{j}',coverage=arm,answers=['yes']*s+['no']*(6-s)) for arm,vs in enumerate(values) for j,s in enumerate(vs)]
    def test_demo_release_blocked(self):
        with self.assertRaises(ValueError):validate_release(dict(status='demo_only'),self.root)
    def test_files_verified(self):
        validate_release(self.release,self.root)
        (self.root/'0-1.jpg').write_bytes(b'changed')
        with self.assertRaises(ValueError):validate_release(self.release,self.root)
    def test_dummy_hashes_fail(self):
        for item in self.release['stimuli']:item['sha256']='a'*64
        with self.assertRaises(ValueError):validate_release(self.release,self.root)
    def test_slots_paths_and_answerability(self):
        for field,value in [('slot',2),('path','../escape.jpg')]:
            r=copy.deepcopy(self.release);r['stimuli'][0][field]=value
            with self.assertRaises(ValueError):validate_release(r,self.root)
        self.release['answerability'][0]['broader']='not_established'
        with self.assertRaises(ValueError):validate_release(self.release,self.root)
    def test_demo_synthetic_and_unknown_fields(self):
        for kind in ['demo','synthetic','test']:
            with self.assertRaises(ValueError):validate_record(dict(self.row,data_kind=kind),self.release)
        with self.assertRaises(ValueError):validate_record(dict(self.row,email='unit@example.invalid'),self.release)
    def test_invalid_types_ranges_and_old_schema(self):
        for change in [dict(coverage=True),dict(confidence=True),dict(coverage_rating=8),dict(answers=[{}]*6),dict(schema_version=1),dict(consent=False)]:
            with self.assertRaises(ValueError):validate_record(dict(self.row,**change),self.release)
    def test_categories_distinguish_uncertainty(self):
        r=dict(self.row,answers=['yes','no','cannot_tell',None,'yes','cannot_tell'])
        self.assertEqual(categories(r,self.release),dict(correct=2,incorrect=1,cannot_tell=2,missing=1));self.assertIsNone(score(r,self.release))
    def test_independent_nonzero_variance_estimate(self):
        # Each sample variance = 1, n=3; SE=sqrt(2/3), difference=2.
        result=summarize(self.rows([[0,1,2],[2,3,4]]),self.release)
        self.assertEqual(result['coverage_difference'],2)
        self.assertAlmostEqual(result['standard_error'],math.sqrt(2/3))
        self.assertAlmostEqual(result['ci95_normal'][0],.39969610788,places=9)
        self.assertAlmostEqual(result['p_two_sided_normal'],.014305878435,places=10)
    def test_unbalanced_arm_means(self):
        self.assertEqual(summarize(self.rows([[0,2],[2,3,4,5,6]]),self.release)['coverage_difference'],3)
    def test_partial_bounds_preserve_observed_answers(self):
        rows=self.rows([[2],[4]])
        rows.append(dict(self.row,participant_id='fixture_partial',coverage=1,answers=['yes']*5+[None]))
        out=summarize(rows,self.release)
        self.assertEqual(out['full_roster_identification_bounds'],[2.5,3])
        self.assertEqual(out['arms']['1']['items'][5]['missing'],1)
        self.assertFalse(out['bounds_are_confidence_intervals'])
    def test_all_missing_one_arm(self):
        rows=self.rows([[2]])+[dict(self.row,participant_id='fixture_missing',coverage=1,answers=[None]*6,technical_failure=True)]
        out=summarize(rows,self.release)
        self.assertIsNone(out['coverage_difference']);self.assertEqual(out['full_roster_identification_bounds'],[-2,4])
    def test_degenerate_variance_withholds_inference(self):
        out=summarize(self.rows([[2,2],[4,4]]),self.release)
        self.assertEqual(out['coverage_difference'],2);self.assertIsNone(out['ci95_normal']);self.assertIsNone(out['p_two_sided_normal']);self.assertIn('degenerate',out['inference'])
    def test_duplicate_and_ceiling_rejected(self):
        with self.assertRaises(ValueError):summarize([self.row,self.row],self.release)
        self.release['assignment_ceiling']=2
        with self.assertRaises(ValueError):summarize(self.rows([[1,2],[3]]),self.release)
    def test_diagnostic_threshold(self):
        out=summarize(self.rows([[1,2]*25,[2,3]*25]),self.release)
        self.assertEqual(out['inference'],'asymptotic primary inference')
    def test_power_and_invalid_inputs(self):
        self.assertEqual(sample_size()['complete_n'],350);self.assertEqual(sample_size()['assignment_ceiling'],412)
        self.assertEqual(sample_size(.2)['complete_n'],786);self.assertEqual(sample_size(.4)['complete_n'],198)
        for d,loss in [(0,.15),(.3,1),(float('nan'),.15)]:
            with self.assertRaises(ValueError):sample_size(d,loss)

if __name__=='__main__':unittest.main()
