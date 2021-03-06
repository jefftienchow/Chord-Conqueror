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
from common.gfxutil import *

vel = 200
nowbar_height = 100
color_mapping = {1:(1,0,0), 2:(1,1,0), 3: (0,1,0), 4: (0,1,1), 5:(0,0,1)}


#Expects inpput chords in the following format [(ROOT, quality, seventhBOOL, chordName]
class ChordMatchDisplay(InstructionGroup) :
    def __init__(self,color_mapping,data,controller, start, end, key):
        super(ChordMatchDisplay, self).__init__()
        self.key = key
        self.diags = []
        self.label = None

        self.color_mapping = color_mapping
        self.data = data
        self.controller = controller
        self.start = start
        self.end = end

        


        self.chords = []
        self.diagrams = []
        self.diagramWidth = Window.width/(len(self.color_mapping)+1)
        self.diagramHeight = self.diagramWidth/1.6
        self.x = 70
        self.y =0

        self.progress_bar = ProgressBar(self.data.get_sections(), start, end, self.color_mapping, self.controller)
        self.add(self.progress_bar)
        self.chord_order = self.progress_bar.chord_order

        # Text Labels
        self.color = Color(1,1,1)
        self.add(self.color)
        self.instrucions1 = TextLabel("Each colored section in the bar above represents a different chord.  Press P to play/pause the song!", pos=(50, 475), font=15, color=Color(1,1,1))
        self.add(self.instrucions1)
        self.instructions2 = TextLabel("Press R to replay the current section!", pos=(50,450), font=15, color=Color(1,1,1))
        self.add(self.instructions2)
        self.instrucions1 = TextLabel("Click anywhere on the bar to set the cursor. This song is in %s." % self.key, pos=(50, 425), font=15, color=Color(1,1,1))
        self.add(self.instrucions1)

        self.move_on = TextLabel("When you are ready, press the space bar to guess the chords in the song!", pos=(50,375), font=15, color=Color(1,1,1))
        self.add(self.move_on)

        self.anim = AnimGroup()
        self.add(self.anim)

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


    def show_options(self, chord, color):
        if self.move_on:
            self.remove(self.move_on)
            self.move_on = None
        self.options.add(chord)
        # print(self.allchords)
        # print("ALL CHORDS")

        while len(self.options)< 3:
            self.options.add(random.choice(self.allchords))

        x = 70
        y = Window.height/2

        if self.label is None:
            self.label = TextLabel("Which chord is the %s chord?  Strum the correct chord to move on." % color, pos=(x, y - 50), font=20, color=Color(*to_rgb[color]))
            self.add(self.label)
        else:
            self.label.update_text("Which chord is the %s chord?  Strum the correct chord to move on." % color, to_rgb[color])
        self.diags = []
        # self.diag_labels = []
        for option in self.options:
            # label = TextLabel(option, pos=(x,y - 50), font= 20)
            # self.add(self.label)
            # self.diag_labels.append(label)

            diag = ChordDiagram(self.diagramHeight, (x,y), chord = option, color = self.color_mapping[chord])
            x +=self.diagramWidth + self.diagramWidth/2
            self.add(diag)
            self.optiondiags.append(diag)
            self.diags.append(diag)

    def on_update_diagram(self, string, fret):
        # print(string)
        # print(fret)
        for diag in self.diags:
            diag.on_update(string,fret)


    def remove_options(self):
        self.options = set()
        for option in self.optiondiags:
            self.remove(option)
        self.optiondiags.clear()
    
    def draw_chord(self, chord):
        if self.x  >= Window.width - self.diagramHeight:
            self.y += self.diagramHeight + 20
            self.x = 70
        diag = ChordDiagram(self.diagramHeight, (self.x,self.y), chord = chord, color = self.color_mapping[chord] )
        self.add(diag)
        self.diagrams.append(diag)
        self.x += self.diagramWidth + self.diagramWidth/(len(self.color_mapping)-1)


    #what happens when a note is correct, called by ChordPlayer
    def correct(self,chord,right):
        self.change_bg((0,1,0))
        self.anim.add(TextLabel("Correct!", pos=(400, 200), font=100, align='center', color=Color(0,1,0), anim=KFAnim((0, 40), (1, 60), (1.2, 0))))
        
        if chord not in self.chords and right:
            self.draw_chord(chord)
            self.chords.append(chord)
    #What happens when a chord is incorrect, called by Chord Player
    def wrong(self):
        self.change_bg((1,0,0))
        self.anim.add(TextLabel("Incorrect, try again!", pos=(400, 200), font=100, align='center', color=Color(1,0,0), anim=KFAnim((0, 40), (1.5, 60), (1.7, 0))))


    #changes background to current color
    def change_bg(self, color):
        self.color.s = 1
        self.color.rgb = color

    def on_update(self, frame):
        #self.color.s -= .01
        self.progress_bar.on_update(frame / 44100)
        self.anim.on_update()
    #erases everything from its canvas

    def cleanup(self):
        self.remove(self.color)
        self.progress_bar.cleanup()
        self.remove(self.progress_bar)
        for diag in self.diagrams:
            self.remove(diag)



    def on_touch_down(self, touch):
        self.progress_bar.set_cursor(touch.pos)





        

