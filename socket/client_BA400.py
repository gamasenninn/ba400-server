# ソケットライブラリ取り込み
import socket
import threading
import sys

# サーバーIPとポート番号
IPADDR = "192.168.11.205"
PORT = 9100

sinfo = socket.getaddrinfo(IPADDR, PORT)
print("info:",sinfo)

#sys.exit()

# ソケット作成
sock = socket.socket(socket.AF_INET,0,0)

# サーバーへ接続
sock.connect((IPADDR, PORT))


# データ受信関数
def recv_data(sock):
    while True:
        try:
            data = sock.recv(1024)
            if data == b"":
                break
            print(data.decode("utf-8"))
        except ConnectionResetError:
            break
        except OSError:
            break


# データ受信をサブスレッドで実行
thread = threading.Thread(target=recv_data, args=(sock,))
thread.start()

while True:
    com_str = input("> ")
    if com_str == '':  #空打ちの場合
        continue
    if com_str == 'quit': #quitで終了
        break

    # コマンド作成
    b_com = b'\x1b' +com_str.encode('utf-8') + b'\x0a\x00'
    print(b_com)

    # コマンド送信
    sock.send(b_com)

sock.shutdown(socket.SHUT_RDWR)
sock.close()
