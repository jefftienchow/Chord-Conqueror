import sys
sys.path.append('..')
from common.core import *
from common.gfxutil import *
from kivy.uix.label import CoreLabel


anim = KFAnim((0, 30), (1, 60), (2, 30), (3, 60))

# class MainWidget(BaseWidget):

# 	def __init__(self, whatever=None):
# 	    super(MainWidget, self).__init__()
	    
# 	    self.txt = TextLabel(text="Time for bed.", pos=(400, 300))
# 	    self.anim = AnimGroup()
# 	    self.anim.add(self.txt)
# 	    self.canvas.add(self.anim)
	    
	    

# 	def on_update(self):
# 		self.anim.on_update()

class TextLabel(InstructionGroup):

	def __init__(self, text, pos, font=40, align='left', color=Color(1,1,1), anim=None):
		super(TextLabel, self).__init__()
		self.t = 0
		self.size_func = anim
		label = CoreLabel(text=text, font_size=font)
		label.refresh()
		text = label.texture
		self.color = color
		self.add(self.color)
		if align == 'left':
			self.pos = pos
		else:
			self.pos = (pos[0] - text.size[0]/2, pos[1] - text.size[1]/2)
			
		self.item = Rectangle(size=text.size, pos=self.pos, texture=text)
		self.add(self.item)

	def on_update(self, dt):
		if self.size_func:
			size = self.size_func.eval(self.t)
			x, y = self.item.size
			self.item.size = (size*5, size)
			size_diff = (self.item.size[0] - x, self.item.size[1] - y)
			print(self.item.size)
			pos = self.item.pos
			self.item.pos = (pos[0] - size_diff[0]/2, pos[1] - size_diff[1]/2)
			self.t += dt
			return self.size_func.is_active(self.t)
		return True

# run(MainWidget, None)