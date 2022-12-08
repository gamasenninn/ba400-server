import unittest
import sys
import os
import filecmp

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from app import tpcl_maker as t

class GetStatusTest(unittest.TestCase):

    def test_get_status(self):
        jsonc_filepath = 'test_print_normal.jsonc'

        conf = t.read_jsonc_file(jsonc_filepath)
        if conf:
            result = t.check_status(conf)
            
        self.assertTrue(result["WN"])
        self.assertTrue(result["WS"])
        self.assertTrue(result["WA"])
        self.assertTrue(result["WB"])
        self.assertTrue(result["WV"])

    def test_analize_status(self):
        jsonc_filepath = 'test_print_normal.jsonc'

        conf = t.read_jsonc_file(jsonc_filepath)
        if conf:
            result = t.analize_status(conf)
        
        self.assertTrue(result)
