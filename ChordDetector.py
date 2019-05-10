name_to_midi = {"a": 69, "b": 71, "c": 72, "d": 74, "e": 76, "f": 77, "g": 79}
class ChordDetector(object):
    def __init__(self):
        self.chords = {}
        self.strumming = False
        self.cur_strings = []
        self.callback = None
        self.cur_notes = set()
        self.chord_played = False
        self.chord_detected = None

    def set_callback(self, callback):
        self.callback = callback

    # new chord was detected
    def new_chord(self, string, note):
        self.strumming = True
        self.strum_time = 0
        self.cur_notes.clear()
        self.cur_strings.clear()
        self.cur_notes.add(note)
        self.cur_strings.append(string)
        self.chord_played = False

    def on_strum(self, note):
        string = note[0]
        note = note[1]
        if not self.strumming: # reset if we haven't strummed in a while
            self.new_chord(string, note)
        else:
            if string in self.cur_strings: # if we're playing a string again, this is probably a new chord?
                self.new_chord(string,note) # might want to also play a miss?
            else: # otherwise, we're adding to the same current chord
                self.cur_notes.add(note)
                self.cur_strings.append(string)
                if len(self.cur_notes) >= 4: # if 4 notes, then we want to see what chord this is
                    chord = self.detect_chord(self.cur_notes)

                    if self.chord_played and self.chord_detected != chord: # if we already played a chord, is the new note adding to the chord?
                        self.callback(chord)
                        print("why not same??")
                    elif not self.chord_played: #
                        self.chord_detected = chord
                        self.chord_played = True
                        self.callback(chord)


    def add_chord(self, chord):
        if chord[-1] == "7":
            seventh = True
        else:
            seventh = False

        if chord[0].islower():
            root = name_to_midi[chord[0]]
            quality = "min"
        else:
            root = name_to_midi[chord[0].lower()]
            quality = "Maj"

        notes = [root, root + 7]
        if quality == "Maj":
            notes.append(root + 4)
            if seventh:
                if "maj" in chord:
                    notes.append(root + 11)
                else:
                    notes.append(root + 10)
        if quality == "min":
            notes.append(root + 3)
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

    def on_update(self, dt):
        if self.strumming:
            if self.strum_time > .2:
                self.strumming = False
                self.strum_time = 0
                self.cur_strings.clear()
                self.cur_notes.clear()