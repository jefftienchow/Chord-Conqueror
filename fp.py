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
from ChordDetector import ChordDetector
from TextLabel import *
from MainMenu import MainMenuDisplay

vel = Window.height
nowbar_height = 100
colors = ["green", "red", "yellow", "blue", "purple", "light_blue"]

class MainWidget(BaseWidget):
    def __init__(self, song):
        super(MainWidget, self).__init__()
        print(song)
        self.playing = False
        self.started = False
        self.mainmenustarted = True
        self.section2_started = False
        self.streak = False
        # self.choose_song(song, (12,23))


        self.MainMenu = MainMenuDisplay(self.choose_song)
        self.canvas.add(self.MainMenu)
       

    def choose_song(self, song, start_end):
        self.data = SongData("annotations/" + song + "AnnotationFull.txt")

        self.controller = AudioController("music/" + song)

        self.color_mapping = {}
        self.chords = self.data.get_chords()
        for i in range(len(self.chords)):
            self.color_mapping[self.chords[i]] = colors[i]
        # print(self.color_mapping)
        self.detector = ChordDetector()

        #display, player for chord learning part


        self.start_section = start_end[0]
        self.end_section = start_end[1]
        print(self.start_section, self.end_section)
        #BrownEyedGirl 12 and 23
        #Riptide 92 108

    def draw_section_1(self):
        self.chordDisplay = ChordMatchDisplay(self.color_mapping,self.data, self.controller, self.start_section, self.end_section)
        self.chordPlayer = ChordPlayer(self.chordDisplay, self.controller, self.detector, self.data, self.color_mapping)

        self.canvas.add(self.chordDisplay)
        
        # self.progress_bar = ProgressBar(self.data.get_sections(), 92, 108, self.color_mapping, self.controller)
        self.controller.set_start(int(self.data.get_sections()[self.start_section][0]))
        self.controller.set_stop(int(self.data.get_sections()[self.end_section][0]))

        # self.canvas.add(self.progress_bar)
        self.objects = []

        self.title = TextLabel("Chord Learning", pos=(50, Window.height - 40), font=30)
        self.canvas.add(self.title)




        #added chords to both self.player and self.chordPlayer
        for chord in self.chords:
            # self.player.add_chord(chord)
            self.detector.add_chord(chord)
        try:
            
            self.midi = MIDIInput(self.detector.on_strum, self.chordDisplay.on_update_diagram)
        except:
            print("No MIDI inputs found! Please plug in MIDI device!")

        self.time = 0
        pass

    def modify_text(self, label, new_text):
        text_label = CoreLabel(text=new_text, font_size = 20)
        text_label.refresh()
        label.texture = text_label.texture

    def init_section_2(self):
        self.pause_menu = TextLabel("Press P to play/pause!", pos=(Window.width/2, Window.height/2), align='center', font=25)
        self.canvas.add(self.pause_menu)
        self.display = BeatMatchDisplay(self.data, self.color_mapping)
        self.player = Player(self.data, self.display, self.controller, self.color_mapping, self.detector, self)
        self.counting = False

    def on_touch_down(self, touch):
        if self.mainmenustarted:
            self.MainMenu.on_touch_down(touch)
        elif not self.section2_started:
            if touch:
                self.chordDisplay.on_touch_down(touch)

    def on_key_down(self, keycode, modifiers):
        if self.section2_started:
            self.handle_down_section2(keycode, modifiers)
        else:
            self.handle_down_section1(keycode, modifiers)

    def handle_down_section1(self, keycode, modifiers):
        if keycode[1] == "enter" and self.mainmenustarted:
            self.mainmenustarted = False
            self.MainMenu.cleanup()
            self.canvas.remove(self.MainMenu)
            self.draw_section_1()
        if keycode[1] == "p":
            self.controller.toggle()

        if keycode[1] == "1":
            # only do when section 2 hasnt begun yet
            if not self.section2_started:
                for obj in self.objects:
                    self.canvas.remove(obj)
                self.init_section_2()
                self.canvas.add(self.display)
                #cleanup graphics
                self.chordDisplay.cleanup()
                # self.progress_bar.cleanup()
                self.canvas.remove(self.chordDisplay)
                # self.canvas.remove(self.progress_bar)
                self.controller.reset()
                self.player.reset()
                self.display.reset()
                self.playing = False
                self.started = False
                self.time = 0
                self.section2_started = True
                self.controller.set_start(0)
                self.controller.set_stop(999999)
                self.canvas.remove(self.title)
        if keycode[1] == "spacebar" and not self.mainmenustarted:
            self.chordPlayer.new_section()
        if keycode[1] == "r" and not self.mainmenustarted:
            self.chordPlayer.replay_section()

    def handle_down_section2(self, keycode, modifiers):
        # play / pause toggle
        if keycode[1] == 'p':

            if not self.playing and self.counting:
                self.canvas.remove(self.counter)
                self.canvas.add(self.pause_menu)
                self.counting = False
            elif self.playing:
                self.canvas.add(self.pause_menu)
                self.controller.toggle()
                self.player.toggle()
                self.playing = False
            else:
                self.canvas.remove(self.pause_menu)
                self.counting = True
                self.count_time = 0
                self.counter = TextLabel("3", pos=(Window.width / 2, Window.height / 2), align='center', font=100,
                                         anim=KFAnim((0, 40), (1.5, 60), (1.7, 0)))
                self.count = 3
                self.canvas.add(self.counter)
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

    def count_down(self):
        self.add(self.counter)
        self.counting = True

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
        if self.mainmenustarted:
            return
        if self.section2_started:
            self.update_section2()
        else:
            self.update_section1()

    def update_section2(self):
        frame = self.controller.on_update()

        self.time = frame / 44100
        self.display.on_update(self.time)
        self.player.on_update(self.time)
        if self.counting:
            self.count_time += kivyClock.frametime
            if self.count_time < 2 and self.count_time >= 1 and self.count == 3:
                self.canvas.remove(self.counter)
                self.counter = TextLabel("2", pos=(Window.width / 2, Window.height / 2), align='center', font=100,
                                         anim=KFAnim((0, 40), (1.5, 60), (1.7, 0)))
                self.canvas.add(self.counter)
                self.count = 2
            elif self.count_time < 3 and self.count_time >= 2 and self.count == 2:
                self.canvas.remove(self.counter)
                self.counter = TextLabel("1", pos=(Window.width / 2, Window.height / 2), align='center', font=100,
                                         anim=KFAnim((0, 40), (1.5, 60), (1.7, 0)))
                self.canvas.add(self.counter)
                self.count = 1
            elif self.count_time >= 3 and self.count == 1:
                self.controller.toggle()
                self.player.toggle()
                self.counting = False
                self.canvas.remove(self.counter)
                self.playing = not self.playing

        self.midi.on_update()

    def updatemenu(self):
        self.MainMenu.on_update()
    def update_section1(self):
        # section 1 of the game updates
        frame = self.controller.on_update()
        self.midi.on_update()

        # self.label.text = '\n LEARNED CHORDS: ' + str(self.chordDisplay.chords)
        # if len(self.chordDisplay.chords) == 5:
        #     self.label.text += '\nDONE! Press 1 to continue to Chord Conqueror'
        self.time += kivyClock.frametime
        self.chordDisplay.on_update(frame)
        self.chordPlayer.on_update(self.time)

print (sys.argv)
run(MainWidget,1)

    
        # if self.midi2 is not None:
        #     self.midi2.on_update()