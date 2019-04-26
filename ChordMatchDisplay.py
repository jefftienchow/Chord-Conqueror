#fp.py



##### NEW UDIO CONTROLLER, NEW PLAYER, AND NEW DISPLAY

from common.core import *
from common.gfxutil import *

from Audio import AudioController
from Display import *
from Player import Player
from SongData import SongData
from ChordDiagram import ChordDiagram

vel = 200
nowbar_height = 100
color_mapping = {1:(1,0,0), 2:(1,1,0), 3: (0,1,0), 4: (0,1,1), 5:(0,0,1)}


#Expects inpput chords in the following format [(ROOT, quality, seventhBOOL, chordName]
class ChordMatchDisplay(InstructionGroup) :
    def __init__(self):
        super(ChordMatchDisplay, self).__init__()


        self.color = Color(1,1,1)
        self.add(self.color)
        self.background = Rectangle(pos = (Window.width - 300,Window.height - 300), size = (250, 250))
        self.add(self.background)

        self.chords = []
        self.diagrams = []
        
        self.x = -390
        self.y =0



    
    def draw_chord(self, chord):
        self.x += 400
        if self.x >= Window.width:
            self.y += 250
            self.x = 10
        diag = ChordDiagram(200, (self.x,self.y), chord)
        self.add(diag)
        self.diagrams.append(diag)


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

    def on_update(self, time):
        self.color.s -= .01 
    #erases everything from its canvas
    def cleanup(self):
        self.remove(self.background)
        self.remove(self.color)
        for diag in self.diagrams:
            self.remove(diag)





        

