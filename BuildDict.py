import re

def buildNSDict(lineList, numLinesinFile):
	fFound=False
	findStr="xmlns:"
	currentLineNo=0
	NSDict={}

	while (currentLineNo < numLinesinFile):
		if (lineList[currentLineNo].find(findStr) != -1):
			if (not fFound):
				fFound=True

			line=lineList[currentLineNo]
			lst=line.split('xmlns:')
			for item in lst:
				item=item.strip()
				equPos=item.find('=')
				if (equPos != -1):
					mKey=item[0:equPos]
					mVal=item[equPos+2:]

					if (mVal.rfind('>') == len(mVal)-1):
						mVal=mVal[0:len(mVal) - 1]

					if (mVal.rfind('"') == len(mVal)-1):
						mVal=mVal[0:len(mVal) - 1]

					if (mVal.rfind('/') == len(mVal)-1):
						mVal=mVal[0:len(mVal) - 1]
			
					if (mVal.rfind('#') == len(mVal)-1):
						mVal=mVal[0:len(mVal) - 1]

					NSDict.update({mKey:mVal})
		else:
			if (fFound):
				break
		currentLineNo += 1

	return(NSDict)
