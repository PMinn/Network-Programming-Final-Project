import time
from Device import Device

class Supporter(Device):
    def __init__(self, socket, address):
        super().__init__(socket, address)
        self.hostname = ""
        self.lastCheckTime = time.time()

    def setHostname(self, hostname):
        self.hostname = hostname

    def checkTime(self):
        self.lastCheckTime = time.time()

    def __str__(self):
        return f"{str(self.hostname)},{str(self.address[0])},{str(self.address[1])},{str(self.lastCheckTime)}"

    def toJSON(self):
        json = "{"
        json += f'"hostname":"{str(self.hostname)}","ip":"{str(self.address[0])}","port":{str(self.address[1])},"lastCheckTime":{str(self.lastCheckTime)}'
        json += "}"
        return json