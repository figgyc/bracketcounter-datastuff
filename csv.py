import matplotlib.pyplot as plt, mpld3
from config import ep2 as tep
from config import ci
import numpy
import datafile

def colpad(string, n):
    return " "*(n-len(string))

def col(string, n, left=False):
    if left:
        return colpad(str(string), n) + str(string)
    else:
        return str(string) + colpad(str(string), n)

def csv(ep):
    out = ""
    data = datafile.loadData(ep['dataFilename'])
    votessorted = sorted(data['votes'], key=lambda k: k['date'])

    epoch = data["epoch"]
    for vote in votessorted:
         time = int( (vote['date'] - epoch) / 1000)
         out += vote['vote'] + "," + str(time) + "\n"
    return out

if __name__ == "__main__":
    out = csv(tep)
    print(out)
