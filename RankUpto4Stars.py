import os
from os.path import isfile, join
import sys
import re
from openpyxl import Workbook
from openpyxl.worksheet.write_only import WriteOnlyCell
from openpyxl.styles import Font

from BuildVocabBase import *
from BuildDict import buildNSDict
from FindBase import findBase
from CheckIfDuplicate import *
from TestLinksToVocab import *
from WriteExcel import writeIntoExcel

ignoreVocabs_Dict={"dcTerms": "<http://purl.org/dc/terms/>",
"dcElements": "<http://purl.org/dc/elements/1.1>",
"foaf": "<http://xmlns.com/foaf/0.1/>",
"owl": "<http://www.w3.org/2002/07/owl#>",
"prov": "<http://www.w3.org/ns/prov#>",
"rdfSchema": "<http://www.w3.org/2000/01/rdf-schema#>",
"rdfSyntax": "<http://www.w3.org/1999/02/22-rdf-syntax-ns#>",
"xmlSchema": "<http://www.w3.org/2001/XMLSchema#>"
}

def incStar(rating):
	rating += 1
	return(rating)

def checkForVersionInfo():
	fVersionInfo=False

	lineNo=0
	findStr="<owl:versionInfo"
	while (lineNo < numLinesinFile):
		if (lineList[lineNo].find(findStr) != -1):
			fVersionInfo=True
			break

	return(fVersionInfo)

def initExcelValues(vFile, bVocab, lToDict, fMeta, sRate):
	vocabFile=vFile
	baseOfVocab=bVocab
	linksToDict=lToDict
	fhasMetaData=fMeta
	starRate=sRate

	class writeExcelValues:
		def _init_(self, vocabFile, baseOfVocab, linksToVocabDict, fhasMetaData, starRate):
			self.vocabFile=""
			self.baseOfVocab=""
			self.linksToDict={}
			self.fhasMetaData=False
			self.starRate=0

	writeExcelValues.vocabFile=vocabFile
	writeExcelValues.baseOfVocab=baseOfVocab
	writeExcelValues.linksToDict=linksToDict
	writeExcelValues.fhasMetaData=fhasMetaData
	writeExcelValues.starRate=sRate

	return(writeExcelValues)

oPath="/Users/Stella/Documents/Ph.D. Research/Code/Output(SWJ)"
bFileName="vocab_Base.xlsx"
bFile=oPath+"/"+bFileName

fExistVocabBase=False
bVocabTypeList=[]
vBaseList=[]
if (os.path.isfile(bFile)):
	fExistVocabBase=True
	bVocabTypeList=buildBaseList(bFile)
eligVocabList=[]

iPath="/Users/Stella/Documents/Ph.D. Research/Code/Input(SWJ)"
filesOnly=[mFile for mFile in os.listdir(iPath) if isfile(join(iPath,mFile))]
currentWriteRow=2
oFileName="Ranked_Vocabs.xlsx"
oFile=oPath+'/'+oFileName
wb=Workbook()
ws=wb.active

for mFile in filesOnly: 
	if (mFile != ".DS_Store"):
		star=1

		rdfFile=False
		owlFile=False
		fFileTypeHandled=True

		mFileName, mFileExt=os.path.splitext(mFile)

		if (mFileExt==".rdf"):
			rdfFile=True
		elif (mFileExt==".owl"):
			owlFile=True
		else:
			print("File Type Not Handled")
			fFileTypeHandled=False

		if (fFileTypeHandled):
			lineList=[]
			try:
				with open(iPath+"/"+mFile,"rt") as processFile:
					for line in processFile:
						lineList.append(line)
			except IOError: 
				print("Input Output Exception in Opening File")
				sys.exit()

			numLinesinFile=len(lineList)

			NSDict={}
			NSDict=buildNSDict(lineList, numLinesinFile)

			fDupVocab=False
			baseURL=findBase(lineList, NSDict)
			modelBase=baseURL.vocabBase
			if (baseURL.fBase):
				star=incStar(star)
				if (fExistVocabBase):
					fDupVocab=checkIfDupBase(modelBase, bVocabTypeList)

				if (fExistVocabBase and (not fDupVocab)):
					addToVocabBase(bFile, modelBase)
				else:
					createVocabBase(bFile, modelBase)
					fExistVocabBase=True
			else:
				if (fExistVocabBase):
					addToVocabBase(bFile, "Base URL not defined (" + mFile +")")
				else:
					createVocabBase(bFile, "Base URL not defined (" + mFile +")")

			print("Aquired Star Rating of: "+str(star))

			linksToDict={}
			findLinksToVocab=checkLinksToVocab(lineList, numLinesinFile, modelBase, ignoreVocabs_Dict, NSDict)
			ffoundLinksToVocab=findLinksToVocab.fLinksToVocab

			if (ffoundLinksToVocab):
				linksToDict=findLinksToVocab.retLinksToDict
				addLinksToVocabBase(bFile, bVocabTypeList, linksToDict)
				star=incStar(star)
			print("Now aquired Star Rating of: "+str(star))

			if (checkForVersionInfo):
				fMetaData=True
			if (fMetaData):
				star=incStar(star)
			print("The ontology has now aquired a Star Rating of: " + str(star))

			writeVals=initExcelValues(mFileName, modelBase, linksToDict, fMetaData, star)
			currentWriteRow = writeIntoExcel(ws, writeVals, currentWriteRow)+1			
wb.save(oFile)
