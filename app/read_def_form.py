from jsonc_parser.parser import JsoncParser
import socket

#--- read JSONC ------
filepath = 'print_conf_ip.jsonc'
encoding = 'utf-8'
prt_encoding = 'cp932'

def ssend(com_str):
    print(com_str)
    b_com = b'\x1b' +com_str.encode(prt_encoding) + b'\x0a\x00'
    #print(b_com)
    # コマンド送信
    sock.send(b_com)

with open(filepath, 'r', encoding=encoding) as f:                # ファイルを開く (encoding 注意)
    jsonc_text = f.read()     

conf = JsoncParser.parse_str(jsonc_text)
#print(conf)

#--- printer IP ----
ip = conf['device']['ip']
port = int(conf['device']['port'])

# socket info
sinfo = socket.getaddrinfo(ip, port)
print("info:",sinfo)

# ソケット作成
sock = socket.socket(socket.AF_INET,0,0)

# サーバーへ接続
sock.connect((ip, port))

#--- D: setttingLable ----
sl = conf['setLabel']
command = f"D{sl['pitch']},{sl['width']},{sl['hight']}"
ssend(command)

#--- define format ----
sf = conf['setFormat']
# buffer clear
if sf['bufferClear'] == "True":
    command = f"C"
    ssend (command)

# PCs
pcs = sf['PC']
for pc in pcs:
    align = ""
    if 'align' in pc:
        align = f",{pc['align']}"
    if 'autoLineFeed' in pc:
        align = f",P5{pc['autoLineFeed']['width']}{pc['autoLineFeed']['pitch']}{pc['autoLineFeed']['rowMax']}"

    command = f"PC{pc['number']};{pc['x']},{pc['y']},{pc['xR']},{pc['yR']},{pc['fontType']},{pc['fontSpace']},{pc['fontDeco']}{align}"
    ssend (command)

# XB_QR
xbqrs = sf['XB_QR']
for xq in xbqrs:
    command = f"XB{xq['number']};{xq['x']},{xq['y']},T,{xq['errorLevel']},{xq['cellSize']},{xq['mode']},{xq['rotation']},{xq['model']}"
    ssend (command)

# XB_BAR
xbs = sf['XB_BAR']
for xb in xbs:
    command = f"XB{xb['number']};{xb['x']},{xb['y']},{xb['type']},{xb['digit']},{xb['width']},{xb['rotation']},{xb['height']},+0000000000,000,{xb['outNumber']},{xb['zeroSup']}"
    ssend (command)

# data
data = conf['data']
for d in data:
    #print(d['command'])
    if d['command'] == "RC":
        command = f"RC{d['number']};{d['content']}"
        ssend (command)
    if d['command'] == "RB":
        command = f"RB{d['number']};{d['content']}"
        ssend (command)
    if d['command'] == "XS":
        command = f"XS;I,{d['copies']},{d['cutInterval']}{d['censorType']}{d['mode']}{d['speed']}{d['ribbon']}{d['tagRotation']}{d['statusResponse']}"
        ssend (command)

# final
finals = conf['final']
for fin in finals:
    if fin['command'] == "IB":
        command = f"IB"
        ssend (command)

sock.shutdown(socket.SHUT_RDWR)
sock.close()
