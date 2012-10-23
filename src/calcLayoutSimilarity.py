from layout import Layout
from uicomp import UIComp
from operator import itemgetter
import sys, os
from stat import *
import math
from heapq import *
def main():
	# read from database?
	# read from file?
	layoutList = readData()
	print len(layoutList[0])
	print len(layoutList[1])
	rankList = rank(layoutList[0],layoutList)
	print 'baselayout:'+layoutList[0].getFilename()
	print '=====ranking======'
	for pair in rankList:
		print pair[1].getFilename()+" cost:"+str(pair[0])+'\n';
	print '================'
def rank(baselayout, layoutList):
	rankList = []
	for layout in layoutList:
		if(layout != baselayout):
			similarity = calcLayoutSimilarity(baselayout,layout);
			heappush(rankList,(similarity,layout));
	return [heappop(rankList) for i in range(len(rankList))]
def readData():
	layoutList = []
	for f in os.listdir('../data'):
		pathname = os.path.join('../data', f)
		mode = os.stat(pathname).st_mode
		if S_ISREG(mode):
			fp = open(pathname,'r')
			boxList = []
			for line in fp:
				strList = line.strip().split()
				box = [int(ele) for ele in strList]
				boxList.append(box)
			layoutList.append(Layout(boxList,f))
	return layoutList

def calcLayoutSimilarity(layout1, layout2):
	totalCost = 0;

	extraCost = 0;

	costEdgeList = []
	for idx1 in range(len(layout1)):
		for idx2 in range(len(layout2)):
			cost = costFunc(layout1.getComp(idx1), layout2.getComp(idx2))
			costEdgeList.append((idx1,idx2,cost))
	costEdgeList = sorted(costEdgeList, key = itemgetter(2))
	availableIdx1 = set(range(len(layout1)))
	availableIdx2 = set(range(len(layout2)))
	matchCount = 0;
	for pair in costEdgeList:
		if pair[0] in availableIdx1 and pair[1] in availableIdx2:
			#print "cost:"+str(pair[2])+ "idx:"+str(pair[0])+" "+str(pair[1])
			totalCost += pair[2]
			availableIdx1.remove(pair[0])
			availableIdx2.remove(pair[1])
			matchCount += 1
	for idx in availableIdx1:
		extraCost += math.sqrt(layout1.getComp(idx).area())
	for idx in availableIdx2:
		extraCost += math.sqrt(layout2.getComp(idx).area())
	print "matchCount:"+str(matchCount)
	return (totalCost + extraCost) / matchCount
def costFunc(comp1, comp2):
	w = 2
	x1,y1 = comp1.center()
	x2,y2 = comp2.center()
	cost = pow(x1 - x2, 2) + pow(y1 - y2, 2)
	cost += w *math.sqrt(abs(comp1.area() - comp2.area()))
	return cost

if __name__ == "__main__":
	main()
