from config import episodes, supes
import datafile
import numpy as np
import matplotlib.pyplot as plt
from colour import Color


i = 0
voters = set()
votens = {}
for ep in episodes:
    print(ep['epnumber'])
    epusers = set()
    validVotes = list(ep['translation'].keys())
    votessorted = sorted(datafile.loadData(ep['dataFilename'])['votes'], key=lambda k: k['date'])
    for vote in votessorted:
        if vote['vote'] in validVotes:
            if vote['user'] not in votens:
                votens[vote['user']] = 0
            votens[vote['user']] += 1
            if not supes or (i == 0):
                voters.add(vote['user'])
            if supes:
                epusers.add(vote['user'])
    if supes:
        print(len(epusers))
        voters = voters.intersection(epusers)
        #for user in voters.copy():
        #    if user not in epusers:
        #        voters.remove(user)
    print(len(voters))
    i = i + 1

occurences = {}
for n in votens.values():
    if n not in occurences:
        occurences[n] = 0
    occurences[n] += 1

maxvotes = len(episodes)
colorseries = list(Color("yellow").range_to(Color("purple"), maxvotes+1))
#colorseries = ["#000", "#111", "#222", "#333", "#444", "#555", "#666", "#777", "#888", "#999", "#AAA", "#BBB", "#CCC"]
labels = range(1,maxvotes+1)
eplabels = []
epocs = {}
for ep in episodes:
    eplabels.append(ep['epnumber'])
    epusers = set()
    validVotes = list(ep['translation'].keys())
    votessorted = sorted(datafile.loadData(ep['dataFilename'])['votes'], key=lambda k: k['date'])
    epoccurences = {}
    for vote in votessorted:
        if vote['vote'] in validVotes:
            n = votens[vote['user']]
            if n not in epoccurences:
                epoccurences[n] = 0
            epoccurences[n] += 1
    epocs[ep['epnumber']] = epoccurences
    print(ep['epnumber'], epoccurences)

fig, ax = plt.subplots()
lastbar = np.zeros(maxvotes)
print("lb", lastbar)
for label in reversed(labels):
    data = []
    for ep in eplabels:
        data.append(epocs[ep][label])
    print(label, data)
    data = np.array(data)
    ax.bar(eplabels, data, 0.5, label=label, bottom=lastbar, color=colorseries[label].hex)
    lastbar = lastbar+data

ax.set_ylabel('votes')
ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05), ncol=maxvotes//2)
plt.show()

print(occurences)
datafile.saveData("vlist.msgp", list(voters))
