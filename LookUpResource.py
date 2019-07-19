import re

def lookUpResource(mResource):
	findChar=';'
	lookUpKey=""

	charPos=mResource.find(findChar)
	if (charPos != -1):
		lookUpKey=mResource[1:charPos]

	return(lookUpKey)
	