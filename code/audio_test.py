import pyaudio
import wave
import eel
import threading
import base64

eel.init('web', allowed_extensions=['.js', '.html'])
def openWindow():
    eel.start('audio.html', size=(1000, 800))  # Start
t = threading.Thread(target=openWindow)
t.start()

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* recording")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

byte_data = b''.join(frames)
# print()
base64_str = str(base64.b64encode(byte_data))

eel.getAudio(base64_str[2:-1])