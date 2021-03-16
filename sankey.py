import datafile
# bfb 19/20
from config import proportional, nMode, vMode
from config import ep1 as ep1t
from config import ep2 as ep2t

def getFactor(epn, char):
    if not proportional:
        return 100
    return totals[epn][char]

def sankey(ep1, ep2):

    json1 =datafile.loadData(ep1['dataFilename'])['votes']
    json2 =datafile.loadData(ep2['dataFilename'])['votes']

    vList = set()
    if vMode:
        vList = set(datafile.loadData("vlist.msgp"))

    if nMode:
        ep1['translation']['n'] = "Didn't vote"
        ep2['translation']['n'] = "Didn't vote"
        ep1['color']['n'] = "#cccccc"
        ep2['color']['n'] = "#cccccc"

    validVotes1 = list(ep1['translation'].keys())
    validVotes2 = list(ep2['translation'].keys())



    structure = {}
    totals = {'1': {}, '2': {}}
    usersFound = []
    for vote in validVotes1:
        structure[vote] = {}
        totals['1'][vote] = 0
        for vote2 in validVotes2:
            structure[vote][vote2] = 0
            totals['2'][vote2] = 0

    uvotes = {}
    for vote in json1:
        uvotes[vote['user']] = vote['vote']

    twovotes = []

    for vote in json2:
        twovotes.append(vote['user'])
        if vote['user'] in vList or not vMode:
            if vote['user'] in uvotes:
                structure[uvotes[vote['user']]][vote['vote']] += 1
                totals['1'][uvotes[vote['user']]] += 1
                totals['2'][vote['vote']] += 1
            else:
                if nMode:
                    structure['n'][vote['vote']] += 1
                    totals['1']['n'] += 1
                    totals['2'][vote['vote']] += 1

    if nMode:
        for vote in json1:
            if vote['user'] in vList or not vMode:
                if vote['user'] not in twovotes:
                    structure[vote['vote']]['n'] += 1
                    totals['1'][vote['vote']] += 1
                    totals['2']['n'] += 1

    totalTotal = {}
    totalTotal['1'] = sum(totals['1'].values())# - totals['1']['n']
    totalTotal['2'] = sum(totals['2'].values())# - totals['2']['n']

    for voteA in structure.keys():
        for voteB in structure[voteA].keys():
            print(f'{ep1["translation"][voteA]}{ep1["epnumber"]} [{structure[voteA][voteB] / (getFactor("1", voteA) * 100 if proportional else 1)}] {ep2["translation"][voteB]}{ep2["epnumber"]}')

    for vote in ep1["color"].keys():
        print(f':{ep1["translation"][vote]}{ep1["epnumber"]} {ep1["color"][vote]}')
    for vote in ep2["color"].keys():
        print(f':{ep2["translation"][vote]}{ep2["epnumber"]} {ep2["color"][vote]}')

if __name__ == "__main__":
    sankey(ep1t, ep2t)
