import eel

eel.init('web', allowed_extensions=['.js', '.html'])
def close_callback(strPath, sockets):
    print("close")
eel.start('eelTest.html', size=(1000, 1000), port=0, close_callback=close_callback)  # Start
