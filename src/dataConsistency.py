# python code
from mongokit import Connection
from heapq import *
from uicomp import UIComp
MONGODB_HOST = "ds039717.mongolab.com"
MONGODB_PORT = 39717
DB_NAME = "heroku_app8550378"

# make a connection
db = Connection(MONGODB_HOST, MONGODB_PORT)
db.heroku_app8550378.authenticate("heroku_app8550378", "2v3kconmt7hbc7pdf32gj3po3s")

example = "logins_2"
data = db[DB_NAME].box.find({"exampleId":example})

#data = db[DB_NAME].box.find({"worker":"machine"})
count = 0 
compList = []
for d in data:
	count += 1
	box = [d["x"], d["y"], d["w"], d["h"]]
	compList.append(UIComp(box))
#	print "%d x:%d y:%d w:%d h:%d" % (count ,d["x"], d["y"], d["w"], d["h"]) 
consistList = []
for i in range(len(compList)):
	for j in range(i,len(compList)):
		overlap = UIComp.overlapArea(compList[i], compList[j])
		union = UIComp.unionArea(compList[i], compList[j])
		consistency = overlap/float(union)
		print compList[i], compList[j], consistency
		heappush(consistList,(consistency,i,j))

for consistPair in [heappop(consistList) for i in range(len(consistList))].reverse():
	print str(consistPair[0]) +  " ", compList[consistPair[1]], compList[consistPair[2]]
