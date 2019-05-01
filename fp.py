#fp.py

from common.core import *
from common.gfxutil import *

from Audio import AudioController
from Display import *
from Player import Player
from SongData import SongData
from MIDIlistener import MIDIInput
from common.kivyparticle.engine import ParticleSystem
from ChordMatchDisplay import *
from ChordPlayer import *
from kivy.clock import Clock as kivyClock
from ProgressBar import ProgressBar
import sys
from kivy.uix.label import CoreLabel

vel = 200
nowbar_height = 100
colors = [(1,0,0), (1,1,0), (0,1,0), (0,1,1), (0,0,1)]

class MainWidget(BaseWidget):
    def __init__(self, song):
        super(MainWidget, self).__init__()
        self.playing = False
        self.started = False
        self.section2_started = False
        self.streak = False

        self.data = SongData("annotations/" + song + "AnnotationFull.txt", "annotations/" + song + "Regions.txt")

        self.regions = self.data.get_regions()
        self.controller = AudioController("music/"+ song, self.regions)

        self.color_mapping = {}
        self.chords = self.data.get_chords()
        for i in range(len(self.chords)):
            self.color_mapping[self.chords[i]] = colors[i]

        #display, player for chord learning part
        self.chordDisplay = ChordMatchDisplay(self.color_mapping)
        self.chordPlayer = ChordPlayer(self.chordDisplay, self.controller)
        self.canvas.add(self.chordDisplay)
        self.progress_bar = ProgressBar(self.data.get_sections(), 92, 108, self.color_mapping, self.controller)
        self.controller.set_start(int(self.data.get_sections()[92][0]))

        self.canvas.add(self.progress_bar)
        self.objects = []


        
        
        
        self.display = BeatMatchDisplay(self.data, self.color_mapping)
        self.player = Player(self.data, self.display, self.controller, self.color_mapping)

        self.create_label("Chord Learning", (50, 560), Color(1, 0, 0))

        #added chords to both self.player and self.chordPlayer
        for chord in self.chords:
            # self.player.add_chord(chord)
            self.chordPlayer.add_chord(chord)

        try:
            pass
            
            self.midiChord = MIDIInput(self.chordPlayer.on_strum)
        except:
            print("No MIDI inputs found! Please plug in MIDI device!")

        self.time = 0




    def create_label(self, text, pos, color = None):
        label = CoreLabel(text=text, font_size=20)
        label.refresh()
        text = label.texture
        if color:
            self.canvas.add(color)
        item = Rectangle(size=text.size, pos=pos, texture=text)
        self.canvas.add(item)
        self.objects.append(item)






    def init_section_2(self):
        self.display = BeatMatchDisplay(self.data, self.color_mapping)
        self.player = Player(self.data, self.display, self.controller, self.color_mapping)
        self.midi = MIDIInput(self.player.on_strum)
        for chord in self.chords:
            self.player.add_chord(chord)

    def on_touch_down(self, touch):
        if not self.section2_started:
            if touch:
                self.progress_bar.set_cursor(touch.pos)

    def on_key_down(self, keycode, modifiers):
        if self.section2_started:
            self.handle_down_section2(keycode, modifiers)
        else:
            self.handle_down_section1(keycode, modifiers)

    def handle_down_section1(self, keycode, modifiers):
        if keycode[1] == "p":
            self.controller.toggle()

        if keycode[1] == "1":
            # only do when section 2 hasnt begun yet
            if not self.section2_started:
                for obj in self.objects:
                    self.canvas.remove(obj)
                self.init_section_2()
                self.midiChord.off()
                self.canvas.add(self.display)
                #cleanup graphics
                self.chordDisplay.cleanup()
                self.progress_bar.cleanup()
                self.canvas.remove(self.chordDisplay)
                self.canvas.remove(self.progress_bar)
                self.controller.reset()
                self.player.reset()
                self.display.reset()
                self.playing = False
                self.started = False
                self.time = 0
                self.section2_started = True
                self.controller.set_start(0)
                self.controller.set_stop(None)

    def handle_down_section2(self, keycode, modifiers):
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
        if self.section2_started:
            self.update_section2()
        else:
            self.update_section1()

    def update_section2(self):
        frame = self.controller.on_update()

        self.time = frame / 44100
        self.display.on_update(self.time)
        self.player.on_update(self.time)
        self.midi.on_update()

        # if not self.player.get_done():
        #     self.label.text = "Press \"P\" to "
        #     if self.playing:
        #         self.label.text += "pause.\n"
        #     elif self.started:
        #         self.label.text += "unpause\n"
        #         self.label.text += "Press \"R\" to restart\n"

        #     else:
        #         self.label.text += "begin.\n"
        #     self.label.text += "score: %d\n" % self.player.get_score()
        #     if self.player.get_streak() >= 5:
        #         self.label.text += "                                                  Streak: %d   2x Bonus" % self.player.get_streak()
        #         if self.player.get_streak() == 5:
        #             self.animate_streak()
        #     else:
        #         self.stop_streak()
        # else:
        #     self.label.text = "Final score is: %d\n" % self.player.get_score()
        #     self.label.text += "Accuracy is: %d %%\n" % self.player.get_accuracy()

        #     self.label.text += "Highest streak: %d\n" % self.player.get_max_streak()
        #     self.label.text += "Press \"R\" to restart"

    def update_section1(self):
        # section 1 of the game updates
        frame = self.controller.on_update()
        self.midiChord.on_update()

        # self.label.text = '\n LEARNED CHORDS: ' + str(self.chordDisplay.chords)
        # if len(self.chordDisplay.chords) == 5:
        #     self.label.text += '\nDONE! Press 1 to continue to Chord Conqueror'
        self.time += kivyClock.frametime
        self.chordDisplay.on_update(self.time)
        self.chordPlayer.on_update(self.time)
        self.progress_bar.on_update(frame / 44100)
print (sys.argv)
try:
    run(MainWidget,sys.argv[1])
except:
    run(MainWidget, "BrownEyedGirl")
    
        # if self.midi2 is not None:
        #     self.midi2.on_update()

