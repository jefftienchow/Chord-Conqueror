from kivy.graphics import Color, Rectangle


#chord_to_index = {"C": 0, "D": 1, "D7": 2, "e": 3, "G": 4}

name_to_midi = {"a": 69, "b": 71, "c": 72, "d": 74, "e": 76, "f": 77, "g": 79}

# Handles game logic and keeps score.
# Controls the display and the audio
class ChordPlayer(object):
    def __init__(self, display, audio_ctrl, detector):
        super(ChordPlayer, self).__init__()
        self.detector = detector

        self.display = display
        self.controller = audio_ctrl
        self.interval = .2
        self.done = False
        self.chords = {}
        self.cur_notes = set()
        self.cur_strings = []
        self.detecting = False
        self.time = 0
        self.hold_time = 0

        self.strumming = False
        self.strum_time = 0
        self.hold = False

        self.detected = set()
        self.all_chords = ['G', 'C', 'D', 'em','D7' ]
        self.current_chord = 0
        self.chord_played = False

        self.detector.set_callback(self.on_button_down)

    def new_chord(self, string, note):
        self.strumming = True
        self.strum_time = 0
        self.cur_notes.clear()
        self.cur_strings.clear()
        self.cur_notes.add(note)
        self.cur_strings.append(string)

    def wrong(self):
        self.display.wrong()
        self.controller.play_sfx()

    # called by MainWidget
    def on_button_down(self, chord):
        if chord == self.all_chords[self.current_chord]:
            self.current_chord+=1
            self.display.correct(chord,True)
            self.detected.add(chord)
            self.current_chord%=len(self.all_chords)
        else:
            self.display.correct(chord, False)

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
