from jsonc_parser.parser import JsoncParser
import socket
import sys

# --- config value ------
IS_SEND = False
IS_LOG = True
LOG_FILE_PATH = "tpcl_send.log"
SOCKET_TIME_OUT = 5

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
