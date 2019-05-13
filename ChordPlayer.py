from kivy.graphics import Color, Rectangle
from TextLabel import *


#chord_to_index = {"C": 0, "D": 1, "D7": 2, "e": 3, "G": 4}

name_to_midi = {"a": 69, "b": 71, "c": 72, "d": 74, "e": 76, "f": 77, "g": 79}
# color_names = ["GREEN", "RED", "YELLOW", "BLUE", "ORANGE"]

# Handles game logic and keeps score.
# Controls the display and the audio
class ChordPlayer(object):
    def __init__(self, display, audio_ctrl, detector,data, mapping, main):
        super(ChordPlayer, self).__init__()
        self.main = main
        self.color_mapping = mapping
        self.detector = detector
        self.data = data
        self.display = display
        self.controller = audio_ctrl
        self.progress_bar = self.display.progress_bar
        self.interval = .2
        self.done = False
        self.cur_notes = set()
        self.cur_strings = []
        self.detecting = False
        self.time = 0
        self.hold_time = 0

        self.strumming = False
        self.strum_time = 0
        self.hold = False

        self.detected = set()
        self.chord_order = self.display.chord_order

        self.start = display.start
        self.end = display.end
        self.current_section = self.start



        self.current_chord_idx = 0
        self.chord_played = False
        self.start_section = self.start
        self.end_section = self.end
        self.done = False
        # self.current_section = 92


        # print(self.chords)
        # print(self.chord_order)
        # print(self.current_chord_idx)
        # print("REE")
        self.detector.set_callback(self.on_button_down)
        self.sections = self.data.get_sections()



    def replay_section(self):

        self.controller.set_start(self.sections[self.start_section][0])
        self.controller.set_stop(self.sections[self.end_section][0])

    def new_section(self):
        self.display.remove_options()
        if self.current_chord_idx == len(self.chord_order):
            self.finished()
            return
        chord = self.chord_order[self.current_chord_idx][0]
        self.current_section = self.chord_order[self.current_chord_idx][1]
        self.start_section = self.current_section - 2
        self.end_section = self.current_section + 2
        self.display.show_options(chord, self.color_mapping[chord])
        self.replay_section()
        self.current_chord_idx += 1

    def finished(self):
        self.done = True
        self.display.label.update_text("Congrats!  You guessed all the chords correctly.  Press 1 to continue.", (1,1,1))

    def wrong(self):
        self.display.wrong()
        self.controller.play_sfx()

    # called by MainWidget
    def on_button_down(self, chord):

        if not self.done and self.main.learning_started:
            print(self.chord_order[self.current_chord_idx - 1][0])
            if chord == self.chord_order[self.current_chord_idx - 1][0]:
                print('Correct', chord, self.chord_order[self.current_chord_idx - 1])
                self.display.correct(chord, True)
                self.detected.add(chord)
                # self.current_chord_idx%=len(self.chord_order)
                self.new_section()
            else:
                print('Incorrect', chord, self.chord_order[self.current_chord_idx - 1][0])
                self.display.wrong()

    # called by MainWidget
    def on_button_up(self):
        pass

    # needed to check if for pass gems (ie, went past the slop window)
    def on_update(self, time):
        dt = time - self.time
        self.time = time
        if self.hold:
            self.hold_time += dt

        if self.strumming:
            self.strum_time += dt

        if self.strum_time > .2:
            self.strum_time = 0
            self.strumming = False
            self.cur_notes.clear()
            self.cur_strings.clear()

        if self.hold_time > .2:
            self.hold = False
            self.hold_time = 0

        self.detector.on_update(dt)

