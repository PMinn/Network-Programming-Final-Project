import pyautogui
from io import BytesIO
import base64

def dataSplit(data):
    result = []
    n = 60000
    for idx in range(0, len(data), n):
        result.append(data[idx : idx + n])
    return result

def getScreenshotToBase64(screen_width, screen_height):
    img = pyautogui.screenshot() # PIL.Image.Image
    # width, height = img.size
    img = img.resize((screen_width//2, screen_height//2))
    output_buffer = BytesIO()
    img.save(output_buffer, format='webp')
    byte_data = output_buffer.getvalue()
    base64_str = str(base64.b64encode(byte_data))
    return base64_str[2:-1]
