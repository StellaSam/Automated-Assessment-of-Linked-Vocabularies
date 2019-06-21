def checkIfBase(mResource, modelBase):
	fBase=False

	if ((mResource == modelBase) or (len(mResource) > len(modelBase) and (mResource.find(modelBase) != -1)) or (len(modelBase) > len(mResource) and (modelBase.find(mResource) != -1))):
		fBase=True

	return(fBase)
