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
page = "index"

eel.init('web', allowed_extensions=['.js', '.html'])

TCPSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
TCPSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
UDPSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

screen_width, screen_height = pyautogui.size()

try:
    TCPSocket.connect((serverIP, TCP_PORT))
    uidCode = TCPSocket.recv(BUF_SIZE)
    remsg = f"{uidCode.decode('utf-8')},{screen_width},{screen_height}".encode('utf-8')
    UDPSocket.sendto(remsg, (serverIP, UDP_PORT))
    msg = TCPSocket.recv(BUF_SIZE).decode('utf-8')
    while msg != 'A':
        UDPSocket.sendto(remsg, (serverIP, UDP_PORT))
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
isSupport = False

def dataSplit(data):
    result = []
    n = 60000
    for idx in range(0, len(data), n):
        result.append(data[idx : idx + n])
    return result

def getScreenshotToBase64():
    img = pyautogui.screenshot() # PIL.Image.Image
    # width, height = img.size
    img = img.resize((screen_width//2, screen_height//2))
    output_buffer = BytesIO()
    img.save(output_buffer, format='webp')
    byte_data = output_buffer.getvalue()
    base64_str = str(base64.b64encode(byte_data))
    return base64_str[2:-1]

def checkControl():
    while isSending:
        UDPSocket.settimeout(2)
        try:
            data, address = UDPSocket.recvfrom(BUF_SIZE)
            data = data.decode("utf-8").split(",")
            if data[0] == 'mm':
                position = data[1].split("@")
                pyautogui.moveTo(int(position[0]), int(position[1])) 
            elif data[0] == 'kd':
                pyautogui.keyDown(data[1])
            elif data[0] == 'ku':
                pyautogui.keyUp(data[1])
            elif data[0] == 'mdl':
                position = data[1].split("@")
                pyautogui.mouseDown(x=int(position[0]), y=int(position[1]))
            elif data[0] == 'mul':
                position = data[1].split("@")
                pyautogui.mouseUp(x=int(position[0]), y=int(position[1]))
            elif data[0] == 'mdr':
                position = data[1].split("@")
                pyautogui.mouseDown(x=int(position[0]), y=int(position[1]), button='right')
            elif data[0] == 'mur':
                position = data[1].split("@")
                pyautogui.mouseUp(x=int(position[0]), y=int(position[1]), button='right')
            elif data[0] == 'wl':
                value = data[1].split("@")
                pyautogui.hscroll(int(value[0]))
                pyautogui.vscroll(int(value[1]))
        except:
            pass

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
    global isSending, isSupport
    isSupport = True
    while isSupport:
        TCPSocket.settimeout(1)
        try:
            msg = TCPSocket.recv(BUF_SIZE)
        except:
            pass
        else:
            data = msg.decode('utf-8').split(',')
            if data[0] == 'connect':
                isSending = True
                address = data[1].split(':')
                address = (address[0],int(address[1]))
                threading.Thread(target=checkControl, name="checkControl").start()
                threading.Thread(target=sending, args=(address,), name="sending").start()
                eel.supporterConnected(data[1])
            elif data[0] == "disconnect":
                isSending = False
                eel.supporterDisonnected()
                print("Supporter get disconnect")

@eel.expose
def signSupporter(hostname):
    print("signSupporter")
    TCPSocket.send(f"signSupporter,{hostname}".encode('utf-8'))
    threading.Thread(target=supporterMainThread, name="SMT").start()

@eel.expose
def supporterDisconnect():
    global isSending
    TCPSocket.send("disconnect2A".encode('utf-8'))
    isSending = False
    BUF_SIZE = 1024
    return 0

''' end supporter '''

''' access '''
targetUid = None
isRecving = False

@eel.expose
def printThread():
    for thread in threading.enumerate(): 
        print(thread.name)

@eel.expose
def getSupporter():
    TCPSocket.send("getSupporter".encode('utf-8'))
    msg = TCPSocket.recv(BUF_SIZE)
    msg_utf8 = msg.decode('utf-8')
    return msg_utf8

def getImageThread():
    while isRecving:
        data = ""
        imgId = 0
        while (len(data) == 0 or data[-1] != '@') and isRecving:
            UDPSocket.settimeout(0.1)
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

def TCPThread():
    global isRecving, BUF_SIZE
    while isRecving:
        TCPSocket.settimeout(1)
        try:
            msg = TCPSocket.recv(BUF_SIZE)
        except:
            pass
        else:
            data = msg.decode('utf-8').split(',')
            print(data)
            if data[0] == 'disconnect':
                isRecving = False
                BUF_SIZE = 1024
                eel.targetDisconnect()
                break

@eel.expose
def connect2Supporter(uid):
    global BUF_SIZE, reServerAddress, targetUid, isRecving
    isRecving = True
    targetUid = uid
    TCPSocket.send(f"connect,{uid}".encode('utf-8'))
    msg = TCPSocket.recv(BUF_SIZE)
    data = msg.decode('utf-8').split(',')
    addr = data[0].split(":")
    reServerAddress = (addr[0],int(addr[1]))
    eel.setImgSize(int(data[1]),int(data[2]))
    BUF_SIZE = 65000
    threading.Thread(target=getImageThread, name="getImageThread").start()
    threading.Thread(target=TCPThread, name="TCPThread").start()

@eel.expose
def mousemove(x,y):
    UDPSocket.sendto(f"mm,{int(x)}@{int(y)}".encode('utf-8'), reServerAddress)

@eel.expose
def mousedownLeft(x,y):
    UDPSocket.sendto(f"mdl,{int(x)}@{int(y)}".encode('utf-8'), reServerAddress)

@eel.expose
def mousedownRight(x,y):
    UDPSocket.sendto(f"mdr,{int(x)}@{int(y)}".encode('utf-8'), reServerAddress)

@eel.expose
def mouseupLeft(x,y):
    UDPSocket.sendto(f"mul,{int(x)}@{int(y)}".encode('utf-8'), reServerAddress)

@eel.expose
def mouseupRight(x,y):
    UDPSocket.sendto(f"mur,{int(x)}@{int(y)}".encode('utf-8'), reServerAddress)

@eel.expose
def wheel(x,y):
    UDPSocket.sendto(f"wl,{int(x)}@{int(y)}".encode('utf-8'), reServerAddress)

@eel.expose
def keydown(key):
    UDPSocket.sendto(f"kd,{key}".encode('utf-8'), reServerAddress)

@eel.expose
def keyup(key):
    UDPSocket.sendto(f"ku,{key}".encode('utf-8'), reServerAddress)

@eel.expose
def accessDisconnect():
    global BUF_SIZE, isRecving, page
    TCPSocket.send(f"disconnect2S,{targetUid}".encode('utf-8'))
    isRecving = False
    BUF_SIZE = 1024
    page = "access"
    return page

''' end access '''

def close_callback(strPath, sockets):
    global BUF_SIZE, isRecving, isSending, isSupport
    print(f"close:{strPath},{sockets}")
    if strPath == "show.html": # connected access close
        if page == "show":
            if isRecving:
                isRecving = False
                TCPSocket.send(f"disconnect2S+offline,{targetUid}".encode('utf-8'))
                TCPSocket.close()
                sys.exit()
            else:
                isRecving = False
                TCPSocket.send(f"offline".encode('utf-8'))
                TCPSocket.close()
                sys.exit()
        # else:
        #     BUF_SIZE = 1024
        #     isRecving = False
    elif strPath == "support.html": # support close
        if isSending:
            isSending = False
            isSupport = False
            TCPSocket.send("disconnect2A+offline".encode('utf-8'))
            time.sleep(1.5)
            TCPSocket.close()
            sys.exit()
        else:
            isSending = False
            isSupport = False
            TCPSocket.send("offline".encode('utf-8'))
            time.sleep(1.5)
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