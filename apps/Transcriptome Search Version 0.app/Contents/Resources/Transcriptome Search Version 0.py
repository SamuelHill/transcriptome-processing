#!/usr/bin/env python
#Transcriptome Search Version 0.py

from contigclass import *
import sys
from Tkinter import *
import tkMessageBox
from tkFileDialog import askopenfile, asksaveasfile

database = []
output = []

###################################################################
#  The code below contains the definitions of the functions that  #
#  will assist in searching through the database.                 #
###################################################################

def search(toSearch):
	"""
	Searches the database for a particular string (or set of strings) against a
	particular set of data associated with the contigs (BLAST, GOs, PFAM, or KEGG)
	"""
	try:
		bp = int(BPLimit.get(1.0, END))
	except ValueError:
		bp = 0
	try:
		eVal = float(eValLim.get(1.0, END))
	except ValueError:
		eVal = 0
	
	raw = searchTerm.get(1.0, END)
	searchstrings = raw.split('\n')
	for index, item in enumerate(searchstrings):
		searchstrings[index] = str(item).strip()
	searchstrings.pop()
	
	for contig in database:
		if (contig.get_bp() > bp) and (float(contig.get_eValue()) < eVal):
			if toSearch is "BLAST":
				for string in searchstrings:
					if string.lower() in contig.mostsigblast.lower():
						output.append(contig)
			elif toSearch is "GO":
				for string in searchstrings:
					if (string.lower() in contig.golist.lower() or string.lower() in contig.golistDef.lower()):
						output.append(contig)
			elif toSearch is "KEGG":
				for string in searchstrings:
					if string.lower() in contig.keggList.lower():
						output.append(contig)
			elif toSearch is "PFAM":
				for string in searchstrings:
					if string.lower() in contig.pfamList.lower():
						output.append(contig)

def write_output():
	"""Writes the generated output to a file"""
	f = asksaveasfile(mode = 'w', title = "Choose Write destination", defaultextension = '.txt')
	f.write("This search yielded %d hits \n" % len(output))
	for item in output:
		f.write(str(item))
	f.close()
	tkMessageBox.showinfo("Completed!", "Output has been writen.")
	output[:] = []

###################################################################
#  The code below contains the definitions of the functions that  #
#  will search in one of the four ways, then write the output;    #
#  and the function to create the application window.             #
###################################################################

def load_dict():
	"""Reads a dictionary file, loads the database, and unlocks other functions"""
	database_file = askopenfile(mode = "r", title = "Choose database file")
	global database
	database = read_dictionary(database_file.name)

def select_blast():
	"""Searchs for (a) BLAST hit(s), then writes the output."""
	search("BLAST")
	write_output()

def select_go():
	"""Searchs for (a) GO Term(s), then writes the output."""
	search("GO")
	write_output()

def select_kegg():
	"""Searchs for (a) Map ID(s), then writes the output."""
	search("KEGG")
	write_output()

def select_pfam():
	"""Searchs for (a) PFAM domain(s), then writes the output."""
	search("PFAM")
	write_output()

def app_Window(root):
	"""Creates the buttons and labels for the application window."""
	#The actual window (name, size, and position)
	root.title('Transcriptome Search')
	w = root.winfo_screenwidth()
	x = w/2 - 350/2
	h = root.winfo_screenheight()
	y = h/2 - 185/2
	root.geometry("350x185+%d+%d" % (x, y))
	
	loadDictionary = Button(root, text = "Choose dictionary to load", command = load_dict)
	loadDictionary.grid(row = 0, columnspan = 2)
	
	searchTermLabel = Label(root, text = "Search:")
	searchTermLabel.grid(row = 1)
	global searchTerm
	searchTerm = Text(root, bg = "LIGHTBLUE")
	searchTerm.config(width =25, height = 3)
	searchTerm.grid(row = 1, column = 1)
	
	BPLimitLabel = Label(root, text = "BP Limit:")
	BPLimitLabel.grid(row = 2)
	global BPLimit
	BPLimit = Text(root, bg = "LIGHTBLUE")
	BPLimit.config(width = 15, height = 1)
	BPLimit.grid(row = 3)
	eValLimLabel = Label(root, text = "eValue Limit:")
	eValLimLabel.grid(row = 2, column = 1)
	global eValLim
	eValLim = Text(root, bg = "LIGHTBLUE")
	eValLim.config(width = 15, height = 1)
	eValLim.grid(row = 3, column = 1)
	
	selectblastB = Button(root, text = "Search for BLAST", command = select_blast)
	selectblastB.grid(row = 4)
	selectgoB = Button(root, text = "Search for GO Terms", command = select_go)
	selectgoB.grid(row = 5)
	selectIPSB = Button(root, text = "Search for PFAM Domains", command = select_pfam)
	selectIPSB.grid(row = 4, column = 1)
	selectKeggB = Button(root, text = "Search for Kegg Map IDs", command = select_kegg)
	selectKeggB.grid(row = 5, column = 1)

####################################################################
#  The code below is what builds the application window and runs.  #
####################################################################

root = Tk()
app_Window(root)
root.mainloop()