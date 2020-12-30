import re
import datafile
from config import ep2 as ep
import hashlib

translation = ep['translation']

validVotes = list(translation.keys())

allVotes = ""
for vote in validVotes:
    allVotes += vote

voteregex = re.compile(r"\[(.)\]", re.M)


cowards = 0
data = datafile.loadData(ep["savestateFilename"])
deadline = int(data['deadline'])
epoch = deadline - 172800000 # 48h in ms
entriessorted = sorted(data['entries'], key=lambda k: k['date']) 
entriessorted.reverse() # newest first for deduplicating
usersProcessed = set()
votes = []
for entry in entriessorted:
    isCoward = entry['userId'] in usersProcessed
    if True: #if entry['date'] <= deadline:
        comment = (entry['content']).lower()
        matches = re.findall(voteregex, comment)
        # matches.reverse()
        if matches:
            vote = ""
            for match in matches:
                if match in validVotes:
                    vote = match
                    if vote != "":
                        if not isCoward:
                            votes.append({'date': entry['date'], 'vote': vote, 'user': hashlib.sha256(str(entry['userId']).encode("utf8")).digest()})
                            usersProcessed.add(entry['userId'])
                        else:
                            cowards += 1
                        isCoward = True
            
votessorted = sorted(votes, key=lambda k: k['date']) 

data = {
    'votes': votessorted,
    'epoch': epoch,
    'comments': len(entriessorted)
}
datafile.saveData(ep["dataFilename"], data)