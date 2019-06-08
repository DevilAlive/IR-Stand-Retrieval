import crawler
import data
import fileSystem
import weight
import show
import asyncio

dataList = []
PTT = 'https://www.ptt.cc/bbs/Gossiping/index.html'
PTT_DOMAIN = 'https://www.ptt.cc'

def searchFile():
	dataList = fileSystem.getDataList()
	return dataList, tuple('('+str(index+2)+') '+dataList[index] for index in range(len(dataList)))

async def getWebContents(url):
	# print('getWebContents')
	# 取得文章的內容與所有回覆
	contentHTML = await crawler.getHTML(url)
	return data.getPttContent(contentHTML)

async def getWebPosts(url, pageIndex):
	# print('getWebPosts')
	# 非同步取得頁面的所有文章
	print('start page: {}'.format(pageIndex))
	pageHTML = await crawler.getHTML(url)
	page = data.getPttPosts(pageHTML)
	postTasks = tuple(getWebContents(post) for post in page)
	temp = await asyncio.gather(*postTasks)
	print('end page: {}'.format(pageIndex))
	return page, temp

async def getWebList(website, page):
	# print('getWebsites')
	# 取得頁碼網址
	if website == 'PTT':
		indexHTML = await crawler.getHTML(PTT)
		return data.getPttLinks(indexHTML, int(page))

async def getDocument(website, page):
	pageList = await getWebList(website, page)
	pageTasks = tuple(getWebPosts(page, index) for index, page in enumerate(pageList))
	temp = await asyncio.gather(*pageTasks)
	url = tuple(content[0] for content in temp)
	doc = tuple(content[1] for content in temp)
	return url, doc

def readFile(name):
	# print('readFile: '+name)
	N = int(name.split('_')[0])
	data = fileSystem.readFile(name)
	return N, data['url'], data['doc'], data['term']

def computeWeight(query, N, doc, term):
	# print('computeWeight')
	query = data.getQuery(query)
	return weight.getTFIDF(query, N, doc, term)

async def main():
	print('Hello World! IR-Stand-Retrieval')
	dataList, strList = searchFile()
	index = input('\n你想要使用新資料集，亦或是舊有資料集呢？\n請輸入選項數字\n(1) 新資料集\n'+'\n'.join(strList)+'\n')
	
	N, url, doc, term = None, None, None, None
	if index == '1':
		web = input('\n你想要爬哪個網站？\n請輸入選項數字\n(1)PTT\n')
		if web == '1':
			num = input('\n你想要抓多少頁數？\n請輸入數字\n')
			links, doc = await getDocument('PTT', num)
			url = []
			for link in links:
				url += link
			doc = data.termTransform(doc)
			N, term = data.getData(doc)
			fileSystem.saveFile(N, link, doc, term)
	else:
		N, url, doc, term = readFile(dataList[int(index)-2])

	query = input('\ninput:')
	while query != 'n':
		tfidfList = computeWeight(query, N, doc, term)
		print('搜尋結果:')
		for doc in tfidfList:
			link = url[int(doc.split()[0])]
			tfidf = doc.split()[1]
			print(link + ' -> ' + tfidf)
		query = input('\n關鍵字:')

# 非同步任務
if __name__ == "__main__":
	loop = asyncio.get_event_loop()
	loop.run_until_complete(main())
