class DevicesList(list):
    def find(self, uid):
        for device in self:
            print(device.uid, ' == ', uid , ' ', device.uid == uid)
            if device.uid == uid:
                return device
        return None

    def __str__(self):
        json = '['
        for i in range(len(self)):
            json += str(self[i])
            if i != len(self)-1:
                json += ','
        json += ']'
        return json