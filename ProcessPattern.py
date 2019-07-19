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

def remEndNos(mResource):
	lEndPos=mResource.rfind('/')
	mResource=mResource[0:lEndPos]
	return(mResource)

def processLine(line, modelBase, ignoreVocabs_Dict, NSDict, iPattern, patternList):
	fBase=False

	fReturn=False
	rMatchedResource=""

	matchedResource=extractURL(line, iPattern)

	class lineRetValues:
		def _init_ (self, fReturn, rMatchedResource):
			self.fReturn=False
			self.rMatchedResource=""
	
	if (matchedResource != ""):
		#print("The matched resource: " + matchedResource)					
		#print("Processing look up of resource")
		if (matchedResource.find('&') != -1):
			lookUpKey=lookUpResource(matchedResource)
			matchedResource=NSDict[lookUpKey]
			#print("& found in matched resource and after look up, the matched resource is: " + matchedResource)

		fBase=checkIfBase(matchedResource, modelBase)
		if (fBase == True):
			#print("Process Pattern: base found in matched resource")
			fReturn=False
			rMatchedResource=""
		elif (inIgnoreVocabList(matchedResource, ignoreVocabs_Dict) == True):
			#print("Matched resource in ignore list")
			fReturn=False
			rMatchedResource=""

		if (fBase == False and inIgnoreVocabList(matchedResource, ignoreVocabs_Dict) == False):
			tagPos=matchedResource.rfind('#')
			if (tagPos != -1):
				#print("# found in matched resource in position: " + str(tagPos))
				matchedResource=matchedResource[0:tagPos]
				#print("matched resource after removing # is: " + matchedResource)

			if (matchedResource.rfind('/') == len(matchedResource)):
				matchedResource=matchedResource[0:matchedResource.rfind('/')]
				#print("Ending / found in matched resource and after removing it, the matched resource is: " + matchedResource)

			slashPos=matchedResource.rfind('/')
			hyphPos=matchedResource.rfind('-')
			if ((slashPos != -1) and (hyphPos != -1) and (hyphPos > slashPos)):
				while ((hyphPos != -1) and (hyphPos > slashPos)):
					matchedResource=matchedResource[0:hyphPos]
					hyphPos=matchedResource.rfind('-')
				#print("- found after last / in matched resource and after removal, the matched resource is: " + matchedResource)

			if ((matchedResource != "") and (matchedResource.find("http") != -1)):
				if (matchedResource[len(matchedResource)-1].isdigit()):
					#print("Matched Resource has ending numbers: " + line)
					matchedResource=remEndNos(matchedResource)
					#print("After removal of ending numbers, the matched resource is: " + matchedResource)
					#input()

				if (checkIfDuplicate(matchedResource, patternList)==False):
					#print("Not a duplicate matched resource: " + matchedResource)
					fReturn=True
					rMatchedResource=matchedResource

	lineRetValues.fReturn=fReturn
	lineRetValues.rMatchedResource=rMatchedResource
	#print(rMatchedResource)
	#input()
	return(lineRetValues)

def processPattern(line, modelBase, ignoreVocabs_Dict, NSDict, iPattern, patternList):
	fPattern=False
	rResource=""

	currentLine=processLine(line, modelBase, ignoreVocabs_Dict, NSDict, iPattern, patternList)
	fPattern=currentLine.fReturn
	if (fPattern):
		rResource=currentLine.rMatchedResource

	return(rResource)
