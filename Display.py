from kivy.graphics import Color, Rectangle
from kivy.graphics.instructions import InstructionGroup

from Note import Note
from ChordDiagram import ChordDiagram
from common.gfxutil import *
from kivy.core.image import Image
from TextLabel import TextLabel

vel = Window.height/2.5
nowbar_height = 100
to_rgb = {"red":(1, 0, 0), "purple": (148 / 255, 0, 211 / 255), "blue":(30/255, 144/255, 1), "green": (0, 1, 0), "yellow": (1, 1, 0)}

# Displays and controls all game elements: Nowbar, Buttons, BarLines, Gems.
class BeatMatchDisplay(InstructionGroup):
    def __init__(self, data, color_mapping):
        super(BeatMatchDisplay, self).__init__()
        self.objects = set()
        self.paused = True
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
            #self.add(gem)

            if cur_chord != gem_info[1]:
                if cur_display:
                    cur_display.set_next(gem_info[0])
                cur_chord = gem_info[1]
                cur_display = ChordDisplay(gem_info[1], gem_info[0], self.color_mapping[cur_chord])
                self.diagrams.append(cur_display)
                #self.add(cur_display)

            last_time = gem_info[0]

        # creates bars
        self.bars = []
        for bar_info in self.bar_data:
            bar = BarDisplay(bar_info)
            self.bars.append(bar)
            #self.add(bar)



        # creates buttons
        pos = (100, nowbar_height)

        self.button = ButtonDisplay(pos)

        self.add(self.button)

        self.score_label = TextLabel("Score: 0", pos=(Window.width/2-125, Window.height-100), font=40)
        self.add(self.score_label)

    def set_player(self, player):
        self.player = player

    def reset(self):
        for gem in self.gems:
            gem.reset()

        for object in self.gems + self.bars + self.diagrams:
            object.added = False
            object.removed = False

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
        continue_flag = True
        for object in self.gems + self.bars + self.diagrams:
            #object.on_update(time)
            if not object.removed:
                flag = object.on_update(time)
                if isinstance(flag, bool):
                    continue_flag = flag

            if object.on_screen and not object.added:
                self.add(object)
                self.objects.add(object)
                object.added = True
            elif object.added and not object.removed and not object.on_screen:
                self.remove(object)
                self.objects.remove(object)
                object.removed = True

        for object in self.objects | {self.button}:
            if self.paused:
                object.darken()
            else:
                object.brighten()

        self.anim_group.on_update()

        self.button.on_update(dt)
        self.score_label.update_text("Score: " + str(self.player.get_score()), (1,1,1))
        return continue_flag

    def toggle(self):
        self.paused = not self.paused

# display for a single gem at a position with a color (if desired)
class BarDisplay(InstructionGroup):
    def __init__(self, data):
        super(BarDisplay, self).__init__()
        self.time = 0
        self.time_loc = data
        self.color = Color(1,1,1, .7)
        self.add(self.color)

        self.ypos = nowbar_height + (self.time_loc - self.time) * vel

        self.bar = Rectangle(pos=(100,self.ypos), size = (Window.width/2, 2))
        self.add(self.bar)

        self.vel = vel
        self.notes = []
        self.added = False
        self.removed = False

    @property
    def on_screen(self):
        return self.ypos >= 0 and self.ypos <= Window.height

    # useful if gem is to animate
    def on_update(self, time):
        self.time = time

        # bar comes down and hits nowbar height at its corresponding time
        self.ypos = nowbar_height + (self.time_loc - time) * vel
        self.bar.pos = (100, self.ypos)

    def darken(self):
        self.color.a = .2

    def brighten(self):
        self.color.a = .7

class ChordDisplay(InstructionGroup):
    def __init__(self, chord, time_loc, color=Color(1,1,1)):
        super(ChordDisplay, self).__init__()
        self.chord = chord
        self.time = 0
        self.time_loc = time_loc
        self.next_time = None
        self.size = 125
        self.ypos = nowbar_height + (self.time_loc - self.time) * vel

        self.box = ChordDiagram(self.size, (600, self.ypos), chord, color)
        self.add(self.box)

        self.vel = vel
        self.added = False
        self.removed = False

    @property
    def on_screen(self):
        return self.ypos >= -300 and self.ypos <= 600
        
    def set_next(self, next_time):
        self.next_time = next_time - self.size/vel

    def on_update(self, time):
        self.time = time

        if self.time < self.time_loc:
            self.ypos = nowbar_height + (self.time_loc - time) * vel
        # catches end of song, returns flag to initialize end menu
        elif self.next_time is None:
            return False
        elif self.time > self.time_loc and self.time < self.next_time:
            self.ypos = nowbar_height
        else:
            self.ypos = nowbar_height + (self.next_time - time) * vel
        
        self.box.set_pos((550, self.ypos))
        return True

    def darken(self):
        self.box.darken()

    def brighten(self):
        self.box.brighten()

# display for a single gem at a position with a color (if desired)
class GemDisplay(InstructionGroup):
    def __init__(self, data, color_mapping):
        super(GemDisplay, self).__init__()
        self.time = 0
        self.type = data[1]
        self.time_loc = data[0]
        self.color_data = color_mapping[self.type]
        self.color = Color(1,1,1)
        self.color.a = 1
        self.add(self.color)

        self.xpos = 110
        self.ypos = nowbar_height + (self.time_loc - self.time) * vel
        color = color_mapping[self.type]
        self.gem = Rectangle(texture=Image("pictures/" + color + "_gem.png").texture, pos=(self.xpos,self.ypos), size = (1/2*Window.width - 20, 10))
        self.add(self.gem)

        self.vel = vel
        self.notes = []
        self.added = False
        self.removed = False
        self.a = 1

    @property
    def on_screen(self):
        return self.ypos >= 0 and self.ypos <= Window.height

    # change to display this gem being hit
    def on_hit(self):
        self.color.a = 0
        self.a = 0
        print('color being set to 0')

        # creates the hit effect where notes animations are added
        for i in range(9):
            note = Note((Window.width/4 + 100 - 20, nowbar_height), to_rgb[self.color_data], i * 40)
            self.add(note)
            self.notes.append(note)

    # change to display a passed gem
    def on_pass(self):
        self.color.a = .3
        self.a = .3

    def reset(self):
        self.color.a = 1
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

    def darken(self):
        self.color.a = .2

    def brighten(self):
        self.color.a = self.a

# Displays one button on the nowbar
class ButtonDisplay(InstructionGroup):
    def __init__(self, pos):
        super(ButtonDisplay, self).__init__()
        self.border_color = Color(1,1,1)
        self.pos = pos
        self.add(self.border_color)
        self.border = Rectangle(texture=Image("pictures/black.png").texture,pos=pos, size=(Window.width/2, 20))
        self.add(self.border)
        self.time = 0
        self.darkened = True

    # displays when button is down (and if it hit a gem)
    def on_down(self, color, hit):
        self.border_color.rgb = to_rgb[color]
        self.time = 0

    # back to normal state
    def on_up(self):
        self.border_color.rgb = (1, 1, 1)

    def on_update(self, dt):
        self.time += dt
        if self.time > .2 and not self.darkened:
            self.border_color.rgb = (1, 1, 1)

    def darken(self):
        self.border_color.a = .2
        self.darkened = True

    def brighten(self):
        self.border_color.a = 1
        self.darkened = False