from Device import Device

class Supporter(Device):
    def __init__(self, device, hostname):
        super().__init__(device.TCPsocket, device.TCPaddress, device.uid)
        super().setUDP(device.UDPaddress)
        self.hostname = hostname

    def __str__(self):
        json = "{"
        json += f'"hostname":"{str(self.hostname)}","ip":"{str(self.TCPaddress[0])}","port":{str(self.TCPaddress[1])},"uid":"{str(self.uid)}","isRuning":"{str(self.isRuning)}"'
        json += "}"
        return json