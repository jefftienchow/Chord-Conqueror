from kivy.graphics import Color, Rectangle


#chord_to_index = {"C": 0, "D": 1, "D7": 2, "e": 3, "G": 4}

name_to_midi = {"a": 69, "b": 71, "c": 72, "d": 74, "e": 76, "f": 77, "g": 79}

# Handles game logic and keeps score.
# Controls the display and the audio
class ChordPlayer(object):
    def __init__(self, display, audio_ctrl):
        super(ChordPlayer, self).__init__()

        self.display = display
        self.controller = audio_ctrl
        self.interval = .2
        self.done = False
        self.chords = {}
        self.cur_notes = []
        self.detecting = False
        self.time = 0
        self.hold_time = 0

        self.strumming = False
        self.strum_time = 0
        self.hold = False

        self.detected = set()
        self.all_chords = ['G', 'C', 'D', 'em','D7' ]
        self.current_chord = 0

        self.replay_region()

    
    def on_strum(self, note):
        if not self.strumming:
            self.cur_notes.append(note)
            self.strum_time = 0
            self.strumming = True
        else:
            self.cur_notes.append(note)
            if len(self.cur_notes) >= 4:
                chord = self.detect_chord(self.cur_notes)
                if chord:
                    self.on_button_down(chord)
                    self.hold = True
                    self.cur_notes = []
                    self.hold_time = 0
                else:
                    self.display.wrong()
                    self.controller.play_sfx()


    # called by MainWidget
    def on_button_down(self, chord):
        if chord == self.all_chords[self.current_chord]:
            self.current_chord+=1
            self.display.correct(chord,True)
            self.next_region()
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
            self.cur_notes = []

        if self.hold_time > .2:
            self.hold = False
            self.hold_time = 0

            print('is this happening')


    def replay_region(self):
        self.controller.replay_region()

    def next_region(self):
        self.controller.next_region()
        self.replay_region()

    def add_chord(self, chord):
        if chord[0].islower():
            root = name_to_midi[chord[0]]
            quality = "min"
            if len(chord) == 3:
                seventh = True
            else:
                seventh = False
        else:
            root = name_to_midi[chord[0].lower()]
            quality = "Maj"
            if len(chord) == 2:
                seventh = True
            else:
                seventh = False


        notes = [root, root + 7]
        if quality == "Maj":
            notes.append(root + 4)
            if seventh:
                notes.append(root + 11)
        if quality == "min":
            notes.append(root + 3)
            if seventh:
                notes.append(root + 10)
        if quality == "Dom":
            notes.append(root + 4)
            if seventh:
                notes.append(root + 10)

        self.chords[chord] = notes

    def detect_chord(self, notes):
        for chord in self.chords:
            chord_matched = True
            for cur_note in notes:
                match = False
                for correct_note in self.chords[chord]:
                    if int(correct_note) % 12 == int(cur_note) % 12:
                        match = True
                        break
                if not match:
                    chord_matched = False
            if chord_matched:
                return chord
        return None
