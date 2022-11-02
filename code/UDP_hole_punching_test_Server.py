import socket

#建立 UDP Scoket
UDPSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#監聽 所有IP的 3386 端口 
listen_addr = ("", 3386)
UDPSock.bind(listen_addr)

#儲存IP用的 Array
ips = []

while True:
    #接收資料
    data, addr = UDPSock.recvfrom(1024)
    print(addr , 'is connected.')
    #將Client IP:Port 儲存到Array內
    ips.append(str(addr[0]) + ':' + str(addr[1]))
    #當第二個Client連上時，進行IP交換動作
    if len(ips) == 2:
        dest = ''
        for ip in ips:
            for i in ips:
                if ip != i:
                    dest = i # 對方的IP
                #將A的IP傳給B，B的IP傳給A
                print(f"send {dest} to {ip}")
                UDPSock.sendto(str(dest).encode('utf-8'), (ip.split(':')[0],int(ip.split(':')[1])))
    