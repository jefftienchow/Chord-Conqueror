from kivy.graphics import Color, Rectangle


#chord_to_index = {"C": 0, "D": 1, "D7": 2, "e": 3, "G": 4}

name_to_midi = {"a": 69, "b": 71, "c": 72, "d": 74, "e": 76, "f": 77, "g": 79}
color_names = ["GREEN", "RED", "YELLOW", "BLUE", "ORANGE"]

# Handles game logic and keeps score.
# Controls the display and the audio
class ChordPlayer(object):
    def __init__(self, display, audio_ctrl, detector,data, mapping):
        super(ChordPlayer, self).__init__()
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
        self.chords = self.display.chord_order
        self.chord_order = []
        for chord in self.chords:
            self.chord_order.append(chord)
        self.current_chord = -1
        self.chord_played = False
        self.start_section = 0
        self.end_section = None
        # self.current_section = 92


        print(self.chords)
        print(self.chord_order)
        print(self.current_chord)
        print("REE")
        self.detector.set_callback(self.on_button_down)



    def replay_section(self):
        self.controller.set_start(int(self.data.get_sections()[self.start_section][0]))
        self.controller.set_stop(int(self.data.get_sections()[self.end_section][0]))

    def new_section(self):
        self.display.remove_options()
        self.current_chord +=1
        self.current_chord %= len(self.chord_order)
        current_section = self.chords[self.chord_order[self.current_chord]]
        self.start_section = current_section - 1
        if self.current_chord != len(self.chord_order) - 1:
            self.end_section = self.chords[self.chord_order[self.current_chord+1]] + 2
        else:
            self.end_section = self.start_section + 4

        #print("this is: " ,self.color_mapping[self.current_chord])
        # print("cur is", self.current_chord)
        # print(self.chord_order)
        self.display.show_options(self.chord_order[self.current_chord], self.color_mapping[self.chord_order[self.current_chord]])


        self.replay_section()
        
        
        
    def wrong(self):
        self.display.wrong()
        self.controller.play_sfx()

    # called by MainWidget
    def on_button_down(self, chord):
        if chord == self.chord_order[self.current_chord]:
            self.display.correct(chord,True)
            self.detected.add(chord)
            self.current_chord%=len(self.chord_order)
            self.new_section()
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

