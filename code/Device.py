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

    def setUID(self, uid):
        self.uid = uid

    def setUDP(self, UDPaddress):
        self.UDPaddress = UDPaddress