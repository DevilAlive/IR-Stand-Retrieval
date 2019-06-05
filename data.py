from bs4 import BeautifulSoup

PTT_DOMAIN = 'https://www.ptt.cc'

def getPttLinks(html, quantity):
	print('data -> getHTML')
	# https://www.ptt.cc/bbs/[看板]/index[頁碼].html
	tree = BeautifulSoup(html, 'lxml')
	page = tree.find('div', 'btn-group-paging')
	for item in page.find_all('a'):
		if '上頁' in item.text:
			pageNum = item['href'][item['href'].find('index')+5:item['href'].find('.html')]
			return tuple('https://www.ptt.cc/bbs/Gossiping/index{}.html'.format(Num) for Num in range(int(pageNum)+1-int(quantity), int(pageNum)+1))

def getPttPosts(html):
	print('data -> getPttPosts')
	tree = BeautifulSoup(html, 'lxml')
	titles = tree.find_all('div', 'r-ent')
	return tuple(PTT_DOMAIN + title.find('div', 'title').find('a').get('href') for title in titles if title.find('div', 'title').find('a'))

def getPttContent(html):
	print('data -> getTerms')
	result = ''
	tree = BeautifulSoup(html, 'lxml')
	contentSection = tree.find('div', id='main-content')
	result += ' '.join(tuple(content.strip().replace('\n\n', '\n') for content in contentSection.find_all(text=True) if content.parent.name == 'div' and content.strip()))
	for comment in contentSection.find_all('div', 'push'):
		result += comment.find('span', 'push-tag').text.strip() + ' ' + comment.find('span', 'push-content').text.strip()[2:] + '\n'
	return result