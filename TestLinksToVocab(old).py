import re

from BuildDict import buildNSDict
from FindBase import findBase
from CheckIfDuplicate import *
from ProcessPattern import *

def checkLinksToVocab(lineList, numLinesinFile, modelBase, ignoreVocabs_Dict, NSDict):

	fLinkToVocab=False
	linksToDict={}

	class retValues:
		def _init_(self, fLinksToVocab, retLinksToDict):
			self.fLinksToVocab=fLinkToVocab
			self.retLinksToDict={}

	classPattern=":Class rdf:about="
	classList=[]

	objPropertyPattern=":ObjectProperty rdf:about="
	objPropertyList=[]

	importPattern=":imports rdf:resource="
	importList=[]

	seeAlsoPattern=":seeAlso rdf:resource="
	seeAlsoList=[]

	isDefinedByPattern=":isDefinedBy rdf:resource="
	isDefinedByList=[]

	sEquivalentClassPattern=":equivalentClass rdf:resource="

	startEquivalentClassPattern="<owl:equivalentClass>"
	endEquivalentClassPattern="</owl:equivalentClass>"

	equivalentClassList=[]

	rangePattern=":range rdf:resource="
	rangeList=[]

	subClassPattern=":subClassOf rdf:resource="
	subClassList=[]

	subPropertyPattern=":subPropertyOf rdf:resource="
	subPropertyList=[]

	equivalentPropertyPattern=":equivalentProperty rdf:resource="
	equivalentPropertyList=[]

	startUnionOfPattern="<owl:unionOf "
	endUnionOfPattern="</owl:unionOf>"
	unionOfList=[]

	resourcePattern="rdf:resource="
	aboutPattern="rdf:about="

	lNum=0
	while (lNum < numLinesinFile):
		iLine=lineList[lNum]
		pList=extractPatterns(iLine)
		for pattern in pList:
			line=iLine
			if (pattern == classPattern):
				resource=processPattern(line, modelBase, ignoreVocabs_Dict, NSDict, classPattern, classList)
				if (resource != ""):
					classList.append(resource)
			elif (pattern == objPropertyPattern):
				resource=processPattern(line, modelBase, ignoreVocabs_Dict, NSDict, objPropertyPattern, objPropertyList)
				if (resource != ""):
					objPropertyList.append(resource)
			elif (pattern == importPattern):
				resource=processPattern(line, modelBase, ignoreVocabs_Dict, NSDict, importPattern, importList)
				if (resource != ""):
					importList.append(resource)
			elif (pattern == seeAlsoPattern):
				resource=processPattern(line, modelBase, ignoreVocabs_Dict, NSDict, seeAlsoPattern, seeAlsoList)
				if (resource != ""):
					seeAlsoList.append(resource)
			elif (pattern == isDefinedByPattern):
				resource=processPattern(line, modelBase, ignoreVocabs_Dict, NSDict, isDefinedByPattern, isDefinedByList)
				if (resource != ""):
					isDefinedByList.append(resource)
			elif (pattern == sEquivalentClassPattern):
				resource=processPattern(line, modelBase, ignoreVocabs_Dict, NSDict, sEquivalentClassPattern, equivalentClassList)
				if (resource != ""):
					equivalentClassList.append(resource)
			elif (pattern == startEquivalentClassPattern):
				lNum += 1
				while (lNum < numLinesinFile):
					line=lineList[lNum]
					if (re.search(endEquivalentClassPattern, line)):
						break
					else:
						if (re.search(resourcePattern, line)): 
							resource=processPattern(line, modelBase, ignoreVocabs_Dict, NSDict, resourcePattern, equivalentClassList)
						elif (re.search(aboutPattern, line)):
							resource=processPattern(line, modelBase, ignoreVocabs_Dict, NSDict, aboutPattern, equivalentClassList)
						lNum += 1
				if (resource != ""):
					equivalentClassList.append(resource)
			elif (pattern == rangePattern):
				resource=processPattern(line, modelBase, ignoreVocabs_Dict, NSDict, rangePattern, rangeList)
				if (resource != ""):
					rangeList.append(resource)
			elif (pattern == subClassPattern):
				resource=processPattern(line, modelBase, ignoreVocabs_Dict, NSDict, subClassPattern, subClassList)
				if (resource != ""):
					subClassList.append(resource)
			elif (pattern == subPropertyPattern):
				resource=processPattern(line, modelBase, ignoreVocabs_Dict, NSDict, subPropertyPattern, subPropertyList)
				if (resource != ""):
					subPropertyList.append(resource)
			elif (pattern == equivalentPropertyPattern):
				resource=processPattern(line, modelBase, ignoreVocabs_Dict, NSDict, equivalentPropertyPattern, equivalentPropertyList)
				if (resource != ""):
					equivalentPropertyList.append(resource)
			elif (pattern == startUnionOfPattern):
				lNum += 1
				while (lNum < numLinesinFile):
					line=lineList[lNum]
					if (re.search(endUnionOfPattern, line)):
						break
					else:
						if (re.search(resourcePattern, line)): 
							resource=processPattern(line, modelBase, ignoreVocabs_Dict, NSDict, resourcePattern, unionOfList)
						elif (re.search(aboutPattern, line)):
							resource=processPattern(line, modelBase, ignoreVocabs_Dict, NSDict, aboutPattern, unionOfList)
						lNum += 1
				if (resource != ""):
					unionOfList.append(resource)

		lNum += 1
		
	if (len(classList) > 0):
		fLinkToVocab=True
		rKey="Class"
		linksToDict[rKey]=classList

	if (len(objPropertyList) > 0):
		fLinkToVocab=True
		rKey="ObjectProperty"
		linksToDict[rKey]=objPropertyList

	if (len(importList) > 0):
		fLinkToVocab=True
		rKey="Import"
		linksToDict[rKey]=importList

	if (len(seeAlsoList) > 0):
		fLinkToVocab=True
		rKey="SeeAlso"
		linksToDict[rKey]=seeAlsoList

	if (len(isDefinedByList) > 0):
		fLinkToVocab=True
		rKey="IsDefinedBy"
		linksToDict[rKey]=isDefinedByList

	if (len(equivalentClassList) > 0):
		fLinkToVocab=True
		rKey="EquivalentClass"
		linksToDict[rKey]=equivalentClassList

	if (len(rangeList) > 0):
		fLinkToVocab=True
		rKey="Range"
		linksToDict[rKey]=rangeList

	if (len(subClassList) > 0):
		fLinkToVocab=True
		rKey="SubClassOf"
		linksToDict[rKey]=subClassList

	if (len(subPropertyList) > 0):
		fLinkToVocab=True
		rKey="SubPropertyOf"
		linksToDict[rKey]=subPropertyList

	if (len(equivalentPropertyList) > 0):
		fLinkToVocab=True
		rKey="EquivalentProperty"
		linksToDict[rKey]=equivalentPropertyList

	if (len(unionOfList) > 0):
		fLinkToVocab=True
		rKey="UnionOf"
		linksToDict[rKey]=unionOfList

	retValues.fLinksToVocab=fLinkToVocab
	retValues.retLinksToDict=linksToDict

	return(retValues)