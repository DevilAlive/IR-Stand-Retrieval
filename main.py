import crawler
import data
import fileSystem
import weight
import show
import asyncio
import io

dataList = []
PTT = 'https://www.ptt.cc/bbs/Gossiping/index.html'
PTT_DOMAIN = 'https://www.ptt.cc'

def searchFile():
	global dataList
	dataList = fileSystem.getDataList()
	return tuple('('+str(index+2)+') '+dataList[index] for index in range(len(dataList)))

async def getWebContents(url):
	print('getWebContents')
	# 取得文章的內容與所有回覆
	contentHTML = await crawler.getHTML(url)
	return data.getPttContent(contentHTML)

async def getWebPosts(url, pageIndex):
	print('getWebPosts')
	# 非同步取得頁面的所有文章
	print('start page: {}'.format(pageIndex))
	pageHTML = await crawler.getHTML(url)
	postTasks = tuple(getWebContents(post) for post in data.getPttPosts(pageHTML))
	temp = await asyncio.gather(*postTasks)
	print('end page: {}'.format(pageIndex))
	return temp

async def getWebList(website, page):
	print('getWebsites')
	# 取得頁碼網址
	if website == 'PTT':
		indexHTML = await crawler.getHTML(PTT)
		return data.getPttLinks(indexHTML, int(page))

async def getDocument(website, page):
	pageList = await getWebList(website, page)
	pageTasks = tuple(getWebPosts(page, index) for index, page in enumerate(pageList))
	return await asyncio.gather(*pageTasks)

def getWebsite():
	print('getData')

def readFile(name):
	print('readFile: '+name)

def computeWeight():
	print('computeWeight')

async def main():
	print('Hello World! IR-Stand-Retrieval')
	index = input('\n你想要使用新資料集，亦或是舊有資料集呢？\n請輸入選項數字\n(1) 新資料集\n'+'\n'.join(searchFile())+'\n')

	if index == '1':
		web = input('\n你想要爬哪個網站？\n請輸入選項數字\n(1)PTT\n')
		if web == '1':
			doc = await getDocument('PTT', 2)
			print(doc)
			with io.open("Output.txt","w",encoding = "utf8") as text_file:
				text_file.write(u'\n'.join(tuple('\n'.join(page) for page in doc)))
	else:
		readFile(dataList[int(index)-2])

# 非同步任務
if __name__ == "__main__":
	loop = asyncio.get_event_loop()
	loop.run_until_complete(main())
