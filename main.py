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

async def getWebContents(website):
	print('getWebContents')


async def getWebPosts(indexHTML):
	print('getWebPosts')
	links = []
	if not indexHTML == None:
		for index, page in enumerate(data.getPttLinks(indexHTML)):
			# 取得所有page的所有post
			pageHTML = await crawler.getHTML(page)
			links.append(data.getPttPosts(pageHTML))
			print('finish:{}/100'.format(index))
	return tuple(links)


async def getWebList(website):
	print('getWebsites')
	if website == 'PTT':
		# 取得index
		return await crawler.getHTML(PTT)

def getWebsite():
	print('getData')

def readFile(name):
	print('readFile: '+name)

def computeWeight():
	print('computeWeight')

# 非同步任務
loop = asyncio.get_event_loop()
print('Hello World! IR-Stand-Retrieval')
index = input('\n你想要使用新資料集，亦或是舊有資料集呢？\n請輸入選項數字\n(1) 新資料集\n'+'\n'.join(searchFile())+'\n')

if index == '1':
	web = input('\n你想要爬哪個網站？\n請輸入選項數字\n(1)PTT\n')
	if web == '1':
		allLink = loop.run_until_complete(getWebPosts(loop.run_until_complete(getWebList('PTT'))))
else:
	readFile(dataList[int(index)-2])