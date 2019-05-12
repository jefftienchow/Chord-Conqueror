


##### NEW UDIO CONTROLLER, NEW PLAYER, AND NEW DISPLAY
import random
from common.core import *
from common.gfxutil import *

from Audio import AudioController
from Display import *
from Player import Player
from SongData import SongData
from ChordDiagram import ChordDiagram
from ProgressBar import ProgressBar
from TextLabel import TextLabel
from kivy.uix.label import CoreLabel
from common.gfxutil import *

songs = ["BrownEyedGirl", "Riptide", "WithoutMe"]
start_end = [(12, 23), (92,108), (12,23)]
keys = ["G Major", "C Major", "e minor"]
class MainMenuDisplay(InstructionGroup):
    
    def __init__(self,choose_song):
        super(MainMenuDisplay, self).__init__()
        self.label = TextLabel(text = "Click on a song to select it, and press ENTER to confirm", pos = (0,0), font=Window.height/30)
        self.add(self.label)
        self.buttons = []
        self.choose_song = choose_song
        x = Window.width - 1/6*Window.width
        y = 200
        i = 0
        label = CoreLabel(text="CHOOSE A SONG", font_size = Window.height/10)
        label.refresh()
        text = label.texture

        title = Rectangle(texture = text, pos =( Window.width/2-text.size[0]/2, Window.height*3/4), size = text.size)
        self.add(title)
        for song in songs:
            button = SongButtons(y = y, song = song, start_end = start_end[i], key=keys[i])
            self.buttons.append(button)
            self.add(button)
            i+=1
            y += Window.height/7


    def on_touch_down(self, touch):
    	for button in self.buttons:
    		inside, song, start_end, key = button.check_inside(touch.pos[0], touch.pos[1])
    		if inside:
    			self.choose_song(song, start_end, key)
    def cleanup(self):
    	self.remove(self.label)
    	for button in self.buttons:
    		self.remove(button)


class SongButtons(InstructionGroup):
	def __init__(self, y, song, start_end, key):
		super(SongButtons, self).__init__()
		self.start_end = start_end
		self.song = song
		self.key = key
		self.color = Color(*(1,1,1))
		self.add(self.color)


		#added lable for texturing the buttons
		label = CoreLabel(text=song, font_size = Window.height/20)
		label.refresh()
		text = label.texture
		self.size =text.size
		x =  Window.width/2-text.size[0]/2
		self.pos =  (x,y)
		self.button = Rectangle(texture = text, pos = self.pos, size = text.size)
		self.add(self.button)


	def click(self):
		self.color.a = .2
		# print("IM CLICKED",self.song)
		return True, self.song, self.start_end, self.key

	def unclick(self):
		self.color.a = 1
		# print("IM UNCLICKED", self.song)
		return False, None, self.start_end, self.key

	def check_inside(self,x,y):
		if x >=self.pos[0] and x <=self.pos[0] + self.size[0]:
			if y >=self.pos[1] and y <=self.pos[1] + self.size[1]:
				return self.click()
		return self.unclick()

