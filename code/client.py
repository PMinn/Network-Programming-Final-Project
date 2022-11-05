import eel
import socket

# Set web files folder
eel.init('web', allowed_extensions=['.js', '.html'])

@eel.expose
def gethostname():
    return socket.gethostname()

eel.start('index.html', size=(1000, 1000))  # Start