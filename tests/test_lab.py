import unittest,datetime
import lab
class FeedbackPolicyTests(unittest.TestCase):
    def setUp(self):self.today=datetime.date(2026,11,19)
    def test_noisy_gate_blocks_all_three(self):self.assertEqual(lab.evaluate('before',today=self.today)['counts']['BLOCK'],3)
    def test_improved_gate_does_not_hide_exposed_marker(self):
        self.assertEqual(lab.evaluate('after',today=self.today)['counts'],{'BLOCK':1,'WARN':1,'TRACK':1})
    def test_removal_passes_with_owned_exception(self):self.assertEqual(lab.evaluate('after',True,self.today)['status'],'PASS')
    def test_expired_exception_reopens_dependency(self):self.assertEqual(lab.evaluate('after',True,datetime.date(2026,11,22))['counts']['BLOCK'],1)
    def test_missing_exception_owner_fails_closed(self):
        e=[{'finding_id':'DEMO-DEP-001','expires':'2026-11-21','reason':'demo','approved_by':'demo'}]
        self.assertEqual(lab.evaluate('after',True,self.today,e)['counts']['BLOCK'],1)
    def test_secret_is_not_exceptable(self):
        ex=[{'finding_id':'DEMO-SECRET-001','owner':'x','approved_by':'x','reason':'x','expires':'2026-11-21'}]
        self.assertEqual(lab.evaluate('after',False,self.today,ex)['findings'][0]['outcome'],'BLOCK')
