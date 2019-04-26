from common.core import *
from common.gfxutil import *

from Audio import AudioController
from Display import *

class ProgressBar(InstructionGroup):
    def __init__(self, sections, start, end, color_mapping):
        super().__init__()
        self.start_time = sections[start][0]
        self.end_time = sections[end][0]
        self.duration = self.end_time - self.start_time

        self.color_mapping = color_mapping

        x_loc = 50
        for i in range(start, end):
            print(sections[i][1])
            color = self.color_mapping[sections[i][1]]
            self.add(Color(*color))
            length = (sections[i+1][0] - sections[i][0]) * 700 / self.duration
            rectangle = Rectangle(pos=(x_loc, 500), size = (length, 50))
            self.add(rectangle)
            x_loc += length

        self.add(Color(1,1,1))
        self.cursor = Rectangle(pos = (50, 500), size = (2, 50))
        self.add(self.cursor)

    def set_cursor(self, time):
        xpos = (time - self.start_time) * 700 / self.duration + 50
        self.cursor.pos = (xpos, 500)

