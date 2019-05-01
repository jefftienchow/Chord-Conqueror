from kivy.graphics import Color, Rectangle
from ChordDetector import ChordDetector
from TextLabel import *

#chord_to_index = {"C": 0, "D": 1, "D7": 2, "e": 3, "G": 4}

name_to_midi = {"a": 69, "b": 71, "c": 72, "d": 74, "e": 76, "f": 77, "g": 79}

# Handles game logic and keeps score.
# Controls the display and the audio
class Player(object):
    def __init__(self, data, display, audio_ctrl, color_mapping, detector, main):
        super(Player, self).__init__()
        self.main = main
        self.gem_data = data.get_gems()

        self.display = display
        self.controller = audio_ctrl

        self.idx = 0
        self.interval = .2
        self.score = 0
        self.streak = 0
        self.done = False
        self.max_streak = 0
        self.hits = 0
        self.chords = {}
        self.cur_notes = set()
        self.cur_strings = []
        self.time = 0

        self.chord_played = False

        self.color_mapping = color_mapping
        self.detector = detector
        self.detector.set_callback(self.on_button_down)

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


    def wrong(self):
        self.controller.play_sfx()
        self.controller.set_mute(True)
        self.deduct()

    # called by MainWidget
    def on_button_down(self, chord):
        if self.idx < len(self.gem_data):
            if self.time >= self.gem_data[self.idx][0] - self.interval and self.time <= self.gem_data[self.idx][0] + self.interval:
                # a correct note is hit
                if chord == self.gem_data[self.idx][1]:
                    self.display.gem_hit(self.idx)
                    self.controller.set_mute(False)
                    self.idx += 1
                    self.score += 100
                    self.streak += 1
                    self.hits += 1
                    self.max_streak = max(self.streak, self.max_streak)
                    if self.streak >= 1:
                        self.score += 100
                        # new streak handling
                        #self.display.add(TextLabel(text='STREAK: %d' % self.get_streak(), pos=(400, 500)))
                        self.main.animate_streak()
                   

                # a lane miss
                else:
                    if chord is None:
                        self.wrong()
                        return
                    self.wrong()
                    self.display.gem_pass(self.idx)

            # a temporal miss
            elif self.idx > 0:
                self.wrong()

        # end of gems
        elif self.idx == len(self.gem_data):
            self.done = True

        if chord is not None:
            self.display.on_button_down(self.color_mapping[chord], None)


    def deduct(self):
        if self.score >= 50:
            self.score -= 50
        self.streak = 0
        self.main.stop_streak()

    # needed to check if for pass gems (ie, went past the slop window)
    def on_update(self, time):
        # print(self.cur_strings)
        dt = time - self.time
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

        self.detector.on_update(dt)