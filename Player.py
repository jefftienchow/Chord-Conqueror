from kivy.graphics import Color, Rectangle


color_mapping = {1:(1,0,0), 2:(1,1,0), 3: (0,1,0), 4: (0,1,1), 5:(0,0,1)}

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
        self.chords = {}

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
    def on_button_down(self, chord):
        self.display.on_button_down(color_mapping[chord + 1], None)
        if self.idx < len(self.gem_data):
            if self.time >= self.gem_data[self.idx][0] - self.interval and self.time <= self.gem_data[self.idx][0] + self.interval:
                # a correct note is hit
                if chord + 1 == self.gem_data[self.idx][1]:
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
    def on_button_up(self):
        self.display.on_button_up()

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

    def generate_chord(self, root, quality, seventh):
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

        name = quality + str(root)
        if seventh:
            name += "sev"
        self.chords[name] = notes

    def detect_chord(self, notes):
        for chord in self.chords:
            chord_matched = True
            for correct_note in chord:
                match = False
                for cur_note in notes:
                    if correct_note % 12 == cur_note % 12:
                        match = True
                        break
                if not match:
                    chord_matched = False
            if chord_matched:
                return chord
        return None



