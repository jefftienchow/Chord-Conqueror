#fp.py

from common.core import *
from common.gfxutil import *

from Audio import AudioController
from Display import *
from Player import Player
from SongData import SongData
from MIDIlistener import MIDIInput

vel = 200
nowbar_height = 100
colors = [(1,0,0), (1,1,0), (0,1,0), (0,1,1), (0,0,1)]

class MainWidget(BaseWidget):
    def __init__(self):
        super(MainWidget, self).__init__()
        self.playing = False
        self.started = False
        self.section2_started = False

        self.data = SongData("annotations/BrownEyedGirlAnnotationFull.txt", "annotations/BrownEyedGirlRegions.txt")


        self.regions = self.data.get_regions()
        self.controller = AudioController("music/BrownEyedGirl", self.regions)



        self.color_mapping = {}
        chords = self.data.get_chords()
        for i in range(len(chords)):
            self.color_mapping[chords[i]] = colors[i]


        self.display = BeatMatchDisplay(self.data, self.color_mapping)
        #current player is chordPlayer
        self.player = Player(self.data, self.display, self.controller, self.color_mapping)



        for chord in chords:
            self.player.add_chord(chord)


        try:
            self.midi = MIDIInput(self.player.on_strum)
        except:
            print("No MIDI inputs found! Please plug in MIDI device!")

        self.time = 0

        self.label = topleft_label()
        self.add_widget(self.label)

    def on_key_down(self, keycode, modifiers):
        if not self.section2_started:
            if keycode[1] == "q":
                #TODO change to self.player commands
                self.controller.replay_region()
                print('??')
                #TODO change to self.player commands
            if keycode[1] == "w":
                self.controller.next_region()
            if keycode[1] == "1":
                self.canvas.add(self.display)
                self.section2_started = True
                #change player to main game player
                self.player = Player(self.data, self.display, self.controller, self.color_mapping)
        print(keycode[1])

        if self.section2_started:
            # play / pause toggle
            if keycode[1] == 'p':
                self.controller.toggle()
                self.playing = not self.playing
                self.started = True

            if keycode[1] == 'r':
                if not self.playing or self.player.get_done():
                    self.controller.reset()
                    self.player.reset()
                    self.display.reset()
                    self.playing = False
                    self.started = False

            if keycode[1] == 'm':
                self.controller.set_mute(True)

            

    def on_key_up(self, keycode):
        pass

    def on_update(self) :
        frame = self.controller.on_update()

        if self.section2_started:
            self.time = frame / 44100
            self.display.on_update(self.time)
            self.player.on_update(self.time)
            self.midi.on_update()

            if not self.player.get_done():
                self.label.text = "Press \"P\" to "
                if self.playing:
                    self.label.text += "pause.\n"
                elif self.started:
                    self.label.text += "unpause\n"
                    self.label.text += "Press \"R\" to restart\n"

                else:
                    self.label.text += "begin.\n"
                self.label.text += "score: %d\n" % self.player.get_score()
                if self.player.get_streak() >= 5:
                    self.label.text += "                                                  Streak: %d   2x Bonus" % self.player.get_streak()
            else:
                self.label.text = "Final score is: %d\n" % self.player.get_score()
                self.label.text += "Accuracy is: %d %%\n" % self.player.get_accuracy()

                self.label.text += "Highest streak: %d\n" % self.player.get_max_streak()
                self.label.text += "Press \"R\" to restart"

run(MainWidget)
