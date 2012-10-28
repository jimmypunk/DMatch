# python code
from mongokit import Connection
from heapq import *
from uicomp import UIComp

def aggregateBoxes(worker, example_pattern, iteration, db):
	data = db.box.find({"exampleId":example_pattern})

	count = 0 
	compList = []
	for d in data:
		count += 1
		box = [d["x"], d["y"], d["w"], d["h"]]
		compList.append(UIComp(box))
		#print "%d x:%d y:%d w:%d h:%d" % (count ,d["x"], d["y"], d["w"], d["h"]) 
	consistList = []
	
	aggregateSet = dict()
	for i in range(len(compList)):
		aggregateSet[i] = set([i])
		for j in range(i+1,len(compList)):
			overlap = UIComp.overlapArea(compList[i], compList[j])
			union = UIComp.unionArea(compList[i], compList[j])
			consistency = overlap/float(union)
			heappush(consistList,(consistency,i,j))

	consistRate = 0.7
	#print len(consistList)
	for rate, cid1, cid2 in [heappop(consistList) for i in range(len(consistList))]:
		if(rate == 0): continue
		print str(rate ),cid1,compList[cid1], cid2, compList[cid2]
		overlap = UIComp.overlapArea(compList[cid1], compList[cid2])
		coverRate1 = overlap/compList[cid1].area()
		coverRate2 = overlap/compList[cid2].area()
		maxcoverRate = max(coverRate1, coverRate2)
		if(rate < 0.7 and maxcoverRate > 0.9):
			if(maxcoverRate == coverRate1):
				print cid1, "in", cid2
			else:
				print cid2, "in", cid1
		if(rate > consistRate):
			assert( cid1 in aggregateSet.keys() and cid2 in aggregateSet.keys())
			aggregateSet[cid1] = aggregateSet[cid2] = aggregateSet[cid1] | aggregateSet[cid2]
	duplicateSet = set()
	dataList = []
	for i in range(len(compList)):
		if i not in duplicateSet:
			duplicateSet = duplicateSet | aggregateSet[i]
			width = 0
			height = 0
			centerX = 0
			centerY = 0

			for idx in aggregateSet[i]:
				comp = compList[idx]
				cx, cy = comp.center()
				centerX += cx
				centerY += cy
				width += comp.w
				height += comp.h

			divisor = len(aggregateSet[i])
			width /= divisor
			height /= divisor
			centerX /= divisor
			centerY /= divisor
			dataList.append("%s:%s:%s:%s" % (centerX - width/2, centerY - height/2, width, height))
	return '|'.join(dataList)
def main():
	# local configuration
	"""
	MONGODB_HOST = 'localhost'
	MONGODB_PORT = 27017
	DB_NAME = "dmatch"
	"""

	# remote configuration
	MONGODB_HOST = "ds039717.mongolab.com"
	MONGODB_PORT = 39717
	DB_NAME = "heroku_app8550378"
	db = Connection(MONGODB_HOST, MONGODB_PORT)

	db.heroku_app8550378.authenticate("heroku_app8550378", "2v3kconmt7hbc7pdf32gj3po3s")
	print aggregateBoxes("jimmy","friends_2","3",db[DB_NAME])
if __name__ == "__main__":
	main()
