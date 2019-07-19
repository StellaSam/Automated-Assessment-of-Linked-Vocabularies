import os
from os.path import isfile, join
import sys
import re
from openpyxl import Workbook
from openpyxl.worksheet.write_only import WriteOnlyCell
from openpyxl.styles import Font

from BuildVocabBase import *
from BuildDict import buildNSDict
from FindBase import *
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

def checkMetaData():
	fMetaData=False

	lineNo=0

	findStr0=":versionIRI"
	findStr1=":versionInfo"
	findStr2=":creator"
	findStr3=":contributor"
	findStr4=":license" 
	findStr5=":licence"
	
	while (lineNo < numLinesinFile):
		if (lineList[lineNo].find(findStr0) != -1) or (lineList[lineNo].find(findStr1) != -1):
			fMetaData=True
			break
		elif(lineList[lineNo].find(findStr2) != -1):
			fMetaData=True
			break
		elif(lineList[lineNo].find(findStr3) != -1):
			fMetaData=True
			break
		elif(lineList[lineNo].find(findStr4) != -1) or (lineList[lineNo].find(findStr5) != -1):
			fMetaData=True
			break

		lineNo+=1

	return(fMetaData)

def initExcelValues(vFile, bVocab, lToDict, fMeta, ranks):
	vocabFile=vFile
	baseOfVocab=bVocab
	linksToDict=lToDict
	fhasMetaData=fMeta
	stars=ranks

	class writeExcelValues:
		def _init_(self, vocabFile, baseOfVocab, linksToVocabDict, fhasMetaData, stars):
			self.vocabFile=""
			self.baseOfVocab=""
			self.linksToDict={}
			self.fhasMetaData=False
			self.stars=""

	writeExcelValues.vocabFile=vocabFile
	writeExcelValues.baseOfVocab=baseOfVocab
	writeExcelValues.linksToDict=linksToDict
	writeExcelValues.fhasMetaData=fhasMetaData
	writeExcelValues.stars=stars

	return(writeExcelValues)

#oPath="/Users/Stella/Documents/Ph.D. Research/Tool/Tool_Output_SWJ"
#oPath="/Users/Stella/Documents/Ph.D. Research/Tool/Tool_Output_LOV"
#oPath="/Users/Stella/Documents/Ph.D. Research/Base_URI_Tool/Base_URI_Tool_Output(SWJ)"
oPath="/Users/Stella/Documents/Ph.D. Research/Base_URI_Tool/Base_URI_Tool_Output(LOV)"
#oPath="YOUR OUTPUT FILE LOCATION HERE"
bFileName="vocab_Base.xlsx"
bFile=oPath+"/"+bFileName

fExistVocabBase=False
bVocabTypeList=[]
vBaseList=[]
if (os.path.isfile(bFile)):
	fExistVocabBase=True
	bVocabTypeList=buildBaseList(bFile)
eligVocabList=[]

#iPath="/Users/Stella/Documents/Ph.D. Research/Tool/Tool_Input_SWJ"
#iPath="/Users/Stella/Documents/Ph.D. Research/Tool/Tool_Input_LOV"
#iPath="/Users/Stella/Documents/Ph.D. Research/Base_URI_Tool/Base_URI_Tool_Input(SWJ)"
iPath="/Users/Stella/Documents/Ph.D. Research/Base_URI_Tool/Base_URI_Tool_Input(LOV)"
#iPath="YOUR INPUT FILE LOCATION HERE"	
filesOnly=[mFile for mFile in os.listdir(iPath) if isfile(join(iPath,mFile))]
currentWriteRow=2
oFileName="Ranked_Vocabs.xlsx"
oFile=oPath+'/'+oFileName
wb=Workbook()
ws=wb.active

for mFile in filesOnly: 
	if (mFile != ".DS_Store"):
		#star=1
		starList=['*']

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
			baseURL=findBase(lineList, NSDict,mFile)
			starList.append('*')

			modelBase=baseURL.vocabBase

			if (baseURL.fBase):
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
				if ((modelBase.find('.rdf')!= -1) or (modelBase.find('.owl') != -1)):
					#print("The base of this vocab is: " + modelBase)
					modelBase=extTempBase(modelBase)
					#print(modelBase)
					#input()

			#print("Aquired Star Rating of: ")

			fMetaDefined=False
			fMetaDefined=checkMetaData()
			if (fMetaDefined):
				starList.append('*')
			else:
				starList.append('-')
			
			#print("The ontology has now aquired a Star Rating of: ")

			linksToDict={}
			findLinksToVocab=checkLinksToVocab(lineList, numLinesinFile, modelBase, ignoreVocabs_Dict, NSDict)
			ffoundLinksToVocab=findLinksToVocab.fLinksToVocab

			if (ffoundLinksToVocab):
				linksToDict=findLinksToVocab.retLinksToDict
				addLinksToVocabBase(bFile, bVocabTypeList, linksToDict)
				starList.append('*')
			else:
				starList.append('-')
			#print("The 4 Star Rating of vocabulary: ")

			stars=""
			for rank in starList:
				stars=stars+rank
		
			writeVals=initExcelValues(mFileName, modelBase, linksToDict, fMetaDefined, stars)
			currentWriteRow = writeIntoExcel(ws, writeVals, currentWriteRow)+1			
wb.save(oFile)
