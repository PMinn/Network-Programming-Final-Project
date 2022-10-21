import socket
import threading
#ver web
import eel

BUF_SIZE = 65000

eel.init('web', allowed_extensions=['.js', '.html'])
UDPSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

class Thread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.start()
    def run(self):
        UDPSocket.settimeout(20)
        UDPSocket.sendto("start".encode('utf-8'), ("127.0.0.1",8888))
        while 1:
            data = ""
            while len(data) == 0 or data[-1] != '@':
                server_reply, reServerIp = UDPSocket.recvfrom(BUF_SIZE)
                data += server_reply.decode("utf-8")
            # print(data)
            img = f'data:image/png;base64,{data[:-1]}'
            eel.readImg(img)

def close_callback():
    UDPSocket.close()

Thread()
eel.start('show.html', size=(1000, 800))  # Start
UDPSocket.close()
# , close_callback=close_callback