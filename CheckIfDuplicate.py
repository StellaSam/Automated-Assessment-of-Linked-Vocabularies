def checkIfDuplicate(mResource, resourceList):
	fDuplicate=False

	for item in resourceList:
		if (mResource == item or (len(mResource) > len(item) and mResource.find(item) != -1)):
			fDuplicate=True
			break

	return(fDuplicate)

def checkIfDupBase(mResource, twoElementsList):
	fDuplicate=False

	checkType="Base"
	for item in twoElementsList:
		if ((item[1] == checkType) and (mResource == item[0])):
			fDuplicate=True
			break

	return(fDuplicate)

def checkIfDupLink(mResource, twoElementsList):
	fDuplicate=False

	checkType="Link"
	for item in twoElementsList:
		if ((item[1] == checkType) and (mResource == item[0])):
			fDuplicate=True
			break
	
	return(fDuplicate)