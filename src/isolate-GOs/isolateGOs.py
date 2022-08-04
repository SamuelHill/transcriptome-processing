#!/usr/bin/env python
#isolateGOs.py
import sys

isolatedGOs = []
try:
	goFile = open(sys.argv[1], "rU")
except Exception, FileNotFound:
	print "Correct Usage: python isolateGOs.py goFile[.txt]"
	sys.exit(0)

line = goFile.readline().strip()
while line:
	while len(line) == 0:
		line = goFile.readline().strip()
	tab_delimit = line.split("\t")
	for item in tab_delimit:
		if "GO:" in item and item not in isolatedGOs:
			isolatedGOs.append(item)
			break
	line = goFile.readline().strip()
goFile.close()

outfilename = raw_input(">What do you want to save this result as?")

f = open(outfilename, "w")
for item in isolatedGOs:
	f.write(item)
	f.write("\n")
f.close()

