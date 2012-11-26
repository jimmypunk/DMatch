# python code
from mongokit import Connection
from heapq import *
from uicomp import UIComp
#input: all the boxes, output: aggregated boxes
def aggregateBoxes(data, consistRate=0.7):
   count = 0 
   compList = []
   for d in data:
      count += 1
      box = [d["x"], d["y"], d["w"], d["h"]]
      compList.append(UIComp(box))
   consistList = []
   aggregateSetDict = dict()
   
   #calculate the overlapArea/unionArea between each two UI component
   for i in range(len(compList)):
      aggregateSetDict[i] = set([i])
      for j in range(i+1,len(compList)):
         overlap = UIComp.overlapArea(compList[i], compList[j])
         union = UIComp.unionArea(compList[i], compList[j])
         consistency = overlap/float(union)
         heappush(consistList,(consistency,i,j))

   #print len(consistList)
   for rate, cid1, cid2 in [heappop(consistList) for i in range(len(consistList))]:
      if(rate == 0): continue
      if(rate > consistRate):
         assert( cid1 in aggregateSetDict.keys() and cid2 in aggregateSetDict.keys())
         aggregateSetDict[cid1] = aggregateSetDict[cid2] = aggregateSetDict[cid1] | aggregateSetDict[cid2]
   aggregatedIdxSet = set()
   dataList = []
   for i in range(len(compList)):
      if i not in aggregatedIdxSet:
         aggregatedIdxSet = aggregatedIdxSet | aggregateSetDict[i]
         width = 0
         height = 0
         centerX = 0
         centerY = 0

         for idx in aggregateSetDict[i]:
            comp = compList[idx]
            cx, cy = comp.center()
            centerX += cx
            centerY += cy
            width += comp.w
            height += comp.h

         divisor = len(aggregateSetDict[i])
         width /= divisor
         height /= divisor
         centerX /= divisor
         centerY /= divisor
         dataList.append([centerX - width/2, centerY - height/2, width, height])
   return dataList
def getAggregatedResult(worker, example_pattern, iteration, db):
	data = db.box.find({"exampleId":example_pattern})
	dataList = aggregateBoxes(data)
	return '|'.join(["%s:%s:%s:%s"%(d[0],d[1],d[2],d[3]) for d in dataList])

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
	print getAggregatedResult("jimmy","friends_2","3",db[DB_NAME])
if __name__ == "__main__":
	main()
