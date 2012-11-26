
class UIComp:
	#def __init__(self,box,tag):
	def __init__(self,box,tag=None):
		self.x = box[0]
		self.y = box[1]
		self.w = box[2]
		self.h = box[3]
	def center(self):
		return (self.x+self.w/2, self.y+self.h/2)
	def area(self):
		return self.w*self.h
	@staticmethod
	def unionArea(comp1, comp2):
		return comp1.area() + comp2.area() - UIComp.overlapArea(comp1, comp2)
	@staticmethod
	def overlapArea(comp1, comp2):
		(cx1,cy1) = comp1.center()
		(cx2,cy2) = comp2.center()
		deltaX = abs(cx1 - cx2)
		deltaY = abs(cy1 - cy2)
		overlapW = (comp1.w + comp2.w)/2 - deltaX
		overlapH = (comp1.h + comp2.h)/2 - deltaY 
		if(overlapW > 0 and overlapH > 0):
			tlX = max(comp1.x, comp2.x)
			tlY = max(comp1.y, comp2.y)
			lrX = min(comp1.x + comp1.w, comp2.x + comp2.w)
			lrY = min(comp1.y + comp1.h, comp2.y + comp2.h)
			return abs(tlX-lrX) * abs(tlY-lrY)
			#return overlapW * overlapH
		return 0
	def toJSON(self):
		return self.__dict__ 
	def __repr__(self):
		return 'x:'+str(self.x) + " y:" + str(self.y) + " w:" + str(self.w) + " h:" + str(self.h)
