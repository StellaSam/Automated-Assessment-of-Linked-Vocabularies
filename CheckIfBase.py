def checkIfBase(mResource, modelBase):
	fBase=False

	#print(modelBase)
	#print("The URI to be compared is: " + mResource)
	mResource=mResource.lower()
	modelBase=modelBase.lower()

	if ((mResource == modelBase) 
		or (len(mResource) > len(modelBase) and (mResource.find(modelBase) != -1)) 
		or (len(modelBase) > len(mResource) and (modelBase.find(mResource) != -1))):
		fBase=True
		#print("Match Found with base")

	# print("Base found? " + str(fBase))
	# input()
	return(fBase)
