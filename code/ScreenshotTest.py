import pyautogui
import base64
from io import BytesIO
import time
# myScreenshot.show()
# myScreenshot.save('111.png')
import threading
#ver web
import eel
import random

eel.init('web', allowed_extensions=['.js', '.html'])

def image_to_base64():
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
        img = f'data:image/png;base64,{image_to_base64()}'
        eel.readImg(img)
Thread()
eel.start('show.html', size=(500, 500))  # Start
