import socket
import threading
from Supporter import Supporter
from SupportersList import SupportersList

PORT = 6666
backlog = 5
BUF_SIZE = 1024	

supporters = SupportersList()

TCPSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
TCPSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
TCPSocket.bind(('', PORT))
TCPSocket.listen(backlog)


def createThread(clientSocket, rAddress):
    supporter = Supporter(clientSocket, rAddress)
    client_msg = clientSocket.recv(BUF_SIZE)
    while client_msg:
        client_utf8 = client_msg.decode('utf-8')
        print(client_utf8)
        data = client_utf8.split(',')
        if data[0] == 'signSupporter':
            supporter.setHostname(data[1])
            supporters.append(supporter)
            print(supporter)
        elif data[0] == 'checkTime':
            supporter.checkTime()
        elif data[0] == 'getSupporter':
            clientSocket.send(supporters.toJSON().encode('utf-8'))
        client_msg = clientSocket.recv(BUF_SIZE)
        # clientSocket.close()

try:
    while True:
        clientSocket, rAddress = TCPSocket.accept()
        print(str(rAddress[0])+" : "+str(rAddress[1]))
        try:
            t = threading.Thread(target=createThread,args=(clientSocket, rAddress))
            t.start()
        except socket.error as msg:
            print("socket error:"+str(msg))
except KeyboardInterrupt:
    TCPSocket.close()
    pass