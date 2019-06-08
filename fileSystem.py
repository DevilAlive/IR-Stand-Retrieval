import os
import io
import json
import time

PATH = './data/'

def getDataList():
	if os.path.isdir(PATH):
		print('find the data.')
		datas = os.listdir(PATH)
		datas = tuple(os.path.splitext(data)[0] for data in datas)
		return datas

def readFile(name):
	if os.path.isdir(PATH) and os.path.isfile(PATH + '{}.txt'.format(name)):
		with io.open(PATH + '{}.txt'.format(name), 'r', encoding='utf8') as reader:
			return json.loads(reader.read())

def saveFile(N, url, doc, term):
	# print(data)
	data = {'url': url, 'doc': doc, 'term': term}
	with io.open(PATH + '{}.txt'.format(str(N) + '_' + time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())), 'w', encoding='utf8') as text_file:
		text_file.write(json.dumps(data, ensure_ascii=False))
	