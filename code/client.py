import eel
import socket
import time
import threading

PORT = 6666
BUF_SIZE = 1024
serverIP = "127.0.0.1"

eel.init('web', allowed_extensions=['.js', '.html'])

TCPSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
TCPSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
    TCPSocket.connect((serverIP, PORT))
except Exception as msg:
    print("err:"+str(msg))

@eel.expose
def gethostname():
    return socket.gethostname()

''' supporter '''
def sendCheckTime():
    while True:
        time.sleep(60)
        TCPSocket.send("checkTime".encode('utf-8'))

@eel.expose
def signSupporter(hostname):
    TCPSocket.send(f"signSupporter,{hostname}".encode('utf-8'))
    t = threading.Thread(target=sendCheckTime)
    t.start()


''' access '''
@eel.expose
def getSupporter():
    TCPSocket.send("getSupporter".encode('utf-8'))
    msg = TCPSocket.recv(BUF_SIZE)
    msg_utf8 = msg.decode('utf-8')
    return msg_utf8

eel.start('index.html', size=(1000, 1000), port=0)  # Start
TCPSocket.close()