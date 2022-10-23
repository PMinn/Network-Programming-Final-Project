import pyautogui
import base64
from io import BytesIO
import time
import socket

# myScreenshot.show()
# myScreenshot.save('111.png')
import threading

import math
import sys

BUF_SIZE = 1024			# Receive buffer size

UDPSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDPSocket.bind(('', 8888))
# TCPSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# TCPSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# TCPSocket.bind(('', 6666))
# TCPSocket.listen(1)

def dataSplit(data):
    result = []
    n = 60000
    for idx in range(0, len(data), n):
        result.append(data[idx : idx + n])
    return result

def getScreenshotToBase64():
    img = pyautogui.screenshot() # PIL.Image.Image
    width, height = img.size
    img = img.resize((width//2, height//2))
    output_buffer = BytesIO()
    img.save(output_buffer, format='PNG')
    byte_data = output_buffer.getvalue()
    base64_str = str(base64.b64encode(byte_data))
    return base64_str[2:-1]

class Thread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.start()
    def run(self):
        client_msg, clientIp = UDPSocket.recvfrom(BUF_SIZE)
        imgId = int(0)
        while 1:
            splitedData = dataSplit(getScreenshotToBase64()+'@')
            print(sys.getsizeof(splitedData))
            for data in splitedData:
                UDPSocket.sendto(('{:06d}'.format(imgId) + data).encode('utf-8'), clientIp)
            imgId += 1
            time.sleep(0.1)
Thread()