
import sys
sys.path.append('..')
from common.core import *
from common.gfxutil import *

from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.graphics import PushMatrix, PopMatrix, Translate, Scale, Rotate

# class MainWidget(BaseWidget) :
#     def __init__(self):
#         super(MainWidget, self).__init__()
#
#
#         # chords=['G','C','D', [-1,2,4,2,3,2]]
#         # for index, chord in enumerate(chords):
#         # 	self.canvas.add(ChordDiagram(size=100, pos=(60+170*index, 300), chord=chord))
#
#         x = ChordDiagram(size=200, pos=(200, 300))
#         self.canvas.add(x)
#
#     def on_update(self):
#     	pass


class Mute(InstructionGroup):
	def __init__(self, size=20, pos=(100,100), color=Color(50/255,1,0)):
		super(Mute, self).__init__()
		x1 = pos[0] - size/2
		x2 = pos[0] + size/2
		y1 = pos[1] - size/2
		y2 = pos[1] + size/2
		self.x = InstructionGroup()
		self.x.add(color)
		line1 = Line(points=[x1,y2,x2,y1], width=size*.15, cap='square')
		line2 = Line(points=[x1,y1,x2,y2], width=size*.15, cap='square')
		self.x.add(line1)
		self.x.add(line2)
		self.add(self.x)


class ChordDiagram(InstructionGroup):
	Chords = {'G':[3,2,0,0,0,3],
			'A':[-1,0,2,2,2,0],
			'am':[-1,0,2,2,1,0],
			'bm':[-1,2,4,4,3,2],
			'C':[-1,3,2,0,1,0],
			'D':[-1,-1,0,2,3,2],
			'D7':[-1,-1,0,2,1,2],
			'em':[0,2,2,0,0,0],
			'Fmaj7':[-1,-1,3,2,1,0],
			'em7':[0,2,0,0,0,0]}

	def __init__(self, size=400, pos=(0,0), chord='G', color=Color(1,1,1)):
		super(ChordDiagram, self).__init__()


		self.add(PushMatrix())
		self.translate = Translate(*pos)
		self.add(self.translate)

		self.size = size
		self.x, self.y = (0,0)
		
		# fretboard
		x = self.x + self.size * .1
		y1 = self.y + self.size * .2
		y2 = self.y + self.size * .8

		fretboard = InstructionGroup()
		fretboard.add(Color(139/255,69/255,19/255))
		background = Rectangle(pos=(x, y1), size=(self.size * 1.4, self.size * .6))
		fretboard.add(background)
		self.add(fretboard)

		# frets
		last_x = x
		self.finger_placements = [x]
		scale_length = self.size * 6
		for i in range(4):
			fret = InstructionGroup()
			fret.add(Color(238/255, 238/255, 224/255))
			x = last_x + scale_length/17.817
			self.finger_placements.append((last_x + x)/2)
			last_x = x
			line = Line(points=[x, y1, x, y2], width=self.size/100, cap='round')
			fret.add(line)
			self.add(fret)
			scale_length = scale_length - scale_length/17.817

		# fret marker
		x_dot = self.finger_placements[3]
		dot = InstructionGroup()
		dot.add(Color(1,1,1))
		circle = CEllipse(cpos=(x_dot, self.y + self.size/2), csize=(self.size*.06, self.size*.06))
		dot.add(circle)
		self.add(dot)

		# strings
		self.string_heights = []
		for i in range(6):
			string = InstructionGroup()
			if i < 3:	# brass strings
				string.add(Color(181/255, 166/255, 66/255))
				width = size/100
			else:
				string.add(Color(180/255, 180/255, 180/255))
				width = size/200
			y = self.y + self.size * (.25 + .1 * i)
			self.string_heights.append(y)
			line = Line(points=[self.x + self.size * .1, y, self.x + self.size * 1.5, y], width=width, cap='round')
			string.add(line)
			self.add(string)

		# nut
		x = self.x + self.size * .1
		nut = InstructionGroup()
		nut.add(Color(238/255, 238/255, 224/255))
		line = Line(points=[x, y1, x, y2], width=self.size/50, cap='square')
		nut.add(line)
		self.add(nut)

		# chord fingering
		# if chord is hard-coded, get the frets from the dict.  else, use the passed-in list of frets
		try:
			indices = self.Chords[chord]
		except:
			indices = chord

		for index, fret in enumerate(indices):
			
			finger = InstructionGroup()
			finger.add(Color(*color))
			# TO DO: handle muted strings
			if fret == -1:
				x = Mute(size=self.size*.07, pos=(self.finger_placements[0], self.string_heights[index]),color= Color(*color))
				finger.add(x)
			else:
				dot = CEllipse(cpos=(self.finger_placements[fret], self.string_heights[index]), csize=(self.size*.1, self.size*.1))
				finger.add(dot)
			self.add(finger)

		# border
		border = InstructionGroup()
		self.color = color
		border.add(Color(*self.color))
		line = Line(points=[self.x, self.y, self.x, self.y + self.size, self.x + self.size * 1.6, self.y + self.size, self.x + self.size * 1.6, self.y],
							 width=self.size/100, joint='miter', close=True)
		border.add(line)
		self.add(border)

		self.add(PopMatrix())

	def set_pos(self, pos):
		self.translate.xy = pos

	def set_color(self, rgb):
		self.color.rgb = rgb


# run(MainWidget)