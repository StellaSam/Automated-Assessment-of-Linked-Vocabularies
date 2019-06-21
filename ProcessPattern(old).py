import re
from BuildDict import buildNSDict
from LookUpResource import lookUpResource

from CheckIfBase import checkIfBase
from CheckIfDuplicate import checkIfDuplicate
from CheckIfInIgnoreVocabList import inIgnoreVocabList

def getItemToAppend(iItem):
	if (iItem == ":Class"):
		rItem=":Class rdf:about="
	elif (iItem == ":ObjectProperty"):
		rItem=":ObjectProperty rdf:about="
	elif (iItem == ":imports"):
		rItem=":imports rdf:resource="
	elif (iItem == ":seeAlso"):
		rItem=":seeAlso rdf:resource="
	elif (iItem == ":isDefinedBy"):
		rItem=":isDefinedBy rdf:resource="
	elif (iItem == ":equivalentClass"):
		rItem=":equivalentClass rdf:resource="
	elif (iItem == ":range"):
		rItem=":range rdf:resource="
	elif (iItem == ":subClassOf"):
		rItem=":subClassOf rdf:resource="
	elif (iItem == ":subPropertyOf"):
		rItem=":subPropertyOf rdf:resource="
	elif (iItem == ":equivalentProperty"):
		rItem=":equivalentProperty rdf:resource="
	elif (iItem == ":unionOf"):
		rItem="<owl:unionOf "

	return(rItem)

def extractPatterns(line):
	refPatternList=[':Class', ':ObjectProperty', ':imports', ':seeAlso', ':isDefinedBy', ':equivalentClass', ':range', ':subClassOf', ':subPropertyOf', ':equivalentProperty', ':unionOf']
	aboutStr="rdf:about="
	resourceStr="rdf:resource="
	mEquivalentClassStr="owl:equivalentClass>"
	unionOfStr="owl:unionOf "
	fList=[]
	patternList=[]

	lst=line.split('<')
	for item in lst:
		if (re.search(mEquivalentClassStr, item)):
			patternList.append("<owl:equivalentClass>")
		elif (re.search(unionOfStr, item)):
			patternList.append("<owl:unionOf ")

	ind=0
	while (ind < len(lst)):
		if re.search(resourceStr, lst[ind]):
			fList.append(re.split(resourceStr, lst[ind]))
		ind += 1
	ind=0
	while (ind < len(lst)):
		if re.search(aboutStr, lst[ind]):
			fList.append(re.split(aboutStr, lst[ind]))
		ind += 1

	ind=0	
	while (ind < len(fList)):
		item=fList[ind][0]
		startPos=item.find(':')
		item=item[startPos::].rstrip()
		if (item in refPatternList):
			patternList.append(getItemToAppend(item))
		ind += 1

	return(patternList)

def extractURL(line, iPattern):
	Pos=line.find(iPattern)
	startPos=Pos+len(iPattern)
	extResource=line[startPos+1::]
	endPos=extResource.find('"')
	extResource=extResource[0:endPos]
	return(extResource)

def remEndNos(line):
	if line[len(line)-1].isdigit():
		lEndPos=line.rfind('/')
		line=line[0:lEndPos]
	return(line)

def processLine(line, modelBase, ignoreVocabs_Dict, NSDict, iPattern, patternList):
	fReturn=False
	rMatchedResource=""

	matchedResource=extractURL(line, iPattern)

	class lineRetValues:
		def _init_ (self, fReturn, rMatchedResource):
			self.fReturn=False
			self.rMatchedResource=""
	
	if (matchedResource != ""):		
		if (modelBase != ""):
			if (matchedResource.find(modelBase) != -1):
				if (len(matchedResource) > len(modelBase)):
					matchedResource=matchedResource[0:len(modelBase)]

		tagPos=matchedResource.rfind('#')
		if (tagPos != -1):
			matchedResource=matchedResource[0:tagPos]
		else:
			if (matchedResource.rfind('/') == len(matchedResource)):
				matchedResource=matchedResource[0:matchedResource.rfind('/')]

		if (matchedResource.find('&') != -1):
			lookUpKey=lookUpResource(matchedResource)
			matchedResource=NSDict[lookUpKey]
		else:
			slashPos=matchedResource.rfind('/')
			hyphPos=matchedResource.rfind('-')
			while ((hyphPos != -1) and (hyphPos > slashPos)):
				matchedResource=matchedResource[0:hyphPos]
				hyphPos=matchedResource.rfind('-')

		if ((matchedResource != "") and (matchedResource.find("http") != -1)):
			matchedResource=remEndNos(matchedResource)
			if (not checkIfBase(matchedResource, modelBase)):
				if (not checkIfDuplicate(matchedResource, patternList)):
					if (not inIgnoreVocabList(matchedResource, ignoreVocabs_Dict)):
						fReturn=True
						rMatchedResource=matchedResource

	lineRetValues.fReturn=fReturn
	lineRetValues.rMatchedResource=rMatchedResource

	return(lineRetValues)

def processPattern(line, modelBase, ignoreVocabs_Dict, NSDict, iPattern, patternList):
	fPattern=False
	rResource=""

	currentLine=processLine(line, modelBase, ignoreVocabs_Dict, NSDict, iPattern, patternList)
	fPattern=currentLine.fReturn
	if (fPattern):
		rResource=currentLine.rMatchedResource

	return(rResource)
