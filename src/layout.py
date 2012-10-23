from uicomp import UIComp
class Layout:
	def __init__(self, boxList, filename):
		self.filename = filename
		self.compList = []
		for idx in range(len(boxList)):
			self.compList.append(UIComp(boxList[idx]))
	def getComp(self, idx):
		return self.compList[idx];
	def getFilename(self):
		return self.filename
	def __len__(self):
		return len(self.compList)

