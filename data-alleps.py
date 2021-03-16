import matplotlib.pyplot as plt, mpld3
import config
import datafile

translation = {}
translation["total"] = "Total"
color = {}
color["total"] = "#000000"



def colpad(string, n):
    return " "*(n-len(string))

def col(string, n, left=False):
    if left:
        return colpad(str(string), n) + str(string)
    else:
        return str(string) + colpad(str(string), n)

fig, ax = plt.subplots()


#colors = ["red", "green", "blue", "pink", "black", "grey", "orange", "purple", "#aaaa00"]

i = 0
#votessorted.reverse() # idk why tbh
for ep in config.episodes:
    data = datafile.loadData(ep['dataFilename'])

    winColor = ep["color"][ep["loser"]]

    epoch = data['epoch']
    votessorted = sorted(data['votes'], key=lambda k: k['date'])

    totalVotes = {}
    votesOverTime = {}
    votesPerTime = {}
    for key in translation.keys():
        totalVotes[key] = 0
        votesOverTime[key] = {}
        votesPerTime[key] = {}

    for vote in votessorted:
        time = int( (vote['date'] - epoch) / 1000) # as far as i can tell youtube rounds it
        totalVotes['total'] += 1
        votesOverTime['total'][time] = totalVotes['total']
        if time not in votesPerTime['total']:
            votesPerTime['total'][time] = 0
        votesPerTime['total'][time] += 1

    ax.plot(list(votesOverTime['total'].keys()), list(votesOverTime['total'].values()), label=ep["epnumber"], color=winColor, drawstyle="steps-post", linewidth=0.6)

    i += 1


ax.set_xlim(-100, 48*60*60 +100)
plt.legend()
plt.xlabel("s since upload")
plt.ylabel("votes")
mpld3.save_html(fig, "graph-totals.html")
plt.show()


