# Bracketcounter Data Tools
This is the secondary repository for Bracketcounter - it's basically got everything except the actual data collection (see [the main bracketcounter](https://github.com/figgyc/bracketcounter) for that).

## Setup
This is a set of command line tools, you will want to use them in the Windows Command Prompt or PowerShell, or the Terminal on Linux or macOS.
1. [Install Python 3](https://www.python.org/downloads/)
2. Run `pip -r requirements.txt`
3. Copy `config.example.py` to `config.py`

## Usage
1. Delete `savestate.json` and restart your Bracketcounter with a clean savestate (this should get rid of any since deleted comments that would interfere with the data)
1. After it counts all the comments, stop your Bracketcounter instance (in the typical use case, just press Ctrl+C.)
1. Copy `savestate.json` from the Bracketcounter folder to the `savestate` folder, and rename it to something sensible, like `savestate-ep1.json`.
1. Edit `config.py` to add details for the episode you are counting - these should mostly mirror configuration on Bracketcounter's server end. The example comes with enough annotation so it should be easy to follow.
1. Run `python processor.py`. You only need to do this once per episode, and once it's done you can delete the savestate if you want. This script takes the savestate data and minifies it into only the user, vote, and time. It also does "hashing" on the user IDs: basically this means that you can check that vote A and vote B were both done by the same person for switching purposes, but you can't easily reverse the hash to find out who that person was.

After you've processed data for an episode, you will want to use the main data scripts (`python scriptname`), described below:
* `data.py` - **This is the main script** that you probably will only ever use, it produces the votes over time per character graph, the votes per minute graph, and **the main voting results numbers** (in a Discord postable format, but you can use them for anything)
* `data-alleps.py` - This script creates a graph of the voters over time per episode (all characters)
* `sankey.py` - This creates data for a voter switching graph; you need to put the output into [SankeyMATIC](http://sankeymatic.com/build/) or a compatible tool.
* `allvoters.py` - This calclates the total number of all voters, or all voters who have voted on every episode, and outputs it to `vlist.msgp`, for use in `sankey.py` so you can chain the graphs together and produce a more interesting result.

## Notes
* The `graph` and `graph2` folders and `graph-totals.html` are HTML conversions of the graphs you see, designed to be uploaded to a website to view (mainly for my application, you probably won't need these)
* `dataFilename` can be set as either a file ending in `msgp` or `json`. The `msgp` format is msgpack, which is much faster to encode and decode, and smaller in filesize, so it is recommended in most applications. You may find the `json` format more useful if you want to take the data and use it in other applications outside of these data tools.

