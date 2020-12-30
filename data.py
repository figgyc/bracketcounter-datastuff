import matplotlib.pyplot as plt, mpld3
from config import ep2 as ep
import datafile

translation = ep['translation']
translation["total"] = "Total"
color = ep['color']
color["total"] = "#000000"

data = datafile.loadData(ep['dataFilename'])
votessorted = sorted(data['votes'], key=lambda k: k['date'])

epoch = data["epoch"]

def colpad(string, n):
    return " "*(n-len(string))

def col(string, n, left=False):
    if left:
        return colpad(str(string), n) + str(string)
    else:
        return str(string) + colpad(str(string), n)




#votessorted.reverse() # idk why tbh
totalVotes = {}
votesOverTime = {}
votesPerTime = {}
for key in translation.keys():
    totalVotes[key] = 0
    votesOverTime[key] = {}
    votesPerTime[key] = {}

for vote in votessorted:
    time = int( (vote['date'] - epoch) / 1000) # as far as i can tell youtube rounds it
    minute = int(time/60)
    totalVotes[vote['vote']] += 1
    votesOverTime[vote['vote']][time] = totalVotes[vote['vote']]
    if minute not in votesPerTime[vote['vote']]:
        votesPerTime[vote['vote']][minute] = 0
    votesPerTime[vote['vote']][minute] += 1
    totalVotes['total'] += 1
    votesOverTime['total'][time] = totalVotes['total']
    if minute not in votesPerTime['total']:
        votesPerTime['total'][minute] = 0
    votesPerTime['total'][minute] += 1


fig, ax = plt.subplots()
for char in translation.keys():
    if char != "total": # is True:
        ax.plot(list(votesOverTime[char].keys()), list(votesOverTime[char].values()), label=char + " - " + translation[char], color=color[char], drawstyle="steps-post", linewidth=0.6)
plt.legend()
plt.xlabel("seconds since upload")
plt.ylabel("votes")
#plt.savefig("graph.svg", dpi=10^11)
mpld3.save_html(fig, "graph/graph-"+ ep["epnumber"] + ".html")
#plt.show()

#plt.clf()
fig2, ax2 = plt.subplots()
#xnew = np.linspace(0, 172800000, 2880*10) 
for char in translation.keys():
    if char != "total": # is True:
        y = list(votesPerTime[char].values())
        #spl = make_interp_spline(list(votesPerTime[char].keys()), y, k=1)
        #ynew = spl(xnew)
        xnew = list(votesPerTime[char].keys())
        ynew = list(votesPerTime[char].values())
        ax2.plot(xnew, ynew, label=char + " - " + translation[char], color=color[char], linewidth=0.6)
plt.legend()
plt.xlabel("mins since upload")
plt.ylabel("votes/minute")
#plt.savefig("graph2.svg", dpi=10^11)
mpld3.save_html(fig2, "graph2/graph2-"+ ep["epnumber"] + ".html")

# generate postable
discordPostable = '```css\n'
sortedVotes = {k: v for k, v in sorted(totalVotes.items(), key=lambda item: item[1])}
sortedVotes.pop("total", None)
#sortedVotes.reverse() # v2s
keys = list(sortedVotes.keys())
keys.reverse()
col1 = 18
col2 = 5
for vote in keys:
    discordPostable += col('['+vote.upper()+"] "+translation[vote], col1) + col(sortedVotes[vote], col2, True) + " ["+ str(sortedVotes[vote]/totalVotes['total'] *100)[:4] +"%]\n"
discordPostable += "/*****************************/\n"
discordPostable += col("Comments", col1) + col(data['comments'], col2, True) + "\n"
discordPostable += col("Votes", col1) + col(totalVotes['total'], col2, True) + " [" + str(totalVotes['total']/data['comments'] *100)[:4]+ "%]\n"
#discordPostable += col("Multi Votes", col1) + col(cowards, col2, True) + " [" + str(cowards/(cowards+totalVotes['total']) *100)[:4]+ "%]\n"
#discordPostable += "/*  multivotes != alts/bots  */\n"
# broken?
discordPostable += "/*****************************/\n"
avgpc = totalVotes['total'] / (len(keys))
onetotwo = sortedVotes[keys[0]] - sortedVotes[keys[1]]
onetox = sortedVotes[keys[0]] - sortedVotes[keys[len(keys)-1]]
xtake12x = sortedVotes[keys[len(keys)-2]] - sortedVotes[keys[len(keys)-1]]
discordPostable += col("Avg Per Char.", col1) + str(round(avgpc, 3)) + "\n"
discordPostable += col("#1st-2nd Margin", col1) + col(onetotwo, col2, True) + " [" + str(onetotwo/totalVotes['total'] *100)[:4]+ "%]\n"
discordPostable += col("#1st-"+str(len(keys))+"th Margin", col1) + col(onetox, col2, True) + " [" + str(onetox/totalVotes['total'] *100)[:4]+ "%]\n"
discordPostable += col("#"+ str(len(keys)-1) + "th-" + str(len(keys)) + "th Margin", col1) + col(xtake12x, col2, True) + " [" + str(xtake12x/totalVotes["total"] *100)[:4]+ "%]\n"

discordPostable += "```"
print(discordPostable)

plt.show()
