import aiohttp
import asyncio

async def getHTML(website):
	# print('-----------------get: {}----------------'.format(website))
	async with aiohttp.ClientSession(cookies={'over18': '1'}) as session:
		async with session.get(website) as res:
			temp = await res.text()
			# print('----------------done: {}----------------'.format(website))
			return temp