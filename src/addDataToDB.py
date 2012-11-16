import os, sys
import urllib2
from stat import *
import re
def main():
	# read from database?
	# read from file?
	layoutList = readData()
def readData():
	layoutList = []
	for f in os.listdir('../data'):
		pathname = os.path.join('../data', f)
		mode = os.stat(pathname).st_mode
		if S_ISREG(mode):
			fp = open(pathname,'r')
			boxList = []
			data = "data="
			headData = 1
			for line in fp:
				strList = line.strip().split()
				box = [int(ele) for ele in strList]
				if headData == 1:
					data += strList[0]+':'+strList[1]+':'+strList[2]+':'+ strList[3]
					headData = 0
				else:
					data += '|'+strList[0]+':'+strList[1]+':'+strList[2]+':'+ strList[3]

				boxList.append(box)
			fileName, fileExtension = os.path.splitext(f)	
			
			exampleId = "exampleId="+fileName
			category = "category=" + re.sub("_[0-9]*","",fileName)
			print pathname
			url = "http://wireframe-prototyping.herokuapp.com/create1?taskType=1&"+exampleId+"&"+category+"&worker=machine&iteration=1&"+data
			print url
			tryCount = 0
			while tryCount < 5:
				response = urllib2.urlopen(url)
				successMessege = "\"success\": 1"
				if(successMessege in response.read()):
					break
				tryCount +=1
				print "fail "+ str(tryCount)
	return layoutList
if __name__ == "__main__":
	main()
