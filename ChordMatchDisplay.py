#fp.py



##### NEW UDIO CONTROLLER, NEW PLAYER, AND NEW DISPLAY

from common.core import *
from common.gfxutil import *

from Audio import AudioController
from Display import *
from Player import Player
from SongData import SongData
from ChordDiagram import ChordDiagram
from ProgressBar import ProgressBar

vel = 200
nowbar_height = 100
color_mapping = {1:(1,0,0), 2:(1,1,0), 3: (0,1,0), 4: (0,1,1), 5:(0,0,1)}


#Expects inpput chords in the following format [(ROOT, quality, seventhBOOL, chordName]
class ChordMatchDisplay(InstructionGroup) :
    def __init__(self,color_mapping,data,controller):
        super(ChordMatchDisplay, self).__init__()
        self.color_mapping = color_mapping
        self.data = data
        self.controller = controller

        self.color = Color(1,1,1)
        self.add(self.color)
        self.background = Rectangle(pos = (Window.width - 300,Window.height - 300), size = (250, 250))
        self.add(self.background)

        self.chords = []
        self.diagrams = []
        self.diagramWidth = Window.width/(len(self.color_mapping)+1)
        self.diagramHeight = self.diagramWidth/1.6
        self.x = 0
        self.y =0

        self.progress_bar = ProgressBar(self.data.get_sections(), 92, 108, self.color_mapping, self.controller)
        self.add(self.progress_bar)
        self.chord_order = self.progress_bar.chord_order

        self.options = []


    def show_options(self, chord):
        pass

    def remove_options(self):
        pass
    
    def draw_chord(self, chord):
        if self.x  >= Window.width:
            self.y += self.diagramHeight + 20
            self.x = 0
        diag = ChordDiagram(self.diagramHeight, (self.x,self.y), chord = chord, color = self.color_mapping[chord] )
        self.add(diag)
        self.diagrams.append(diag)
        self.x += self.diagramWidth + self.diagramWidth/(len(self.color_mapping)-1)


    #what happens when a note is correct, called by ChordPlayer
    def correct(self,chord,right):
        self.change_bg((0,1,0))
        if chord not in self.chords and right:
            self.draw_chord(chord)
            self.chords.append(chord)
    #What happens when a chord is incorrect, called by Chord Player
    def wrong(self):
        self.change_bg((1,0,0))


    #changes background to current color
    def change_bg(self, color):
        self.color.s = 1
        self.color.rgb = color

    def on_update(self, frame):
        self.color.s -= .01 
        self.progress_bar.on_update(frame / 44100)
    #erases everything from its canvas
    def cleanup(self):
        self.remove(self.background)
        self.remove(self.color)
        self.progress_bar.cleanup()
        self.remove(self.progress_bar)
        for diag in self.diagrams:
            self.remove(diag)



    def on_touch_down(self, touch):
        self.progress_bar.set_cursor(touch.pos)





        

