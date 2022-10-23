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
            imgId = 0
            while len(data) == 0 or data[-1] != '@':
                server_reply, reServerIp = UDPSocket.recvfrom(BUF_SIZE)
                data_utf8 = server_reply.decode("utf-8")
                newImgId = int(data_utf8[0:6])
                print(newImgId)
                if newImgId == imgId:
                    data += data_utf8[6:]
                elif newImgId > imgId:
                    imgId = newImgId
                    data = data_utf8[6:]
            if len(data) > 0 and data[-1] == '@':
                print('show')
                img = f'data:image/png;base64,{data[:-1]}'
                eel.readImg(img)

def close_callback():
    UDPSocket.close()

Thread()
eel.start('show.html', size=(1000, 800))  # Start
UDPSocket.close()
# , close_callback=close_callback