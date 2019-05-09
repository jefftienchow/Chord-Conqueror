#fp.py



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

vel = 200
nowbar_height = 100
color_mapping = {1:(1,0,0), 2:(1,1,0), 3: (0,1,0), 4: (0,1,1), 5:(0,0,1)}


#Expects inpput chords in the following format [(ROOT, quality, seventhBOOL, chordName]
class ChordMatchDisplay(InstructionGroup) :
    def __init__(self,color_mapping,data,controller):
        super(ChordMatchDisplay, self).__init__()
        self.diags = []

        self.color_mapping = color_mapping
        self.data = data
        self.controller = controller

        self.color = Color(1,1,1)
        self.add(self.color)

        self.chords = []
        self.diagrams = []
        self.diagramWidth = Window.width/(len(self.color_mapping)+1)
        self.diagramHeight = self.diagramWidth/1.6
        self.x = 0
        self.y =0

        self.progress_bar = ProgressBar(self.data.get_sections(), 12, 23, self.color_mapping, self.controller)
        self.add(self.progress_bar)
        self.chord_order = self.progress_bar.chord_order

        # Text Labels
        self.instrucions1 = TextLabel("Each colored section in the bar above corresponds to a different chord in the song.  Press P to play/pause!", pos=(50, 475), font=15, color=Color(1,0,0))
        self.add(self.instrucions1)
        self.instrucions1 = TextLabel("Click anywhere on the bar to set the cursor.", pos=(50, 450), font=15, color=Color(1,0,0))
        self.add(self.instrucions1)

        self.move_on = TextLabel("When you are ready, press the space bar to guess the chords in the song!", pos=(50,400), font=15, color=Color(1,0,0))
        self.add(self.move_on)

        self.options = set()
        self.optiondiags = []
        self.allchords = ['G',
            'A',
            'am',
            'bm',
            'C',
            'D',
            'D7',
            'em',
            'Fmaj7',
            'em7']


    def show_options(self, chord, color=Color(1,1,1), color_name='WHITE'):
        self.options.add(chord)
        print(self.allchords)
        print("ALL CHORDS")

        while len(self.options)< 3:
            self.options.add(random.choice(self.allchords))




        # for i in range(2):
        #     choice = random.choice(self.allchords)
        #     print(choice)
        #     while choice not in self.options and choice != chord:
        #         choice = random.choice(self.allchords)
        #         print(choice)
        #     print("DIFFERENT FROM: " + chord )
        #     print(choice)
        #     self.options.append(choice)
        # random.shuffle(self.options)
        # print(self.options)

        #drawign section
        x = 50
        y = Window.height/2
        self.label = TextLabel("Which chord is the %s chord?  Strum the correct chord to move on." % color_name, pos=(x, y - 50), font=20, color=Color(*color))
        self.add(self.label)
        self.diags = []
        for option in self.options:
            diag = ChordDiagram(self.diagramHeight, (x,y), chord = option, color =color)
            x +=self.diagramWidth + self.diagramWidth/2
            self.add(diag)
            self.optiondiags.append(diag)
            self.diags.append(diag)

    def on_update_diagram(self, string, fret):
        print(string)
        print(fret)
        for diag in self.diags:
            diag.on_update(string,fret)


    def remove_options(self):
        self.options = set()
        for option in self.optiondiags:
            self.remove(option)
        self.optiondiags.clear()
    
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
        self.remove(self.color)
        self.progress_bar.cleanup()
        self.remove(self.progress_bar)
        for diag in self.diagrams:
            self.remove(diag)



    def on_touch_down(self, touch):
        self.progress_bar.set_cursor(touch.pos)





        

