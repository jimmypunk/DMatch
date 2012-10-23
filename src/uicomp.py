class UIComp:
	#def __init__(self,box,tag):
	def __init__(self,box):
		self.x = box[0]
		self.y = box[1]
		self.w = box[2]
		self.h = box[3]
	def center(self):
		return (self.x+self.w/2, self.y+self.h/2)
	def area(self):
		return self.w*self.h
	@staticmethod
	def unionAria(comp1, comp2):
		return comp1.area() + comp2.area() - overlapArea(comp1, comp2)
	@staticmethod
	def overlapArea(comp1, comp2):
		(cx1,cy1) = comp1.center()
		(cx2,cy2) = comp2.cnter()
		deltaX = abs(cx1 - cx2)
		deltaY = abs(cy1 - cy2)
		overlapW = (comp1.w + comp2.w)/2 - deltaX
		overlapH = (comp1.h + comp2.h)/2 - deltaY 
		if(overlapW > 0 and overlapH > 0):
			return overlapW * overlapH
		return 0
