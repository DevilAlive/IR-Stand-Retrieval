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
	global dataList
	dataList = fileSystem.getDataList()
	return tuple('('+str(index+2)+') '+dataList[index] for index in range(len(dataList)))

async def getWebContents(url):
	print('getWebContents')
	# 取得文章的內容與所有回覆
	contentHTML = await crawler.getHTML(url)
	return data.getPttContent(contentHTML)

async def getWebPosts(url):
	print('getWebPosts')
	# 取得頁面的所有文章
	pageHTML = await crawler.getHTML(url)
	return data.getPttPosts(pageHTML)

async def getWebList(website):
	print('getWebsites')
	# 取得頁碼網址
	if website == 'PTT':
		indexHTML = await crawler.getHTML(PTT)
		return data.getPttLinks(indexHTML, 3)

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
			pageList = await getWebList('PTT')
			# print(pageList)
			contentList = []
			for pageIndex, page in enumerate(pageList):
				print('start page: {}'.format(pageIndex))
				postList = await getWebPosts(page)
				# print(postList)
				tasks = []
				for postIndex, post in enumerate(postList):
					tasks.append(getWebContents(post))
					# contentList.append(loop.run_until_complete(getWebContents(post)))
				contentList.append(await asyncio.gather(*tasks))
				print('end page: {}'.format(pageIndex))
			print(contentList)
			
			# allLink = loop.run_until_complete()
	else:
		readFile(dataList[int(index)-2])

# 非同步任務
if __name__ == "__main__":
	loop = asyncio.get_event_loop()
	loop.run_until_complete(main())
