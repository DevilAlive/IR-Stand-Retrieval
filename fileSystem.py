import os

PATH = './data/'

def getDataList():
	print('check datas.')
	if os.path.isdir(PATH):
		datas = os.listdir(PATH)
		datas = tuple(os.path.splitext(data)[0] for data in datas)
		return datas
	