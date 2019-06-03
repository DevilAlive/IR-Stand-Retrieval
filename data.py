from bs4 import BeautifulSoup

PTT_DOMAIN = 'https://www.ptt.cc'

def getPttLinks(html):
	print('data -> getHTML')
	# https://www.ptt.cc/bbs/[看板]/index[頁碼].html
	tree = BeautifulSoup(html, 'lxml')
	page = tree.find('div', 'btn-group-paging')
	for item in page.find_all('a'):
		if '上頁' in item.text:
			pageNum = item['href'][item['href'].find('index')+5:item['href'].find('.html')]
			return tuple('https://www.ptt.cc/bbs/Gossiping/index{}.html'.format(Num) for Num in range(int(pageNum)-100, int(pageNum)+1))

def getPttPosts(html):
	print('data -> getPttPosts')
	tree = BeautifulSoup(html, 'lxml')
	titles = tree.find_all('div', 'r-ent')
	return tuple(PTT_DOMAIN + title.find('div', 'title').find('a').get('href') for title in titles if title.find('div', 'title').find('a'))

def getPttContent(html):
	print('data -> getTerms')
	tree = BeautifulSoup(html, 'lxml')

	# body = tree.body
	# if body is None:
	# 	return None

	# for tag in body.select('script'):
	# 	tag.decompose()
	# for tag in body.select('style'):
	# 	tag.decompose()
		
	return tree.find(id='main-content')