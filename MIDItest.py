from common.core import *
from common.gfxutil import *

from Audio import AudioController
from Display import *
from Player import Player
from SongData import SongData


from MIDIlistener import MIDIInput
vel = 200
nowbar_height = 100
color_mapping = {1:(1,0,0), 2:(1,1,0), 3: (0,1,0), 4: (0,1,1), 5:(0,0,1)}

class MainWidget(BaseWidget) :
    def __init__(self):
        super(MainWidget, self).__init__()
        #creates MIDI listener object
        self.MIDI = MIDIInput()

        self.label = topleft_label()
        self.add_widget(self.label)

    def on_key_down(self, keycode, modifiers):
        pass
        


    def on_key_up(self, keycode):
        pass
        
    def on_update(self) :
        self.label.text = str(self.MIDI.last_note) + '\n'
        self.label.text += str(self.MIDI.current_notes)
        self.MIDI.on_update()

run(MainWidget)