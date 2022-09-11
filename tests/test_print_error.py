import unittest
import sys
import os
import filecmp

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from app import tpcl_maker as t

class PrintErrorTest(unittest.TestCase):

    #---ソケット関連のエラーテスト--
    def test_socket(self):
        jsonc_filepath = 'test_print_normal.jsonc'
        #log_filepath = 'tpcl_send.log'
        #exp_filepath = 'test_print_normal.exp'

        conf = t.read_jsonc_file(jsonc_filepath)
        if conf:
            #存在しないIPを指定する
            conf['device']['ip'] = "192.168.11.206"
            result = t.tpcl_maker(conf)
            
        self.assertEqual(result,-101)

        conf = t.read_jsonc_file(jsonc_filepath)
        if conf:
            #存在しないポートを指定する
            conf['device']['port'] = 9102
            result = t.tpcl_maker(conf)
            
        self.assertEqual(result,-102)

    #---ファイル関連のエラーテスト--
    def test_file_not_found(self):
        jsonc_filepath = 'test_print_normalXXXXX.jsonc'

        with self.assertRaises(FileNotFoundError):
            conf = t.read_jsonc_file(jsonc_filepath)
