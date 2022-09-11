import unittest
import sys
import os
import filecmp

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from app import tpcl_maker as t

class PrintNormalTest(unittest.TestCase):

    def test_normal(self):
        jsonc_filepath = 'test_print_normal.jsonc'
        log_filepath = 'tpcl_send.log'
        exp_filepath = 'test_print_normal.exp'

        conf = t.read_jsonc_file(jsonc_filepath)
        if conf:
            result = t.tpcl_maker(conf)
            
        self.assertTrue(result)

        self.assertTrue(filecmp.cmp(log_filepath,exp_filepath,shallow=True))
        #self.assertTrue(filecmp(log_filepath,exp_filepath,shallow=True))
