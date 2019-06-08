from bs4 import BeautifulSoup
import re
import jieba
import time

PTT_DOMAIN = 'https://www.ptt.cc'

def getPttLinks(html, quantity):
	# print('data -> getHTML')
	# https://www.ptt.cc/bbs/[看板]/index[頁碼].html
	tree = BeautifulSoup(html, 'lxml')
	page = tree.find('div', 'btn-group-paging')
	for item in page.find_all('a'):
		if '上頁' in item.text:
			pageNum = item['href'][item['href'].find('index')+5:item['href'].find('.html')]
			return tuple('https://www.ptt.cc/bbs/Gossiping/index{}.html'.format(Num) for Num in range(int(pageNum)+1-int(quantity), int(pageNum)+1))

def getPttPosts(html):
	# print('data -> getPttPosts')
	tree = BeautifulSoup(html, 'lxml')
	titles = tree.find_all('div', 'r-ent')
	return tuple(PTT_DOMAIN + title.find('div', 'title').find('a').get('href') for title in titles if title.find('div', 'title').find('a'))

def getPttContent(html):
	# print('data -> getTerms')
	tree = BeautifulSoup(html, 'lxml')
	contentSection = tree.find('div', id='main-content')
	result = ' '.join(tuple(content.strip().replace('\n', ' ') for content in contentSection.find_all(text=True) if content.parent.name == 'div' and content.strip()))
	for comment in contentSection.find_all('div', 'push'):
		result += comment.find('span', 'push-tag').text.strip() + ' ' + comment.find('span', 'push-content').text.strip()[2:] + ' '
	return result

def termTransform(pages):
	# print('data -> getTerm')
	# with io.open("Output.txt","r",encoding = "utf8") as f:
	# 	text = f.read()
	start_time_jieba = time.time()
	seg_list = []
	for page in pages:
		seg_list += tuple(tuple(tuple(re.sub(r'\W', '', term) for term in jieba.lcut(text) if not re.search(r'\W', term))) for text in page)
	# with io.open("cut_jieba.txt","w",encoding = "utf8") as f:
	# 	f.write(" ".join(seg_list))
	print("Total running time of jieba: {}".format(time.time() - start_time_jieba))
	return tuple(seg_list)

def getDoc(terms):
	# print('data -> makeTerm')
	docFile = {}
	for index, term in enumerate(terms):
		if term in docFile:
			docFile[term].append(index)
		else:
			docFile[term] = [index]
	return docFile

def getData(docs):
	# print('data -> makeDoc')
	dataFile = {}
	for index, doc in enumerate(docs):
		docFile = getDoc(doc)
		for term in docFile.keys():
			pos = tuple(docFile[term])
			if term in dataFile:
				dataFile[term][0] += 1
				dataFile[term][1][index] = (len(pos), pos)
			else:
				dataFile[term] = [1, {index: (len(pos), pos)}]
	return len(docs), dataFile

def getQuery(query):
	return tuple(re.sub(r'\W', '', word) for word in jieba.lcut(query) if not re.search(r'\W', word))