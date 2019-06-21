from BuildDict import buildNSDict
from LookUpResource import lookUpResource

def extractBase(line, iPattern):
	Pos=line.find(iPattern)
	startPos=Pos+len(iPattern)
	extResource=line[startPos+1::]
	endPos=extResource.find('"')
	extResource=extResource[0:endPos]
	if (extResource[endPos-1] == '/'):
		extResource=extResource[0:endPos-1]
	endPos-=1
	if (extResource.find('#') != -1):
		extResource=extResource[0:len(extResource)-1]
	return(extResource)

def findBase(lineList, NSDict):
	fHasBase = False
	vBase=""

	class baseValues:
		def _init_(self, fBase, vocabBase):
			self.fBase=False,
			self.vocabBase=""

	findStr1="<owl:Ontology rdf:about="
	findStr2="xml:base="
	for line in lineList:
		if (line.find(findStr1) != -1):
			fHasBase=True
			vBase=extractBase(line, findStr1)
		elif (line.find(findStr2) != -1):
			fHasBase=True
			vBase=extractBase(line, findStr2)
			break
	
	if (fHasBase):
		if (vBase.find('&') != -1):
			lookUpKey=lookUpResource(vBase)
			vBase=NSDict[lookUpKey]
	else:
		print("Base not found")

	baseValues.fBase=fHasBase
	baseValues.vocabBase=vBase
	return(baseValues)