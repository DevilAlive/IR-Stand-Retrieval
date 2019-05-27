from time import time
import warc
# python2
# from selectolax.parser
# from HTMLParser import HTMLParser
# python3
# from html.parser import HTMLParser
from bs4 import BeautifulSoup
import re
# import sys
import unicodedata
import json
import psutil

FILE = '10.warc.gz'
PATH = './data/'
TERM = 'termFile.json'
DOC = 'docFile.json'

def clean_word(word):
	if re.search(r'\w', word):
		try:
			word = unicode(word, 'utf-8')
		except (TypeError, NameError):
			pass
		word = unicodedata.normalize('NFD', word)
		word = word.encode('ascii', 'ignore')
		word = word.decode('utf-8')
		word = word.lower()
		if re.search(r'\w+\W+more', word):
			word = re.sub(r'\W+more', '', word)
		word = re.sub(r'\W+', '', word)
		word = re.sub(r'\d+', '', word)
		return word.encode('utf-8')
	return ''

def make_file(text, job):
	terms = {}
	docs = []
	term = False
	doc = False
	if job == 'term':
		term = True
	elif job == 'doc':
		doc = True
	elif job == 'all':
		term = True
		doc = True

	for i,word in enumerate(text.split()):
		cleanWord = clean_word(word)
		if not cleanWord == '':
			if doc:
				docs.append(cleanWord)
			if term:
				if terms.has_key(cleanWord):
					terms[cleanWord].append(i)
				else:
					terms[cleanWord] = [i]
	return (docs,terms)

def get_text_bs(html):
	tree = BeautifulSoup(html, 'lxml')

	body = tree.body
	if body is None:
		return None

	for tag in body.select('script'):
		tag.decompose()
	for tag in body.select('style'):
		tag.decompose()

	text = body.get_text(separator='\n')
	return text


def read_doc(record, parser=get_text_bs):
	url = record.url
	text = None

	if url:
		payload = record.payload
		header, html = payload.split(b'\n\n', 1)
		html = html.strip()

		if len(html) > 0:
			text = parser(html)

	return url, text


def process_warc(file_name, save_path, term_file, doc_file, job, limit=0):
	existed_limit=True if limit>0 else False
	warc_file = warc.open(file_name, 'rb')
	t0 = time()
	termFile = {}
	docFile = {}
	doTerm = False
	doDoc = False
	n_documents = 0
	if job == 'term':
		doTerm = True
	elif job == 'doc':
		doDoc = True
	elif job == 'all':
		doTerm = True
		doDoc = True

	startMemory = psutil.virtual_memory().available

	for i,record in enumerate(warc_file):
		
		if existed_limit:
			if i > limit:
				break

		url, text = read_doc(record, get_text_bs)
		if not text or not url:
			continue
		# print(text.encode("utf8").decode("cp950", "ignore"))

		print('\nFile:'+str(i))

		# build term
		docs = []
		terms = {}
		(docs, terms) = make_file(text, job)
		
		# doc
		if doDoc:
			docFile[i] = tuple(docs)

		# term
		if doTerm:
			for term in terms.keys():
				pos = tuple(terms[term])
				if termFile.has_key(term):
					termFile[term][0] += 1
					termFile[term][1][i] = (len(pos),pos)
				else:
					termFile[term] = [1,{i:(len(pos),pos)}]

		n_documents += 1

	print('Memory usage {} Bytes'.format(startMemory-psutil.virtual_memory().available))

	warc_file.close()
	print('Parsing took %s seconds and produced %s documents\n' % (time() - t0, n_documents))

	if doDoc:
		# jsonFile = json.dumps(termFile)
		f = open((save_path+doc_file), 'w')
		json.dump(docFile, f)
		# f.write(jsonFile)
		f.close()

	if doTerm:
		termFile = {term:termFile[term] for term in sorted(termFile)}
		# jsonFile = json.dumps(termFile)
		f = open((save_path+term_file), 'w')
		json.dump(termFile, f)
		# f.write(jsonFile)
		f.close()
