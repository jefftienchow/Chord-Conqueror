

name_to_midi = {"a": 69, "b": 71, "c": 72, "d": 74, "e": 76, "f": 77, "g": 79}
class ChordDetector(object):
    def __init__(self):
        self.chords = {}

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
                notes.append(root + 10)
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
