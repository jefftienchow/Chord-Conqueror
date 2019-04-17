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