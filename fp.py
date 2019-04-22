#fp.py

from common.core import *
from common.gfxutil import *

from Audio import AudioController
from Display import *
from Player import Player
from SongData import SongData
from MIDIlistener import MIDIInput
from common.kivyparticle.engine import ParticleSystem

vel = 200
nowbar_height = 100
colors = [(1,0,0), (1,1,0), (0,1,0), (0,1,1), (0,0,1)]

class MainWidget(BaseWidget):
    def __init__(self):
        super(MainWidget, self).__init__()
        self.playing = False
        self.started = False
        self.section2_started = False
        self.streak = False

        self.data = SongData("annotations/BrownEyedGirlAnnotationFull.txt", "annotations/BrownEyedGirlRegions.txt")


        self.regions = self.data.get_regions()
        self.controller = AudioController("music/BrownEyedGirl", self.regions)



        self.color_mapping = {}
        chords = self.data.get_chords()
        for i in range(len(chords)):
            self.color_mapping[chords[i]] = colors[i]


        self.display = BeatMatchDisplay(self.data, self.color_mapping)
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
                self.controller.replay_region()
            if keycode[1] == "w":
                self.controller.next_region()
            if keycode[1] == "1":
                self.canvas.add(self.display)
                self.section2_started = True


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


            print(keycode[1])

    def on_key_up(self, keycode):
        pass

    def animate_streak(self):
        if not self.streak:
            self.ps1 = ParticleSystem('particle/particle.pex')
            self.ps1.emitter_x = 50.0
            self.ps1.emitter_y = 100.0
            self.ps1.start()
            self.add_widget(self.ps1)

            self.ps2 = ParticleSystem('particle/particle.pex')
            self.ps2.emitter_x = 550.0
            self.ps2.emitter_y = 100.0
            self.ps2.start()
            self.add_widget(self.ps2)

            self.streak = True


    def stop_streak(self):
        if self.streak:
            self.remove_widget(self.ps1)
            self.remove_widget(self.ps2)
            self.streak = False
            self.ps1.stop()
            self.ps2.stop()

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
                    if self.player.get_streak() == 5:
                        self.animate_streak()
                else:
                    self.stop_streak()
            else:
                self.label.text = "Final score is: %d\n" % self.player.get_score()
                self.label.text += "Accuracy is: %d %%\n" % self.player.get_accuracy()

                self.label.text += "Highest streak: %d\n" % self.player.get_max_streak()
                self.label.text += "Press \"R\" to restart"

run(MainWidget)
