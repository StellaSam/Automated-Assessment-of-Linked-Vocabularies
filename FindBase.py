from BuildDict import buildNSDict
from LookUpResource import lookUpResource

def extractBase(line, iPattern):
	Pos=line.find(iPattern)
	startPos=Pos+len(iPattern)
	extResource=line[startPos+1::]
	endPos=extResource.find('"')
	if (endPos > 0):
		extResource=extResource[0:endPos]
		if (extResource[endPos-1] == '/'):
			extResource=extResource[0:endPos-1]
		endPos-=1
		if (extResource.find('#') != -1):
			extResource=extResource[0:len(extResource)-1]
	else:
		extResource=""
	return(extResource)

def findBase(lineList, NSDict, iFName):
	fHasBase = False
	vBase=""

	class baseValues:
		def _init_(self, fBase, vocabBase):
			self.fBase=False,
			self.vocabBase=""

	findStr1="xml:base="
	findStr2="<owl:Ontology rdf:about="
	findStr3="<void:Dataset rdf:about="
	findStr4="xmlns:schema="
	for line in lineList:
		if (line.find(findStr1) != -1):
			fHasBase=True
			vBase=extractBase(line, findStr1)
			break
		elif (line.find(findStr2) != -1):
			fHasBase=True
			vBase=extractBase(line, findStr2)
			break
		elif (line.find(findStr3) != -1):
			fHasBase=True
			vBase=extractBase(line,findStr3)
			break
		elif (line.find(findStr3) != -1):
			fHasBase=True
			vBase=extractBase(line,findStr4)
			break
	
	if (fHasBase and vBase != ""):
		if (vBase.find('&') != -1):
			lookUpKey=lookUpResource(vBase)
			vBase=NSDict[lookUpKey]
	else:
		print("Base not found")
		vBase=iFName

	baseValues.fBase=fHasBase
	baseValues.vocabBase=vBase
	return(baseValues)

def extTempBase(mBase):	
	mBase=mBase[0:len(mBase)-4]
	#print("Now the base to be compared is: " + mBase)
		
	if (mBase.find('-') != -1):
		#print("hyphen found")
		tillPos=mBase.find('-')
		#print(str(tillPos))
		mBase=mBase[0:tillPos]
		#print("After removing hyphen, base to be compared is: " + mBase)

	if (mBase.find('_') != -1):
		#print("underscore found")
		tillPos=mBase.find('_')
		#print(str(tillPos))
		mBase=mBase[0:tillPos]
		#print("After removing underscore, base to be compared is: " + mBase)
	return(mBase)