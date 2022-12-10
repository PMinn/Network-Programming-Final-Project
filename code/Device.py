import uuid

class Device():
    def __init__(self, TCPsocket, TCPaddress, uid = None):
        self.TCPsocket = TCPsocket
        self.TCPaddress = TCPaddress
        if uid == None:
            self.uid = uuid.uuid5(uuid.NAMESPACE_DNS, f'{TCPaddress[0]}:{TCPaddress[1]}').hex
        else:
            self.uid = uid
        self.UDPaddress = None
        self.isRuning = False
        self.connectTarget = ""
        self.screen_width = 0
        self.screen_height = 0

    def setUID(self, uid):
        self.uid = uid

    def setUDP(self, UDPaddress):
        self.UDPaddress = UDPaddress

    def setSize(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height