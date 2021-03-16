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
# voteregex = re.compile(r"(needle|rocky|teardrop|leafy|flower|golf ball|coiny|snowball|ice cube|tennis ball)", re.M)

cowards = 0
data = datafile.loadData(ep["savestateFilename"])
deadline = int(data['deadline'])
epoch = deadline - (3600000 * ep["deadlineHours"]) # 48h in ms
#print(deadline, epoch)
#epoch = 1262363842000 * 1000
#deadline = epoch + (3600000 * ep["deadlineHours"])
entriessorted = sorted(data['entries'], key=lambda k: k['date']) 
entriessorted.reverse() # newest first for deduplicating
usersProcessed = set()
votes = []
for entry in entriessorted:
    isCoward = entry['userId'] in usersProcessed
    if entry['date'] <= deadline:
        #print(entry)
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
                            if entry['userId'] == "UC210Pp4CFbGfRK8DbMQ9k4Q": #bho
                            #if entry['userId'] == "UCgXJoWsPCZaNd74q-Ms1LiQ": #tdo
                                print(entry)
                            if 'likes' not in entry:
                                entry['likes'] = 0
                            if 'edited' not in entry:
                                entry['edited'] = False
                            #print(entry)
                            datechoose = entry['date']
                            votes.append({'date': datechoose if 'postDate' in entry else entry['date'], 'vote': vote, 'likes': entry['likes'], 'edited': entry['edited'], 'user': hashlib.sha256(str(entry['userId']).encode("utf8")).digest()})
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
