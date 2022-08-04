#!/usr/bin/env python
#Database.py

from contigclass import *
import sys
from Tkinter import *
from tkFileDialog import askopenfile, asksaveasfile
import xml.etree.ElementTree as ET

database = []
starter_line = "Transcriptomes in file: "

####################################################################
#  The code below is the definitions of functions that will build  #
#  the database from Blast2Go files and a Gene Ontology, write     #
#  the output, and build an application window.                    #
####################################################################

def seqTable():
	"""
	Takes the Sequence Table output of BLAST2GO and gets the Contig ID,
	most significant Blast hit, base pair count of sequence, and e-value
	for the database.
	"""
	sequence_table = askopenfile(mode = 'r', multiple = False,
                                 title = "Choose Sequence Table file")
	title_line = sequence_table.readline()
	for line in sequence_table:
		line_split = line.split("\t")
		temp = Contig()
		temp.set_id(line_split[0])
		temp.set_blast(line_split[1])
		temp.set_bp(int(line_split[2]))
		if line_split[4] is "":
			temp.set_eValue("---NA---")
		else:
			temp.set_eValue(line_split[4])
		database.append(temp)
	sequence_table.close()
	listbox.insert(END, "Completed Sequence Table!", "Database now contains all" +\
						 " contigs, blasts, bp length, and evalues.")
	listbox.yview(END)

def goStat():
	"""
	Takes the GOStat output of BLAST2GO and gets the list of GO terms
	associated with each contig for the database.
	"""
	golistXMLwithDef = askopenfile(mode = 'r', multiple = False,
		                          title = "Choose go daily term XML file")
	listbox.insert(END, "Reading in terms and definitions...")
	listbox.yview(END)
	listbox.update_idletasks()
	tree = ET.parse(golistXMLwithDef)
	root = tree.getroot()
	goTerms = []
	goTermDefs = []
	for i in range(0, len(root[0])):
		goTerms.append(root[0][i][0].text)
		goTermDefs.append(root[0][i][1].text)
	listbox.insert(END, "Matched all terms and definitions.")
	listbox.yview(END)
	
	goStat_file = askopenfile(mode = 'r', multiple = False,
		                          title = "Choose GOStat file")
	line_count = len(goStat_file.readlines()) - 1
	goStat_file.seek(0)
	title_line = goStat_file.readline()
	for index, line in enumerate(goStat_file):
		line_split = line.split("\t")
		contig_with_gos = line_split[0]
		gos = line_split[1]
		for index_of_database, contig in enumerate(database):
			if contig.get_id() == contig_with_gos:
				golist = formatGOS(gos)
				database[index_of_database].set_golist(golist)
				golistdefs = ""
				godefs = golist.split(" ")
				for goterm in godefs:
					for i, go in enumerate(goTerms):
						if goterm == go:
							golistdefs += goTermDefs[i] + "; "
							break
				database[index_of_database].set_golistDef(golistdefs[:-2])
				break
		listbox.insert(END, str(((float(index + 1)/line_count)*100)) + "%")
		listbox.yview(END)
		listbox.update_idletasks()
	goStat_file.close()
	listbox.insert(END, "Completed GOStat/Defs!")
	listbox.insert(END, "Each contig in Database now has a list of GO terms and defs.")
	listbox.yview(END)

def formatGOS(gos):
	"""
	Formats the list of GO's provided by the GOStat file into lists
	separated by spaces, including the GO: prefix, and with the correct
	number of leading 0's.
	
	Input: String (comma delineated list of GO's)
	"""
	golist = gos.split(",")
	new_golist = ""
	for go in golist:
		go = go.strip()
		num_zeros = 7 - len(go)
		new_golist += "GO:" + ("0" * num_zeros) + str(go) + " "
	return new_golist

def fasta():
	"""
	Takes the Fasta file output of BLAST2GO and adds the nucleic acid
	sequence of each contig to the database.
	"""
	fasta_file = askopenfile(mode = 'r', multiple = False,
		                     title = "Choose Fasta file")
	fasta_lines = [line for line in fasta_file.readlines() if ">" not in line]
	for index, line in enumerate(fasta_lines):
		database[index].set_fastaseq(str(line.strip()))
	fasta_file.close()
	listbox.insert(END, "Completed Fasta Sequence!")
	listbox.insert(END, "Each contig in Database now has its sequence.")
	listbox.yview(END)

def add_keggs():
	"""
	Takes the KEGG file output of BLAST2GO and adds the associated KEGGs
	to each contig in the database.
	"""
	kegg_table = askopenfile(mode = 'rU', multiple = False,
	                         title = "Choose Kegg Table file")
	kegg_lines = [line for line in kegg_table.readlines() if "Pathway\tSeqs" not in line]
	for line in kegg_lines:
		line_split = line.split("\t")
		temp = Kegg()
		temp.set_pathway(line_split[0])
		temp.set_enzyme(line_split[2])
		temp.set_enzymeID(line_split[3])
		temp.set_pathwayID(line_split[6])
		sequences = line_split[5].split(" ")
		for seq in sequences:
			for index, contig in enumerate(database):
				if contig.get_id().strip() == seq:
					database[index].set_keggList(temp)
					break
	listbox.insert(END, "Completed Kegg Maps!")
	listbox.insert(END, "Each contig in Database now has its Kegg annotaions.")
	listbox.yview(END)

def pfam():
	"""
	Takes the InterProScan file output of BLAST2GO and adds the associated
	PFAM domains to each contig in the database.
	"""
	ipsr_table = askopenfile(mode = 'r', multiple = False,
		                     title = "Choose InterProScan file")
	for line in ipsr_table.readlines():
		line_split = line.split("\t")
		try:
			line_split[5]
		except IndexError:
			continue
		if 'PF' in line_split[5]:
			contig_to_check = line_split[0]
			temp = PFAM(line_split[3], line_split[5][:-7].strip())
			for index, contig in enumerate(database):
				if contig.get_id().strip() == contig_to_check:
					database[index].set_pfamList(temp)
					break
	listbox.insert(END, "Completed PFAM!")
	listbox.insert(END, "Each contig in Database now has its PFAM annotation.")
	listbox.yview(END)

def expression_Levels():
	"""
	"""
	names = trans_names.get(1.0, END)
	if names == "\n":
		listbox.insert(END, "Must enter names of Transcriptomes.")
		listbox.yview(END)
		return
	#Else statements for 1 transcriptome vs multiple
	#assign different beginnings for multipliers
	names = names.split(",")
	num_trans = len(names)
	
	starter_line += ", ".join(names) + "\n"
	
	expr_lvl_table = askopenfile(mode = 'r', multiple = False,
			                     title = "Choose CLC output file")
	title_line = expr_lvl_table.readline()
	for line in expr_lvl_table:
		line_split = line.split("\t")
		for index, contig in enumerate(database):
			if contig.get_id() == line_split[0]:
				expr_lvls = []
				for i in range(num_trans):
					expr_lvls[i] = names[i] + " = " + linesplit[16 + (i * 8)]
				final_lvls = ", ".join(expr_lvls)
				database[index].set_expressionLevels(final_lvls)
				break

def write_database():
	"""Writes the database into a single file."""
	f = asksaveasfile(mode = 'w', title = "Choose Write destination", defaultextension = '.txt')
	f.write(starter_line)
	for item in database:
		f.write(str(item))
	listbox.insert(END, "Database has been written!")
	listbox.yview(END)
	database[:] = []

def app_Window(root):
	"""Creates the application window."""
	#The actual window (name, size, and position)
	root.title('Database')
	w = root.winfo_screenwidth()
	x = w/2 - 372/2
	h = root.winfo_screenheight()
	y = h/2 - 345/2
	root.geometry("372x345+%d+%d" % (x, y))
	
	#Buttons for the building of the Database
	seq_tab_B = Button(root, text = "Sequence Table", command = seqTable)
	seq_tab_B.grid(row = 0)
	global trans_names
	trans_names = Text(root, bd = 3, bg = "LIGHTBLUE")
	trans_names.config(width = 22, height = 5)
	trans_names.grid(row = 1, rowspan = 3)
	expr_lvl_B = Button(root, text = "Expression Levels", command = expression_Levels)
	expr_lvl_B.grid(row = 4)
	gostat_B = Button(root, text = "GOStat/Defs", command = goStat)
	gostat_B.grid(row = 0, column = 1)
	fasta_B = Button(root, text = "Fasta Sequences", command = fasta)
	fasta_B.grid(row = 1, column = 1)
	kegg_B = Button(root, text = "Kegg Maps", command = add_keggs)
	kegg_B.grid(row = 2, column = 1)
	ipsr_B = Button(root, text = "PFAM", command = pfam)
	ipsr_B.grid(row = 3, column = 1)
	create_B = Button(root, text = "Create Database", command = write_database)
	create_B.grid(row = 4, column = 1)
	
	#Listbox for providing feedback to the user.
	list_L = Label(root, text = "Current Progress")
	list_L.grid(row = 5, columnspan = 2)
	global listbox
	listbox = Listbox(root)
	listbox.grid(row = 6, rowspan = 6, columnspan = 2, ipadx = 100, padx = 5)

####################################################################
#  The code below is what builds the application window and runs.  #
####################################################################

root = Tk()
app_Window(root)
root.mainloop()