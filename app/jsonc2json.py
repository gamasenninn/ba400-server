from jsonc_parser.parser import JsoncParser
import sys
import json

encoding = 'utf-8'

args = sys.argv
if len(args) == 1 :
    pass
elif len(args) ==2:
    jsonc_filepath = args[1]
else:
    print("パラメータエラー\n")
    sys.exit()

with open(jsonc_filepath, 'r', encoding=encoding) as f:                # ファイルを開く (encoding 注意)
    jsonc_text = f.read()
    json_d = JsoncParser.parse_str(jsonc_text)

