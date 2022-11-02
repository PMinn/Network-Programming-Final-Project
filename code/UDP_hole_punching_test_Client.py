import socket
from threading import Thread
from time import sleep
 
UDPSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
 
data = 'hello'
#先連線到公開的伺服器
addr = ("127.0.0.1", 3386)
 
#接收到封包之後傳給另一台躲在NAT後的主機
def threaded_function(rip):
    for i in range(100):
        print('Send ' , i ,'to ', rip)
        UDPSock.sendto(str(i).encode('utf-8'), rip)
        sleep(1)
 
#先丟給SERVER封包，讓伺服器取得IP資訊
UDPSock.sendto(data.encode('utf-8'),addr)
#接收伺服器回傳的另一台主機IP:PORT
dest, adr = UDPSock.recvfrom(1024)
dest = dest.decode('utf-8').split(',')
if(dest[0] == 'connect'):
    print(f"send ping to {dest[1]}")
    dest = dest[1].split(':')
    rip = (dest[0], int(dest[1]))
    #進行打洞
    UDPSock.sendto('ping,'.encode('utf-8'), rip)
    thread = Thread(target = threaded_function, args = (rip, ))
    thread.start()

#持續接收封包
while True:
    data, adr = UDPSock.recvfrom(1024)
    print(f'Recv {data.decode("utf-8")} from {adr}')