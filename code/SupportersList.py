class SupportersList(list):
    def __init__(self):
        super().__init__()

    def __str__(self):
        data = ''
        for i in range(len(self)):
            data += str(self[i])
            if i != len(self)-1:
                data += '|'
        return data

    def toJSON(self):
        json = '['
        for i in range(len(self)):
            json += self[i].toJSON()
            if i != len(self)-1:
                json += ','
        json += ']'
        return json