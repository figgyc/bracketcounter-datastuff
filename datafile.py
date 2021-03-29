import json, msgpack

def loadData(filename):
    if str(filename).endswith("msgp"):
        return msgpack.load(open(filename, "rb"))
    else: # json
        return json.loads(open(filename, "rb").read())

def saveData(filename, data):
    with open(filename, "wb") as fileStream:
        if str(filename).endswith("msgp"):
            msgpack.dump(data, fileStream)
        else: # json
            fileStream.write(json.dumps(data))
