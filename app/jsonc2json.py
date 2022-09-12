from jsonc_parser.parser import JsoncParser
import sys
import json
import os

encoding = 'utf-8'

args = sys.argv
if len(args) == 1 :
    pass
elif len(args) ==2:
    jsonc_filepath = args[1]
else:
    print("パラメータエラー\n")
    sys.exit()

#print(os.path.dirname(jsonc_filepath))
#basename = os.path.basename(jsonc_filepath)
fs = os.path.splitext(jsonc_filepath)
filename = fs[0]

#---- json に変換する ------
with open(jsonc_filepath, 'r', encoding=encoding) as f:                # ファイルを開く (encoding 注意)
    jsonc_text = f.read()
    json_d = JsoncParser.parse_str(jsonc_text)
    json_str =json.dumps(json_d,ensure_ascii=False,indent=2)
    print (json_str)

#---- json に出力する ------
json_filepath = filename+'.json'
with open(json_filepath, 'w', encoding=encoding) as f:
    f.write(json_str)

#---- js に出力する ------
json_filepath = filename+'.js'
with open(json_filepath, 'w', encoding=encoding) as f:
    js_str = "conf="+json_str+";"
    f.write(js_str)
