#fp.py

from common.core import *
from common.audio import *
from common.mixer import *
from common.wavegen import *
from common.wavesrc import *
from common.gfxutil import *

from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.graphics import PushMatrix, PopMatrix, Translate, Scale, Rotate
from kivy.core.image import Image
from kivy.clock import Clock as kivyClock
from random import randint

import random
import numpy as np
import bisect

vel = 200
nowbar_height = 100
color_mapping = {1:(1,0,0), 2:(1,1,0), 3: (0,1,0), 4: (0,1,1), 5:(0,0,1)}

class MainWidget(BaseWidget) :
    def __init__(self):
        super(MainWidget, self).__init__()
        self.playing = False
        self.started = False

        self.data = SongData("annotations/annotation.txt", "annotations/barlines_beginning.txt")

        self.controller = AudioController("music/KillerQueen",self.data)

        self.display = BeatMatchDisplay(self.data)

        self.canvas.add(self.display)

        self.player = Player(self.data, self.display, self.controller)
        self.time = 0

        self.label = topleft_label()
        self.add_widget(self.label)

    def on_key_down(self, keycode, modifiers):
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

        # button down
        button_idx = lookup(keycode[1], '12345', (0,1,2,3,4))
        if button_idx is not None:
            self.player.on_button_down(button_idx)

        print(keycode[1])


    def on_key_up(self, keycode):
        # button up
        button_idx = lookup(keycode[1], '12345', (0,1,2,3,4))
        if button_idx is not None:
            self.player.on_button_up(button_idx)

    def on_update(self) :
        frame = self.controller.on_update()
        self.time = frame / 44100
        self.display.on_update(self.time)
        self.player.on_update(self.time)

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

# creates the Audio driver
# creates a song and loads it with solo and bg audio tracks
# creates snippets for audio sound fx
class AudioController(object):
    def __init__(self, song_name, data):
        super(AudioController, self).__init__()
        self.audio = Audio(2)
        self.mixer = Mixer()
        self.solo = WaveGenerator(WaveFile(song_name + "_solo.wav"), False)
        self.bg = WaveGenerator(WaveFile(song_name + "_bg.wav"),False)
        self.mixer.add(self.solo)
        self.mixer.add(self.bg)

        self.audio.set_generator(self.mixer)

    # start / stop the song
    def toggle(self):
        self.solo.play_toggle()
        self.bg.play_toggle()

    def reset(self):
        self.solo.reset()
        self.bg.reset()

    # mute / unmute the solo track
    def set_mute(self, mute):
        self.solo.set_mute(mute)

    # play a sound-fx (miss sound)
    def play_sfx(self):
        gen = WaveGenerator(WaveFile("music/Miss_sound.wav"))
        self.mixer.add(gen)
        gen.play_toggle()


    # needed to update audio
    def on_update(self):
        self.audio.on_update()
        return self.solo.get_frame()

# holds data for gems and barlines.
class SongData(object):
    def __init__(self, gem_annotation, bar_annotation):
        super(SongData, self).__init__()
        self.gems = self.read_gems(gem_annotation)
        self.bars = self.read_bars(bar_annotation)

    def get_gems(self):
        return self.gems

    def get_bars(self):
        return self.bars

    def lines_from_file(self,filepath):
        with open(filepath) as file:
            return file.readlines()

    def tokens_from_line(self,line):
        new_str = line.strip()
        new_str = new_str.strip("\n")
        return new_str.split("\t")

    # read the gems and song data. You may want to add a secondary filepath
    # argument if your barline data is stored in a different txt file.
    def read_gems(self, filename):
        gems = []
        lines = self.lines_from_file(filename)
        for line in lines:
            tokens = self.tokens_from_line(line)
            gems.append((float(tokens[0]), int(tokens[1])))
        return gems

    def read_bars(self,filename):
        bars = []
        lines = self.lines_from_file(filename)
        for line in lines:
            tokens = self.tokens_from_line(line)
            bars.append(float(tokens[0]))
        return bars

class Note(InstructionGroup):
    def __init__(self, pos, color, angle):
        super(Note, self).__init__()
        self.pos = np.array(pos, dtype=np.float)

        self.pos[0] += 25
        self.pos[1] += 10

        self.color = Color(*color)
        self.add(self.color)
        # adds a translation and rotation and another translation to the note
        self.add(PushMatrix())
        self.translate = Translate(*self.pos)
        self.add(self.translate)

        self._angle = Rotate(angle = angle)
        self.add(self._angle)

        self.translate2 = Translate(0, 40)
        self.add(self.translate2)

        self.note = Rectangle(texture=Image("pictures/note.png").texture, pos = (-5,-7), size = (10,15))

        self.add(self.note)

        self.add(PopMatrix())

        self.vel = np.array((0,20), dtype= np.float)

        self.color.a = 1

    def on_update(self, dt):

        self.color.a -= dt
        # apply translation
        self.translate2.xy = (self.translate2.x, self.translate2.y + self.vel[1] * dt)

        # returns true if note is visible and on the screen
        return self.color.a > 0

# display for a single gem at a position with a color (if desired)
class BarDisplay(InstructionGroup):
    def __init__(self, data):
        super(BarDisplay, self).__init__()
        self.time = 0
        self.time_loc = data
        self.color = Color(1,1,1, .7)
        self.add(self.color)

        self.ypos = nowbar_height + (self.time_loc - self.time) * vel

        self.bar = Rectangle(pos=(0,self.ypos), size = (800, 2))
        self.add(self.bar)

        self.vel = vel
        self.notes = []

    # useful if gem is to animate
    def on_update(self, time):
        self.time = time

        # bar comes down and hits nowbar height at its corresponding time
        self.ypos = nowbar_height + (self.time_loc - time) * vel

        self.bar.pos = (0, self.ypos)

# display for a single gem at a position with a color (if desired)
class GemDisplay(InstructionGroup):
    def __init__(self, data):
        super(GemDisplay, self).__init__()
        self.time = 0
        self.type = data[1]
        self.time_loc = data[0]
        self.color_data = color_mapping[self.type]
        self.color = Color(*color_mapping[self.type])
        self.color.a = .7
        self.add(self.color)

        self.xpos = self.type * 100
        self.ypos = nowbar_height + (self.time_loc - self.time) * vel
        self.gem = Rectangle(pos=(self.xpos,self.ypos), size = (50, 10))
        self.add(self.gem)

        self.vel = vel
        self.notes = []

    # change to display this gem being hit
    def on_hit(self):
        self.color.a = 0

        # creates the hit effect where notes animations are added
        for i in range(6):
            note = Note((self.xpos, nowbar_height), self.color_data, i * 60)
            self.add(note)
            self.notes.append(note)

    # change to display a passed gem
    def on_pass(self):
        self.color.a = .3

    def reset(self):
        self.color.a = .7
        self.notes = []

    # useful if gem is to animate
    def on_update(self, time):
        dt = abs(time - self.time)
        self.time = time
        # gem comes down and hits nowbar height at its corresponding time
        self.ypos = nowbar_height + (self.time_loc - time) * vel

        self.gem.pos = (self.xpos, self.ypos)

        for note in self.notes:
            note.on_update(dt)


# Displays one button on the nowbar
class ButtonDisplay(InstructionGroup):
    def __init__(self, pos, color):
        super(ButtonDisplay, self).__init__()
        self.color = color
        self.pos = pos
        self.add(color)
        self.button = Rectangle(pos=pos, size=(50, 20))
        self.add(self.button)

    # displays when button is down (and if it hit a gem)
    def on_down(self, hit):
        self.color.a = 1


    # back to normal state
    def on_up(self):
        self.color.a = .5


# Displays and controls all game elements: Nowbar, Buttons, BarLines, Gems.
class BeatMatchDisplay(InstructionGroup):
    def __init__(self, data):
        super(BeatMatchDisplay, self).__init__()
        self.gem_data = data.get_gems()
        self.bar_data = data.get_bars()

        self.time = 0

        # creates gems
        self.gems = []
        for gem_info in self.gem_data:
            gem = GemDisplay(gem_info)
            self.gems.append(gem)
            self.add(gem)

        # creates bars
        self.bars = []
        for bar_info in self.bar_data:
            bar = BarDisplay(bar_info)
            self.bars.append(bar)
            self.add(bar)

        # creates the nowbar
        self.add(Color(1,1,1,.5))
        self.nowbar = Rectangle(pos = (0,nowbar_height), size = (800, 20))
        self.add(self.nowbar)

        # creates buttons
        self.buttons = []
        for i in range(1,6):
            color = Color(*color_mapping[i])
            color.a = .5
            pos = (100*i, nowbar_height)

            button = ButtonDisplay(pos,color)

            self.add(button)
            self.buttons.append(button)

    def reset(self):
        for gem in self.gems:
            gem.reset()

    # called by Player. Causes the right thing to happen
    def gem_hit(self, gem_idx):
        self.gems[gem_idx].on_hit()

    # called by Player. Causes the right thing to happen
    def gem_pass(self, gem_idx):
        self.gems[gem_idx].on_pass()

    # called by Player. Causes the right thing to happen
    def on_button_down(self, lane, hit):
        self.buttons[lane].on_down(hit)

    # called by Player. Causes the right thing to happen
    def on_button_up(self, lane):
        self.buttons[lane].on_up()

    # call every frame to make gems and barlines flow down the screen
    def on_update(self, time):
        for gem in self.gems:
            gem.on_update(time)
        for bar in self.bars:
            bar.on_update(time)



# Handles game logic and keeps score.
# Controls the display and the audio
class Player(object):
    def __init__(self, data, display, audio_ctrl):
        super(Player, self).__init__()
        self.gem_data = data.get_gems()

        self.display = display
        self.controller = audio_ctrl

        self.idx = 0
        self.interval = .1
        self.score = 0
        self.streak = 0
        self.done = False
        self.max_streak = 0
        self.hits = 0

    def get_score(self):
        return self.score

    def get_streak(self):
        return self.streak

    def get_done(self):
        return self.idx == len(self.gem_data)

    def reset(self):
        self.done = False
        self.streak = 0
        self.score = 0
        self.idx = 0

    def get_max_streak(self):
        return self.max_streak

    def get_accuracy(self):
        return self.hits * 100 /len(self.gem_data)

    # called by MainWidget
    def on_button_down(self, lane):
        self.display.on_button_down(lane, None)
        if self.idx < len(self.gem_data):
            if self.time >= self.gem_data[self.idx][0] - self.interval and self.time <= self.gem_data[self.idx][0] + self.interval:
                # a correct note is hit
                if lane + 1 == self.gem_data[self.idx][1]:
                    self.display.gem_hit(self.idx)
                    self.controller.set_mute(False)
                    self.idx += 1
                    self.score += 100
                    self.streak += 1
                    self.hits += 1
                    self.max_streak = max(self.streak, self.max_streak)
                    if self.streak >= 5:
                        self.score += 100

                # a lane miss
                else:
                    self.display.gem_pass(self.idx)
                    self.controller.play_sfx()
                    self.controller.set_mute(True)
                    self.deduct()

            # a temporal miss
            elif self.idx > 0:
                self.controller.play_sfx()
                self.controller.set_mute(True)
                self.deduct()

        # end of gems
        elif self.idx == len(self.gem_data):
            self.done = True

    def deduct(self):
        if self.score >= 50:
            self.score -= 50
        self.streak = 0

    # called by MainWidget
    def on_button_up(self, lane):
        self.display.on_button_up(lane)

    # needed to check if for pass gems (ie, went past the slop window)
    def on_update(self, time):
        self.time = time
        # done
        if self.idx == len(self.gem_data):
            self.done = True
            return
        # checks for a miss
        while time > self.gem_data[self.idx][0] + self.interval:
            self.display.gem_pass(self.idx)
            self.idx += 1
            self.controller.set_mute(True)
            self.deduct()

run(MainWidget)
