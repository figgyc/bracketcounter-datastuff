from config import episodes
import sankey
import data

n = len(episodes)
n2 = 0
while n2 < n-1:
    sankey.sankey(episodes[n2], episodes[n2+1])
    n2 += 1

for ep in episodes:
    plt, out = data.graphify(ep)
    plt.close()
