import socket
import threading
from Supporter import Supporter
from Device import Device
from DevicesList import DevicesList
import time

TCP_PORT = 6666
UDP_PORT = 8888
backlog = 5
BUF_SIZE = 1024	

supporters = DevicesList()
devices = DevicesList()

TCPSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
TCPSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
TCPSocket.bind(('', TCP_PORT))
TCPSocket.listen(backlog)
UDPSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDPSocket.bind(('', UDP_PORT))

def mainThread(clientSocket, rAddress):
    # init
    device = Device(clientSocket, rAddress)
    print('register',device.uid)
    devices.append(device)
    clientSocket.send(str(device.uid).encode('utf-8'))
    time.sleep(0.5)
    while device.UDPaddress == None:
        clientSocket.send("E".encode('utf-8'))
        time.sleep(1)
    clientSocket.send("A".encode('utf-8'))
    # end init
    client_msg = clientSocket.recv(BUF_SIZE)
    while client_msg:
        client_utf8 = client_msg.decode('utf-8')
        data = client_utf8.split(',')
        if data[0] == 'signSupporter':
            device = Supporter(device, data[1])
            supporters.append(device)
            print(device)
        elif data[0] == 'checkTime':
            device.checkTime()
        elif data[0] == 'getSupporter':
            clientSocket.send(str(supporters).encode('utf-8'))
        elif data[0] == 'connect2Supporter':
            targetSupporter = supporters.find(data[1])
            clientSocket.send(f"{targetSupporter.UDPaddress[0]}:{targetSupporter.UDPaddress[1]}".encode('utf-8'))
            targetSupporter.TCPsocket.send(f'connect2Supporter,{device.UDPaddress[0]}:{device.UDPaddress[1]}'.encode('utf-8'))
            targetSupporter.isRuning = True
        elif data[0] == 'disconnection':
            targetSupporter = supporters.find(data[1])
            targetSupporter.TCPsocket.send('disconnection'.encode('utf-8'))
            targetSupporter.isRuning = False
        elif data[0] == 'unsupport':
            targetSupporter = supporters.find(data[1])
            targetSupporter.TCPsocket.send('disconnection'.encode('utf-8'))
            targetSupporter.isRuning = False

        try:
            client_msg = clientSocket.recv(BUF_SIZE)
        except:
            supporters.removeDevice(device)
            devices.removeDevice(device)
            print(f"device ({device.uid}) offline")
            clientSocket.close()
            break

def UDPThread():
    while 1:
        try:
            UDPSocket.settimeout(5)
            data, address = UDPSocket.recvfrom(BUF_SIZE)
            targetUID = data.decode('utf-8')
            print(targetUID)
            targetDevices = devices.find(targetUID)
            if targetDevices != None:
                targetDevices.setUDP(address)
        except:
            pass

try:
    while True:
        clientSocket, rAddress = TCPSocket.accept()
        print(str(rAddress[0])+" : "+str(rAddress[1]))
        try:
            threading.Thread(target=mainThread,args=(clientSocket, rAddress)).start()
            threading.Thread(target=UDPThread).start()
        except socket.error as msg:
            print("socket error:"+str(msg))
except KeyboardInterrupt:
    TCPSocket.close()
    pass