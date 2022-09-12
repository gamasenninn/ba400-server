from jsonc_parser.parser import JsoncParser
import socket
import sys
from PIL import Image, ImageDraw, ImageFont

# --- config value ------
IS_SEND = False
IS_LOG = True
LOG_FILE_PATH = "tpcl_send.log"
SOCKET_TIME_OUT = 5
IS_IMAGE = True
IMAGE_FILE_PATH = "tpcl_preview.png"

# ----- error code -----
ERR_SOCKET_TIME_OUT = -101
ERR_CNNECTION_REFUSED = -102

# ----コマンド送信 -----


def ssend(com_str, socket, prt_encoding='cp932'):
    # print(com_str)
    b_com = b'\x1b' + com_str.encode(prt_encoding) + b'\x0a\x00'
    # print(b_com)
    if IS_SEND:
        socket.send(b_com)
    if IS_LOG:
        encoding = 'utf-8'
        with open(LOG_FILE_PATH, 'a', encoding=encoding) as f:                # ファイルを開く (encoding 注意)
            f.write(com_str+"\n")

# ----- JSONC定義ファイルの読み込み -------


def read_jsonc_file(jsonc_filepath, encoding='utf-8'):

    with open(jsonc_filepath, 'r', encoding=encoding) as f:                # ファイルを開く (encoding 注意)
        try:
            jsonc_text = f.read()
            return JsoncParser.parse_str(jsonc_text)

        except FileNotFoundError:
            print('ファイルが存在しません。')
            return {}

# ------ tpcl コマンドを編集し、送信する ------


def tpcl_maker(conf):
    if IS_LOG:
        encoding = 'utf-8'
        with open(LOG_FILE_PATH, 'w', encoding=encoding) as f:                # ファイルを開く (encoding 注意)
            pass

    # --- printer IP ----
    ip = conf['device']['ip']
    port = int(conf['device']['port'])
    # if 'isPrintOut' in conf['device']:
    global IS_SEND
    IS_SEND = eval(conf['device']['isPrintOut']
                   ) if 'isPrintOut' in conf['device'] else False
    global IS_IMAGE
    IS_IMAGE = eval(conf['device']['isImage']
                    ) if 'isImage' in conf['device'] else False
    # create socket
# with で全体を囲んだほうがよいのではないか？
    sock = socket.socket(socket.AF_INET, 0, 0)
    # connect to printer
    sock.settimeout(SOCKET_TIME_OUT)
    try:
        sock.connect((ip, port))
    except socket.timeout:  # タイムアウトエラー
        sock.close()
        return ERR_SOCKET_TIME_OUT
    except ConnectionRefusedError:  # コネクション拒否エラー
        sock.close()
        return ERR_CNNECTION_REFUSED

    # --- D: setttingLable ----
    sl = conf['setLabel']
    command = f"D{sl['pitch']},{sl['width']},{sl['height']}"
    ssend(command, sock)
    # image
    if IS_IMAGE:
        width = int(int(sl['width'])/10*3.78)
        height = int(int(sl['height'])/10*3.78)
        pitch = int(int(sl['pitch'])/10*3.78)
        base_width = int(int("1150")/10*3.78)
        x_mergin = int((base_width-width)/2)
        y_mergin = int((pitch-height)/2)
        im = Image.new("RGB", (base_width, pitch), (128, 128, 128))
        draw = ImageDraw.Draw(im)
        draw.rectangle((x_mergin, y_mergin, width, height))

    # --- define format ----
    sf = conf['setFormat']
    # buffer clear
    if sf['bufferClear'] == "True":
        command = f"C"
        ssend(command, sock)

    # PCs
    pcs = sf['PC']
    for pc in pcs:
        align = ""
        if 'align' in pc:
            align = f",{pc['align']}"
        if 'autoLineFeed' in pc:
            align = f",P5{pc['autoLineFeed']['width']}{pc['autoLineFeed']['pitch']}{pc['autoLineFeed']['rowMax']}"

        command = f"PC{pc['number']};{pc['x']},{pc['y']},{pc['xR']},{pc['yR']},{pc['fontType']},{pc['fontSpace']},{pc['fontDeco']}{align}"
        ssend(command, sock)
        if IS_IMAGE:
            x1 = int(int(pc['x'])/10*3.78)+x_mergin
            y1 = int(int(pc['y'])/10*3.78)+y_mergin
            #width = int(int(pc['width'])/10*3.78)
            width = 50
            x2 = x1 + width
            y2 = x2 - 20
            draw.rectangle((x1, y1, x2, y1))
            font = ImageFont.truetype('ipaexg.ttf', 12)
            draw.multiline_text((x1,y1), 'Pillow sample', anchor="ls",fill=(0, 0, 0), font=font)


    # XB_QR
    xbqrs = sf['XB_QR']
    for xq in xbqrs:
        command = f"XB{xq['number']};{xq['x']},{xq['y']},T,{xq['errorLevel']},{xq['cellSize']},{xq['mode']},{xq['rotation']},{xq['model']}"
        ssend(command, sock)

    # XB_BAR
    xbs = sf['XB_BAR']
    for xb in xbs:
        command = f"XB{xb['number']};{xb['x']},{xb['y']},{xb['type']},{xb['digit']},{xb['width']},{xb['rotation']},{xb['height']},+0000000000,000,{xb['outNumber']},{xb['zeroSup']}"
        ssend(command, sock)

    # data
    fields = conf['fields'] if 'fields' in conf else []
    data = conf['data'] if 'data' in conf else [{}]

    for d in data:
        for f in fields:
            # print(f)
            default_v = f['default'] if 'default' in f else ""
            bind_v = default_v
            if 'bind' in f:
                bind_key = f['bind']
                bind_v = d[bind_key] if bind_key in d else default_v

            if f['command'] == "RC":
                command = f"RC{f['number']};{bind_v}"
                ssend(command, sock)
            if f['command'] == "RB":
                command = f"RB{f['number']};{bind_v}"
                ssend(command, sock)
            if f['command'] == "XS":
                command = f"XS;I,{f['copies']},{f['cutInterval']}{f['censorType']}{f['mode']}{f['speed']}{f['ribbon']}{f['tagRotation']}{f['statusResponse']}"
                ssend(command, sock)

    # final
    finals = conf['final']
    for fin in finals:
        if fin['command'] == "IB":
            command = f"IB"
            ssend(command, sock)
    if IS_IMAGE:
        im.save(IMAGE_FILE_PATH, quality=95)

    sock.shutdown(socket.SHUT_RDWR)
    sock.close()

    return True


# ------- initial ---------
if __name__ == '__main__':

    jsonc_filepath = 'print_conf_ip.jsonc'
    encoding = 'utf-8'
    prt_encoding = 'cp932'

    args = sys.argv
    if len(args) == 1:
        pass
    elif len(args) == 2:
        jsonc_filepath = args[1]
    else:
        print("パラメータエラー\n")
        sys.exit()

    conf = read_jsonc_file(jsonc_filepath)
    if conf:
        tpcl_maker(conf)
