#!/usr/bin/env python
#contigclass.py

###################################################################
#  The code below defines the class structure for a Contig. Each  #
#  contig has its ID, most significant blast hit (if available),  #
#  eValue (if available), a list of associated GO terms (if       #
#  available), a list of correlated GO descriptions, the length   #
#  of the sequence, the sequence, a list of associated KEGGs,     #
#  and a list of PFAM domains.                                    #
###################################################################

class Contig(object):
	def __init__(self, contigid = "", mostsigblast = "", eValue = "",
				 golist = "---NA---", golistDef = "---NA---", bp = 0,
				 fastaseq = "", keggList = "---NA-----",
				 pfamList = "---NA-----", expressionLevels = "---NA---"):
		self.contigid = contigid
		self.mostsigblast = mostsigblast
		self.eValue = eValue
		self.golist = golist
		self.golistDef = golistDef
		self.bp = bp
		self.fastaseq = fastaseq
		self.keggList = keggList
		self.pfamList = pfamList
		self.expressionLevels = expressionLevels
	
	def __repr__(self):
		toPrint = self.contigid + "\n\tMost Significant Blast Hit: " +\
		self.mostsigblast + "\n\teValue: " + self.eValue + "\n\tGO Terms: "\
		+ self.golist + "\n\tGO Descriptions: " + self.golistDef +\
		"\n\tKEGG Annotations: " + self.keggList[:-2] + "\n\tPFAM: " +\
		self.pfamList[:-2] + "\n\tExpression Levels: " + self.expressionLevels +\
		"\n\tLength: " + str(self.bp) + "\n\tSequence: " + self.fastaseq + "\n"
		return toPrint

	def set_id(self, contigid):
		self.contigid = contigid
	def get_id(self):
		return self.contigid
	
	def set_blast(self, mostsigblast):
		self.mostsigblast = mostsigblast
	def get_blast(self):
		return self.mostsigblast
	
	def set_eValue(self, eValue):
		self.eValue = eValue
	def get_eValue(self):
		return self.eValue
	
	def set_golist(self, golist):
		self.golist = golist
	def get_golist(self):
		return self.golist
	
	def set_golistDef(self, golistDef):
		self.golistDef = golistDef
	def get_golistDef(self):
		return self.golistDef
	
	def set_bp(self, bp):
		self.bp = bp
	def get_bp(self):
		return self.bp
	
	def set_fastaseq(self, fastaseq):
		self.fastaseq = fastaseq
	def get_fastaseq(self):
		return self.fastaseq
	
	def set_keggList(self, kegg):
		if "---NA---" in self.keggList:
			self.keggList = str(kegg) + "; "
		else:
			self.keggList += str(kegg) + "; "
	def get_keggList(self):
		return self.keggList
	
	def set_pfamList(self, ipsr):
		if "---NA---" in self.pfamList:
			self.pfamList = str(ipsr) + "; "
		else:
			self.pfamList += str(ipsr) + "; "
	def get_pfamList(self):
		return self.pfamList
	
	def set_expressionLevels(self, expressionLevels):
		self.expressionLevels = expressionLevels
	def get_expressionLevels(self):
		return self.expressionLevels

###################################################################
#  The code below defines the class structure for a Kegg map.     #
#  Each Kegg map has a pathway, pathway ID, enzyme, and enzyme    #
#  ID.                                                            #
###################################################################

class Kegg(object):
	def __init__(self, pathway = "---NA---", enzyme = "---NA---",
				 enzymeID = "---NA---", pathwayID = "---NA---"):
		self.pathway = pathway
		self.pathwayID = pathwayID
		self.enzyme = enzyme
		self.enzymeID = enzymeID
	
	def __repr__(self):
		toPrint = "(" + self.pathway + " (" + self.pathwayID + "), " +\
		          self.enzyme + " (" + self.enzymeID + "))"
		return toPrint
	
	def set_pathway(self, pathway):
		self.pathway = pathway
	def get_pathway(self):
		return self.pathway
	
	def set_pathwayID(self, pathwayID):
		self.pathwayID = pathwayID
	def get_pathwayID(self):
		return self.pathwayID
	
	def set_enzyme(self, enzyme):
		self.enzyme = enzyme
	def get_enzyme(self):
		return self.enzyme
	
	def set_enzymeID(self, enzymeID):
		self.enzymeID = enzymeID
	def get_enzymeID(self):
		return self.enzymeID

###################################################################
#  The code below defines the class structure for a PFAM          #
#  annoation. Each PFAM has a domain description and pfam ID.     #
###################################################################

class PFAM(object):
	def __init__(self, description = "---NA---", pfam = "---NA---"):
		self.description = description
		self.pfam = pfam
	
	def __repr__(self):
		toPrint = "(" + self.description + "; " + self.pfam + ")"
		return toPrint
	
	def set_description(self, description):
		self.description = description
	def get_description(self):
		return self.description
	
	def set_pfam(self, pfam):
		self.pfam = pfam
	def get_pfam(self):
		return self.pfam
	
###################################################################
#  The code below defines a method that reads the dictionary      #
#  file created by the Database program, turns it into a list of  #
#  Contigs, and passes that database to the user.                 #
###################################################################

def read_dictionary(filename):
	"""
	Takes a dictionary file created by Database.py and populates a
	list of Contigs.
	"""
	database = []
	dictionary_file = open(filename, "rU")
	
	header = dictionary_file.readline().strip()
	#DO SOMETHING WITH THIS HEADER
	
	line = dictionary_file.readline().strip()
	while line:
		temp = Contig()
		temp.set_id(line)
		line = dictionary_file.readline().strip()
		temp.set_blast(line[28:])
		line = dictionary_file.readline().strip()
		temp.set_eValue(line[8:])
		line = dictionary_file.readline().strip()
		temp.set_golist(line[10:])
		line = dictionary_file.readline().strip()
		temp.set_golistDef(line[17:])
		line = dictionary_file.readline().strip()
		temp.keggList = line[18:]
		line = dictionary_file.readline().strip()
		temp.pfamList = line[6:]
		line = dictionary_file.readline().strip()
		temp.set_expressionLevels(line[19:])
		line = dictionary_file.readline().strip()
		temp.set_bp(int(line[8:]))
		line = dictionary_file.readline().strip()
		temp.set_fastaseq(line[10:])
		line = dictionary_file.readline().strip()
		database.append(temp)
	
	dictionary_file.close()
	return database