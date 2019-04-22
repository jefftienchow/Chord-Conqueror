from kivy.graphics import Color, Rectangle
from kivy.graphics.instructions import InstructionGroup

from Note import Note
from ChordDiagram import ChordDiagram

vel = 200
nowbar_height = 100


# Displays and controls all game elements: Nowbar, Buttons, BarLines, Gems.
class BeatMatchDisplay(InstructionGroup):
    def __init__(self, data, color_mapping):
        super(BeatMatchDisplay, self).__init__()

        self.color_mapping = color_mapping

        self.gem_data = data.get_gems()
        self.bar_data = data.get_bars()

        self.time = 0


        self.diagrams = []
        # creates gems
        self.gems = []
        cur_chord = None
        cur_display = None
        for gem_info in self.gem_data:
            gem = GemDisplay(gem_info, self.color_mapping)
            self.gems.append(gem)
            self.add(gem)
            
            if cur_chord != gem_info[1]:
                if cur_display:
                    cur_display.set_next(gem_info[0])
                cur_chord = gem_info[1]
                cur_display = ChordDisplay(gem_info[1], gem_info[0])
                self.diagrams.append(cur_display)
                self.add(cur_display)

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
        color = Color(1,1,1)
        color.a = .5
        pos = (100, nowbar_height)

        self.button = ButtonDisplay(pos,color)

        self.add(self.button)

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
    def on_button_down(self, color, hit):
        self.button.on_down(color, hit)

    # called by Player. Causes the right thing to happen
    def on_button_up(self):
        self.button.on_up()

    # call every frame to make gems and barlines flow down the screen
    def on_update(self, time):
        for gem in self.gems:
            gem.on_update(time)
        for bar in self.bars:
            bar.on_update(time)
        for diagram in self.diagrams:
            diagram.on_update(time)

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

class ChordDisplay(InstructionGroup):
    def __init__(self, chord, time_loc):
        super(ChordDisplay, self).__init__()
        self.chord = chord
        self.time = 0
        self.time_loc = time_loc
        self.next_time = None

        self.ypos = nowbar_height + (self.time_loc - self.time) * vel

        self.box = ChordDiagram(80, (700, self.ypos), chord)
        self.add(self.box)

        self.vel = vel
        
    def set_next(self, next_time):
        self.next_time = next_time

    def on_update(self, time):
        self.time = time

        self.ypos = nowbar_height + (self.time_loc - time) * vel
        
        self.box.pos = (0, self.ypos)

# display for a single gem at a position with a color (if desired)
class GemDisplay(InstructionGroup):
    def __init__(self, data, color_mapping):
        super(GemDisplay, self).__init__()
        self.time = 0
        self.type = data[1]
        self.time_loc = data[0]
        self.color_data = color_mapping[self.type]
        self.color = Color(*color_mapping[self.type])
        self.color.a = .7
        self.add(self.color)

        self.xpos = 100
        self.ypos = nowbar_height + (self.time_loc - self.time) * vel
        self.gem = Rectangle(pos=(self.xpos,self.ypos), size = (400, 10))
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
        self.button = Rectangle(pos=pos, size=(400, 20))
        self.add(self.button)

    # displays when button is down (and if it hit a gem)
    def on_down(self, color, hit):
        self.color.rgb = color

    # back to normal state
    def on_up(self):
        self.color.rgb = (1,1,1)