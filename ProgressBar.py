from common.core import *
from common.gfxutil import *

from Audio import AudioController
from Display import *

class ProgressBar(InstructionGroup):
    def __init__(self, sections, start, end, color_mapping, controller):
        super().__init__()
        self.start_time = sections[start][0]
        self.end_time = sections[end][0]
        self.duration = self.end_time - self.start_time
        self.objects = []
        self.color_mapping = color_mapping
        self.controller = controller

        x_loc = 50
        for i in range(start, end):
            print(sections[i][1])
            color = self.color_mapping[sections[i][1]]
            color = Color(*color)
            self.add(color)
            self.objects.append(color)
            length = (sections[i+1][0] - sections[i][0]) * 700 / self.duration
            rectangle = Rectangle(pos=(x_loc, 500), size = (length, 50))
            self.add(rectangle)
            self.objects.append(rectangle)
            x_loc += length
        newcolor = Color(1,1,1)
        self.add(newcolor)
        self.objects.append(newcolor)
        self.cursor = Rectangle(pos = (50, 500), size = (2, 50))

        self.add(self.cursor)
        self.objects.append(self.cursor)

    def set_cursor(self, loc):
        if loc[1] <= 550 and loc[1] >= 500 and loc[0] >= 50 and loc[0] <= 750:
            self.cursor.pos = (loc[0], 500)
            time = ((loc[0] - 50) / 700) * self.duration + self.start_time
            self.controller.set_start(time)
            #xpos = (time - self.start_time) * 700 / self.duration + 50

    def on_update(self, time):

        xpos = (time - self.start_time) * 700 /self.duration + 50
        self.cursor.pos = (xpos, 500)

    def cleanup(self):
        for obj in self.objects:
            self.remove(obj)


