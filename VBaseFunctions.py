def setIndices(row):
	colA='A'
	colB='B'
	colC='C'
	colD='D'
	colE='E'
	colF='F'
	colG='G'

	class retIndices:
		def _init_ (self, aInd, bInd, cInd, dInd, eInd, fInd):
			self.aInd=""
			self.bInd=""
			self.cInd=""
			self.dInd=""
			self.eInd=""
			self.fInd=""
			self.gInd=""

	retIndices.aInd=colA+str(row)
	retIndices.bInd=colB+str(row)
	retIndices.cInd=colC+str(row)
	retIndices.dInd=colD+str(row)
	retIndices.eInd=colE+str(row)
	retIndices.fInd=colF+str(row)
	retIndices.gInd=colG+str(row)

	return(retIndices)

def collectBVocabInfo(vocab, bFile, bwb, bws, row):
	colA='A'
	colB='B'
	colC='C'
	aInd=colA+str(row)
	bInd=colB+str(row)
	cInd=colC+str(row)

	retBaseDict={}
	retLinksDict={}

	class retBVocabInfo:
		def _init_ (self, retBaseDict, retLinksDict, retRow):
			self.retBaseDict={}
			self.retLinksDict={}
			self.retRow=row

	if (bws[bInd].value == "Base"):
		retBaseDict[bws[aInd].value]=row

		row += 1
		bInd=colB+str(row)
		while (bws[bInd].value == "Link"):
			aInd=colA+str(row)
			bInd=colB+str(row)
			cInd=colC+str(row)
			if (bws[bInd].value == "Link"):	
				retLinksDict[bws[aInd].value]=row
				row += 1

	retBVocabInfo.retBaseDict=retBaseDict
	retBVocabInfo.retLinksDict=retLinksDict
	retBVocabInfo.retRow=row

	return(retBVocabInfo)

def collectFromLinksInfo(vocab, bFile, bws, row):
	colA='A'
	colB='B'
	aInd=colA+str(row)
	bInd=colB+str(row)

	maxRow=bws.max_row
	fromLinksList=[]

	class retFromLinksInfo:
		def _init_ (self, retFromLinksList, retRow):
			self.retFromLinksList=[]
			self.retRow=row

	if (bws[bInd].value != None):
		fromLinksList.append(bws[bInd].value)
	
	row += 1
	aInd=colA+str(row)
	bInd=colB+str(row)
	while ((row <= maxRow) and (bws[aInd].value == None)):
		if (bws[bInd].value != None):
			fromLinksList.append(bws[bInd].value)
		row += 1
		aInd=colA+str(row)
		bInd=colB+str(row)
		
	retFromLinksInfo.retFromLinksList=fromLinksList
	retFromLinksInfo.retRow=row
	return(retFromLinksInfo)