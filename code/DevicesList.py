class DevicesList(list):
    def find(self, uid):
        for device in self:
            if device.uid == uid:
                return device
        return None

    def removeDevice(self, targetDevice):
        for device in self:
            if device.uid == targetDevice.uid:
                self.remove(device)
                return True
        return False

    def __str__(self):
        json = '['
        for i in range(len(self)):
            json += str(self[i])
            if i != len(self)-1:
                json += ','
        json += ']'
        return json