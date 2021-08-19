import datafile, sys

for filename in sys.argv[1:]:
	datafile.saveData(filename[:-4] + "msgp", datafile.loadData(filename))
