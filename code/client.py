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
page = "index"

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

@eel.expose
def changePage(targetPage):
    global page
    page = targetPage
    return targetPage

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

def checkControl():
    while 1:
        data, address = UDPSocket.recvfrom(BUF_SIZE)
        data = data.decode("utf-8").split(",")
        if data[0]=='mm':
            position = data[1].split("@")
            pyautogui.moveTo(int(position[0]), int(position[1])) 

def sending(address):
    imgId = int(0)
    while isSending:
        splitedData = dataSplit(getScreenshotToBase64()+'@')
        for data in splitedData:
            UDPSocket.sendto(('{:06d}'.format(imgId) + data).encode('utf-8'), address)
            time.sleep(0.04166667/len(splitedData))
            # 24fps == 0.04166667
        imgId += 1

def supporterMainThread():
    global isSending
    while 1:
        msg = TCPSocket.recv(BUF_SIZE)
        data = msg.decode('utf-8').split(',')
        if data[0] == 'connect':
            isSending = True
            address = data[1].split(':')
            address = (address[0],int(address[1]))
            threading.Thread(target=checkControl).start()
            threading.Thread(target=sending, args=(address,)).start()
        elif data[0] == "disconnect":
            isSending = False
            print("Supporter get disconnect")

@eel.expose
def signSupporter(hostname):
    print("signSupporter")
    TCPSocket.send(f"signSupporter,{hostname}".encode('utf-8'))
    # threading.Thread(target=sendCheckTime).start()
    threading.Thread(target=supporterMainThread).start()
    
''' end supporter '''

''' access '''
targetUid = None
isRecving = False

@eel.expose
def getSupporter():
    TCPSocket.send("getSupporter".encode('utf-8'))
    msg = TCPSocket.recv(BUF_SIZE)
    msg_utf8 = msg.decode('utf-8')
    return msg_utf8

def getImageThread():
    UDPSocket.setblocking(False)
    while isRecving:
        data = ""
        imgId = 0
        while len(data) == 0 or data[-1] != '@' and isRecving:
            try:
                server_reply, reServerAddress = UDPSocket.recvfrom(BUF_SIZE)
            except:
                pass
            else:
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
    UDPSocket.setblocking(True)

@eel.expose
def connect2Supporter(uid):
    global BUF_SIZE, reServerAddress, imageThread, targetUid, isRecving
    isRecving = True
    targetUid = uid
    TCPSocket.send(f"connect,{uid}".encode('utf-8'))
    msg = TCPSocket.recv(BUF_SIZE)
    addr = msg.decode('utf-8').split(':')
    reServerAddress = (addr[0],int(addr[1]))
    BUF_SIZE = 65000
    imageThread = threading.Thread(target=getImageThread)
    imageThread.start()

@eel.expose
def mousemove(x,y):
    UDPSocket.sendto(f"mm,{int(x)}@{int(y)}".encode('utf-8'), reServerAddress)

''' end access '''

def close_callback(strPath, sockets):
    global BUF_SIZE, reServerAddress, imageThread, targetUid, isRecving, isSending
    print(f"close:{strPath},{sockets}")
    if strPath == "show.html": # connected access close
        isRecving = False
        TCPSocket.send(f"disconnect,{targetUid}".encode('utf-8'))
        TCPSocket.close()
        sys.exit()
    elif strPath == "support.html": # support close
        if isSending:
            isSending = False
            TCPSocket.send(f"disconnect,{targetUid}".encode('utf-8'))
            TCPSocket.close()
            sys.exit()
        else:
            TCPSocket.send("offline".encode('utf-8'))
            TCPSocket.close()
            sys.exit()
    elif strPath == "access.html": # access close
        if page == "access":
            TCPSocket.send(f"offline".encode('utf-8'))
            TCPSocket.close()
            sys.exit()
    elif strPath == "index.html": # access close
        if page == "index":
            TCPSocket.send(f"offline".encode('utf-8'))
            TCPSocket.close()
            sys.exit()

eel.start('index.html', size=(1000, 1000), port=0, close_callback=close_callback)  # Start
TCPSocket.close()