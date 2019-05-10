from common.core import *
from common.gfxutil import *

from Audio import AudioController
from Display import *

class ProgressBar(InstructionGroup):
    def __init__(self, sections, start, end, color_mapping, controller):
        super().__init__()
        # print(sections)
        # print("AAA")
        # print(end)
        self.start_time = sections[start][0]
        self.end_time = sections[end][0]
        self.duration = self.end_time - self.start_time
        self.objects = []
        self.color_mapping = color_mapping
        self.controller = controller
        self.last_pos = 0


        self.chord_order = {}

        x_loc = 50
        for i in range(start, end):
            length = (sections[i + 1][0] - sections[i][0]) * 700 / self.duration

            if sections[i][1]:
                if sections[i][1] not in self.chord_order:
                    self.chord_order[sections[i][1]] = i
                color = self.color_mapping[sections[i][1]]
                rectangle = Rectangle(texture=Image("pictures/" + color + ".png").texture, pos=(x_loc, 500),
                                      size=(length, 50))

                self.add(rectangle)
                self.objects.append(rectangle)
            x_loc += length

        
        newcolor = Color(1,1,1)
        self.add(newcolor)
        #self.objects.append(newcolor)
        self.cursor = Rectangle(pos = (50, 500), size = (2, 50))

        self.add(self.cursor)
        #self.objects.append(self.cursor)
        # print(self.chord_order)

    def set_cursor(self, loc):
        for object in self.objects:
            if loc[1] <= 550 and loc[1] >= 500 and loc[0] >= object.pos[0] and loc[0] <= object.pos[0] + object.size[0]:
                self.cursor.pos = (object.pos[0], 500)
                time = ((object.pos[0] - 50) / 700) * self.duration + self.start_time
                self.controller.set_start(time)
                self.controller.set_stop(self.end_time)




        # if loc[1] <= 550 and loc[1] >= 500 and loc[0] >= 50 and loc[0] <= 750:
        #     self.cursor.pos = (loc[0], 500)
        #     time = ((loc[0] - 50) / 700) * self.duration + self.start_time
        #     self.controller.set_start(time)
        #     #xpos = (time - self.start_time) * 700 / self.duration + 50

    def on_update(self, time):
        xpos = (time - self.start_time) * 700 /self.duration + 50
        self.cursor.pos = (xpos, 500)
        # if xpos == self.last_pos and self.controller.bg.pause == False and self.controller.bg.stop == True:
        #     print("HERE")
        self.last_pos=xpos
        # if self.cursor.pos[0] > self.end_time *700:
        #     self.controller.p

    def cleanup(self):
        for obj in self.objects:
            self.remove(obj)
