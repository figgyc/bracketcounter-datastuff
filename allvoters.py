from config import episodes, supes
import datafile

i = 0
voters = set()
for ep in episodes:
    print(ep['epnumber'])
    epusers = set()
    validVotes = list(ep['translation'].keys())
    votessorted = sorted(datafile.loadData(ep['dataFilename'])['votes'], key=lambda k: k['date'])
    for vote in votessorted:
        if vote['vote'] in validVotes:
            if not supes or (i == 0):
                voters.add(vote['user'])
            if supes:
                epusers.add(vote['user'])
    if supes:
        #print(len(epusers))
        voters = voters.intersection(epusers)
        #for user in voters.copy():
        #    if user not in epusers:
        #        voters.remove(user)
    print(len(voters))
    i = i + 1


datafile.saveData("vlist.msgp", list(voters))