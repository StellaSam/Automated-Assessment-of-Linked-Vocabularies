def inIgnoreVocabList(mResource, ignoreVocabs_Dict):
	fIgnoreVocab=False

	for key,vocab in ignoreVocabs_Dict.items():	
		if (vocab.find(mResource) != -1) or ((len(mResource) > len(vocab)) and (mResource.find(vocab[1:len(vocab)-1]) != -1)):
			fIgnoreVocab=True

	return(fIgnoreVocab)