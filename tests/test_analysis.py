import copy
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'analysis'))
from analyze import validate_release,validate_record,summarize
from power import sample_size

class AnalysisTests(unittest.TestCase):
    def setUp(self):
        # Test-only fabricated structures, never a study dataset or a collection approval.
        self.release=dict(status='approved_for_collection',protocol_version='unit-test',stimulus_version='fixture-only',stimulus_sha256=['a'*64]*24,items=[dict(options=['yes','no','cannot_tell'],correct='yes')]*6)
        self.row=dict(schema_version=1,data_kind='observed',environment='approved_study',protocol_version='unit-test',stimulus_version='fixture-only',participant_id='fixture_000',consent=True,eligible=True,clarity=0,atmosphere=0,answers=['yes']*6,confidence=80,booking_intention=4,appeal=4,technical_failure=False)
    def test_demo_release_blocked(self):
        with self.assertRaises(ValueError): validate_release(dict(status='demo_only'))
    def test_demo_synthetic_test_excluded(self):
        for kind in ['demo','synthetic','test']:
            r=dict(self.row,data_kind=kind)
            with self.assertRaises(ValueError): validate_record(r,self.release)
    def test_unknown_private_fields_rejected(self):
        with self.assertRaises(ValueError): validate_record(dict(self.row,email='never-accept@example.invalid'),self.release)
    def test_invalid_answers_and_ranges(self):
        for change in [dict(answers=['invented']*6),dict(confidence=True),dict(clarity=True),dict(consent=False),dict(appeal=8)]:
            with self.assertRaises(ValueError): validate_record(dict(self.row,**change),self.release)
    def test_duplicate_id_fails(self):
        with self.assertRaises(ValueError): summarize([self.row,self.row],self.release)
    def test_balanced_contrast_and_missing_bounds(self):
        rows=[]
        for c in [0,1]:
            for a in [0,1]:
                for j in range(2):
                    rows.append(dict(self.row,participant_id=f'fixture_{c}{a}{j}',clarity=c,atmosphere=a,answers=['yes']*(2+c)+['no']*(4-c)))
        out=summarize(rows,self.release)
        self.assertEqual(out['clarity_difference'],1)
        self.assertEqual(out['full_roster_bounds'],[1,1])
        self.assertIn('diagnostic',out['inference'])
        rows.append(dict(self.row,participant_id='fixture_missing',clarity=1,atmosphere=0,answers=[None]*6,technical_failure=True))
        out=summarize(rows,self.release)
        self.assertEqual(out['cells']['(1, 0)']['missing_n'],1)
        self.assertEqual(out['cells']['(1, 0)']['technical_failure_n'],1)
        self.assertEqual(out['clarity_difference'],1)
        self.assertLess(out['full_roster_bounds'][0],1)
        self.assertGreater(out['full_roster_bounds'][1],1)
    def test_unbalanced_cells_equal_weight(self):
        rows=[]
        for c,a,n,score in [(0,0,2,0),(0,1,10,4),(1,0,10,2),(1,1,2,6)]:
            for j in range(n):
                rows.append(dict(self.row,participant_id=f'fixture_{c}{a}{j}',clarity=c,atmosphere=a,answers=['yes']*score+['no']*(6-score)))
        self.assertEqual(summarize(rows,self.release)['clarity_difference'],2)
    def test_cannot_tell_zero_unanswered_missing(self):
        from analyze import score
        self.assertEqual(score(dict(self.row,answers=['cannot_tell']*6),self.release),0)
        self.assertIsNone(score(dict(self.row,answers=[None]*6),self.release))
    def test_power_plan(self):
        self.assertEqual(sample_size()['complete_n'],352)
        self.assertEqual(sample_size()['assignment_ceiling'],416)
        self.assertEqual(sample_size(.2)['complete_n'],788)

if __name__=='__main__': unittest.main()
