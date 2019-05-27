import warc_test
import json
import os
import math

FILE = '10.warc.gz'
PATH = './data/'
TERM = 'termFile.json'
DOC = 'docFile.json'

def doHW2():
	if os.path.isdir(PATH) and os.path.isfile(PATH+TERM) and os.path.isfile(PATH+DOC):
		print('find the doc and term files. start reading.')
		with open(PATH+DOC, 'r') as reader:
			docFile = json.loads(reader.read())
		N = len(docFile)
		del docFile
		with open(PATH+TERM, 'r') as reader:
			termFile = json.loads(reader.read())
		print('terms:'+str(len(termFile))+' docs:'+str(N))
		query = raw_input('Query:').lower()
		while not query == 'n':
			query = query.split()
			appearDoc = set()
			q = {}
			for word in query:
				if q.has_key(word):
					q[word] += 1
				else:
					q[word] = 1
				if termFile.has_key(word):
				# 	print(word+' : '+str(termFile[word][0]))
					appearDoc = appearDoc | set(termFile[word][1].keys())
				else:
					print('not found.')
			appearDoc = tuple(appearDoc)
			
			# q tfidf
			q = {word:(1+math.log10(q[word])*math.log10(N/termFile[word][0])) if termFile.has_key(word) else 0 for word in query}

			# q normalize under
			qUnder = math.sqrt(sum(tuple(math.pow(v, 2) for v in q.values())))
			
			# d tfidf
			d = {}
			for doc in appearDoc:
				d[doc] = ({word:((1 + math.log10(termFile[word][1][doc][0]))*math.log10(N/termFile[word][0])) if termFile.has_key(word) and termFile[word][1].has_key(doc) else 0 for word in query})
			
			# d normalize under
			dUnder = {}
			for doc in d.keys():
				dUnder[doc] = math.sqrt(sum(tuple(math.pow(d[doc][word], 2) if d[doc].has_key(word) else 0 for word in query)))
			
			# sim(d,q)
			ans = {}
			for doc in appearDoc:
				ans[doc] = sum(tuple(q[word]*d[doc][word] if d[doc].has_key(word) else 0 for word in query)) / (dUnder[doc] * qUnder)

			# sort output
			ans = [str(doc[0])+' '+str(doc[1]) for doc in sorted(ans.iteritems(), key=lambda(k, v): (-float(v), int(k)))]
			for doc in ans:
				print(doc)
			
			# input
			query = raw_input('Query:').lower()
	else:
		print('Not found all file.')
		createFile = input('There isn\'t files, do you want to build it? (y/n)')
		createFile = createFile.lower()
		if createFile == 'y':
			print('start to build')
			os.mkdir(PATH)
			a = raw_input('What do you want to build, all or term or doc? ').lower()
			if a == 'term' or a == 'doc' or a == 'all':
				print('Build '+a)
				b = input('Limited? Small then 1 means all. ')
				warc_test.process_warc(FILE, PATH, TERM, DOC, a, b)
			else:
				print('No build')

doHW2()