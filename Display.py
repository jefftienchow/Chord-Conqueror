from kivy.graphics import Color, Rectangle
from kivy.graphics.instructions import InstructionGroup

from Note import Note
from ChordDiagram import ChordDiagram
from common.gfxutil import *

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

        self.anim_group = AnimGroup()
        self.add(self.anim_group)

        self.diagrams = []
        # creates gems
        self.gems = []
        cur_chord = None
        cur_display = None
        last_time = None
        for gem_info in self.gem_data:
            gem = GemDisplay(gem_info, self.color_mapping)
            self.gems.append(gem)

            if cur_chord != gem_info[1]:
                if cur_display:
                    cur_display.set_next(last_time)
                cur_chord = gem_info[1]
                cur_display = ChordDisplay(gem_info[1], gem_info[0], self.color_mapping[cur_chord])
                self.diagrams.append(cur_display)

            last_time = gem_info[0]

        # creates bars
        self.bars = []
        for bar_info in self.bar_data:
            bar = BarDisplay(bar_info)
            self.bars.append(bar)

        # creates the nowbar
        self.add(Color(1,1,1,.5))
        self.nowbar = Rectangle(pos = (0,nowbar_height), size = (600, 20))
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

        for object in self.gems + self.bars + self.diagrams:
            object.added = False

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
        dt = time - self.time
        self.time = time

        for object in self.gems + self.bars + self.diagrams:
            object.on_update(time)
            if object.on_screen:
                self.add(object)
            elif object.added:
                self.remove(object)
        self.button.on_update(dt)

# display for a single gem at a position with a color (if desired)
class BarDisplay(InstructionGroup):
    def __init__(self, data):
        super(BarDisplay, self).__init__()
        self.time = 0
        self.time_loc = data
        self.color = Color(1,1,1, .7)
        self.add(self.color)

        self.ypos = nowbar_height + (self.time_loc - self.time) * vel

        self.bar = Rectangle(pos=(0,self.ypos), size = (600, 2))
        self.add(self.bar)

        self.vel = vel
        self.notes = []
        self.added = False

    @property
    def on_screen(self):
        return self.ypos >= 0 and self.ypos <= 600

    # useful if gem is to animate
    def on_update(self, time):
        self.time = time

        # bar comes down and hits nowbar height at its corresponding time
        self.ypos = nowbar_height + (self.time_loc - time) * vel

        self.bar.pos = (0, self.ypos)

class ChordDisplay(InstructionGroup):
    def __init__(self, chord, time_loc, color=Color(1,1,1)):
        super(ChordDisplay, self).__init__()
        self.chord = chord
        self.time = 0
        self.time_loc = time_loc
        self.next_time = None
        self.size = 125
        self.ypos = nowbar_height + (self.time_loc - self.time) * vel

        self.box = ChordDiagram(self.size, (650, self.ypos), chord, color)
        self.add(self.box)

        self.vel = vel
        self.added = False

    @property
    def on_screen(self):
        return self.ypos >= 0 and self.ypos <= 600
        
    def set_next(self, next_time):
        self.next_time = next_time - self.size/vel/2

    def on_update(self, time):
        self.time = time

        if self.time < self.time_loc:
            self.ypos = nowbar_height + (self.time_loc - time) * vel
        elif self.time > self.time_loc and self.time < self.next_time:
            self.ypos = nowbar_height
        else:
            self.ypos = nowbar_height + (self.next_time - time) * vel
        
        self.box.set_pos((600, self.ypos))

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
        self.added = False

    @property
    def on_screen(self):
        return self.ypos >= 0 and self.ypos <= 600

    # change to display this gem being hit
    def on_hit(self):
        self.color.a = 0

        # creates the hit effect where notes animations are added
        for i in range(6):
            note = Note((300, nowbar_height), self.color_data, i * 60)
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
        self.time = 0

    # displays when button is down (and if it hit a gem)
    def on_down(self, color, hit):
        self.color.rgb = color
        self.time = 0

    # back to normal state
    def on_up(self):
        self.color.rgb = (1,1,1)

    def on_update(self, dt):
        self.time += dt
        if self.time > .2:
            self.color.rgb = (1,1,1)