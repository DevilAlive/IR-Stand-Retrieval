import requests as rq

async def getHTML(website):
	html = rq.get(website, cookies={'over18': '1'})
	return html.text