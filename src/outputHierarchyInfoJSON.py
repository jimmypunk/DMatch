# python code
from mongokit import Connection
from heapq import *
from uicomp import UIComp
import json
from json import JSONEncoder
from boxAggregation import *
#input:aggregated box data, output:UICompTree
def buildUICompTree(boxList):
   count = 0
   compList = []
   for box in boxList:
      count += 1
      compList.append(UIComp(box))
   compList = sorted(compList, cmp=compareArea)
   consistList = []
   
   #calculate the overlapArea/unionArea between each two UI component
   uicompTreeDict = dict()
   root = UICompTree(UIComp([0,0,-1,-1]))
   for i in range(len(compList)):
      uicompTreeDict[i] = UICompTree(compList[i])
      parentFound = False
      for j in range(i-1,-1, -1):
         overlap = UIComp.overlapArea(compList[i], compList[j])
         coverRate = overlap/compList[i].area()
         if(coverRate > 0.9):
            #print i, "in", j
            uicompTreeDict[j].addChildTree(uicompTreeDict[i])
            parentFound = True
            break
      if(parentFound == False):
         root.addChildTree(uicompTreeDict[i])
   return root
   
def outputHierarchyInfoJSON(example_pattern, db):
   data = db.box.find({"exampleId":example_pattern})
   boxList = aggregateBoxes(data)
   root = buildUICompTree(boxList)
   return json.dumps(root,cls=MyEncoder, indent=3)
class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        return obj.toJSON()
def compareArea(uicomp1, uicomp2):
   if uicomp1.area() > uicomp2.area():
      return -1
   else:
      return 1
def printTree(tree,depth):
   print tree.uicomp,depth
   for childtree in tree.getchildren():
      printTree(childtree,depth+1)
class UICompTree(JSONEncoder):
   def __init__(self, uicomp, children=None):
     self.uicomp = uicomp
     if children is None:
         children = []
     self.children = children
   def addChildTree(self,childTree):
      self.children.append(childTree)
   def getchildren(self):
      return self.children
   def toJSON(self):
      if(len(self.children)!=0):
        return self.__dict__
      else:
        return {'uicomp':self.uicomp.toJSON()}
      
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
   fp = open("test.json","w")
   fp.write(outputHierarchyInfoJSON("friends_3",db[DB_NAME]))
   fp.close()
if __name__ == "__main__":
   main()
