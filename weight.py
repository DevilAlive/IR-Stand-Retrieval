import math

def getP(query, termFile):
	appearDoc = set()
	q = {}
	for word in query:
		if word in q:
			q[word] += 1
		else:
			q[word] = 1
		if word in termFile:
		# 	print(word+' : '+str(termFile[word][0]))
			appearDoc = appearDoc | set(termFile[word][1].keys())
		# else:
		# 	print('not found.')
	return q, tuple(appearDoc)

def getTFIDF(query, N, docFile, termFile):
	q, appearDoc = getP(query, termFile)
	# q tfidf
	q = {word:(1+math.log10(q[word])*math.log10(N/termFile[word][0])) if word in termFile else 0 for word in query}

	# q normalize under
	qUnder = math.sqrt(sum(tuple(math.pow(v, 2) for v in q.values())))
	
	# d tfidf
	d = {}
	for doc in appearDoc:
		words = {}
		for word in docFile[int(doc)]:
			if word in words:
				words[word] += 1
			else:
				words[word] = 1
		d[doc] = ({word:((1 + math.log10(words[word]))*math.log10(N/termFile[word][0])) for word in words.keys()})

	# d = {}
	# for doc in appearDoc:
	# 	d[doc] = ({word:((1 + math.log10(termFile[word][1][doc][0]))*math.log10(N/termFile[word][0])) if word in termFile and doc in termFile[word][1] else 0 for word in query})
	
	# d normalize under
	dUnder = {}
	for doc in d.keys():
		dUnder[doc] = (math.sqrt(sum(tuple(math.pow(value, 2) for value in d[doc].values()))))
	# dUnder = {}
	# for doc in d.keys():
	# 	dUnder[doc] = math.sqrt(sum(tuple(math.pow(d[doc][word], 2) if word in d[doc] else 0 for word in query)))
	
	# sim(d,q)
	ans = {}
	for doc in appearDoc:
		if dUnder[doc] != 0 and qUnder != 0:
			ans[doc] = sum(tuple(q[word]*d[doc][word] if word in d[doc] else 0 for word in query)) / (dUnder[doc] * qUnder)
		else:
			ans[doc] = 0

	# sort output
	ans = [str(doc[0])+' '+str(doc[1]) for doc in sorted(ans.items(), key=lambda kv: (-float(kv[1]), int(kv[0])))]
	# for doc in ans:
	# 	print(doc)
	return ans