import eel
import socket
import time
import threading
import sys
import pyautogui
import base64
from io import BytesIO

TCP_PORT = 6666
UDP_PORT = 8888
BUF_SIZE = 1024
serverIP = "127.0.0.1"
reServerAddress = None
imageThread = None

eel.init('web', allowed_extensions=['.js', '.html'])

TCPSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
TCPSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
UDPSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    TCPSocket.connect((serverIP, TCP_PORT))
    uidCode = TCPSocket.recv(BUF_SIZE)
    UDPSocket.sendto(uidCode, (serverIP, UDP_PORT))
    msg = TCPSocket.recv(BUF_SIZE).decode('utf-8')
    while msg != 'A':
        UDPSocket.sendto(uidCode, (serverIP, UDP_PORT))
        msg = TCPSocket.recv(BUF_SIZE).decode('utf-8')
except Exception as msg:
    print("err:"+str(msg))

@eel.expose
def gethostname():
    return socket.gethostname()

''' supporter '''
isSending = False
def sendCheckTime():
    while True:
        time.sleep(60)
        TCPSocket.send("checkTime".encode('utf-8'))

def dataSplit(data):
    result = []
    n = 60000
    for idx in range(0, len(data), n):
        result.append(data[idx : idx + n])
    return result

def getScreenshotToBase64():
    img = pyautogui.screenshot() # PIL.Image.Image
    width, height = img.size
    # img = img.resize((width//2, height//2))
    output_buffer = BytesIO()
    img.save(output_buffer, format='webp')
    byte_data = output_buffer.getvalue()
    base64_str = str(base64.b64encode(byte_data))
    return base64_str[2:-1]

def checkClose():
    global isSending
    msg = TCPSocket.recv(BUF_SIZE)
    data = msg.decode('utf-8')
    if data=="closeShow":
        isSending = False
        print("closeShow")

@eel.expose
def signSupporter(hostname):
    global isSending
    print("signSupporter")
    TCPSocket.send(f"signSupporter,{hostname}".encode('utf-8'))
    threading.Thread(target=sendCheckTime).start()
    msg = TCPSocket.recv(BUF_SIZE)
    data = msg.decode('utf-8').split(',')
    if data[0] == 'connect2Supporter':
        isSending = True
        address = data[1].split(':')
        address = (address[0],int(address[1]))
        imgId = int(0)
        threading.Thread(target=checkClose).start()
        while isSending:
            splitedData = dataSplit(getScreenshotToBase64()+'@')
            # data = getScreenshotToBase64()+'@'
            for data in splitedData:
                UDPSocket.sendto(('{:06d}'.format(imgId) + data).encode('utf-8'), address)
                time.sleep(0.04166667/len(splitedData))
                # 24fps == 0.04166667
            imgId += 1

''' access '''
targetUid = None
@eel.expose
def getSupporter():
    TCPSocket.send("getSupporter".encode('utf-8'))
    msg = TCPSocket.recv(BUF_SIZE)
    msg_utf8 = msg.decode('utf-8')
    return msg_utf8

def getImageThread():
    while 1:
        data = ""
        imgId = 0
        while len(data) == 0 or data[-1] != '@':
            server_reply, reServerAddress = UDPSocket.recvfrom(BUF_SIZE)
            data_utf8 = server_reply.decode("utf-8")
            newImgId = int(data_utf8[0:6])
            if newImgId == imgId:
                data += data_utf8[6:]
            elif newImgId > imgId:
                imgId = newImgId
                data = data_utf8[6:]
        if len(data) > 0 and data[-1] == '@':
            img = f'data:image/png;base64,{data[:-1]}'
            eel.readImg(img)

@eel.expose
def connect2Supporter(uid):
    global BUF_SIZE, reServerAddress, imageThread, targetUid
    targetUid = uid
    BUF_SIZE = 65000
    TCPSocket.send(f"connect2Supporter,{uid}".encode('utf-8'))
    imageThread = threading.Thread(target=getImageThread)
    imageThread.start()

@eel.expose
def mousemove(x,y):
    print(x,y)

def close_callback(strPath, sockets):
    print(f"close:{strPath},{sockets}")
    if strPath=="show.html":
        TCPSocket.send(f"closeShow,{targetUid}".encode('utf-8'))
        TCPSocket.close()
        sys.exit()

eel.start('index.html', size=(1000, 1000), port=0, close_callback=close_callback)  # Start
TCPSocket.close()