import numpy as np
from kivy.core.image import Image
from kivy.graphics import Color, Rectangle
from kivy.graphics import PushMatrix, PopMatrix, Translate, Rotate
from kivy.graphics.instructions import InstructionGroup


class Note(InstructionGroup):
    def __init__(self, pos, color, angle):
        super(Note, self).__init__()
        self.pos = np.array(pos, dtype=np.float)

        self.pos[0] += 25
        self.pos[1] += 10

        self.color = Color(*color)
        self.add(self.color)
        # adds a translation and rotation and another translation to the note
        self.add(PushMatrix())

        self.translate = Translate(*self.pos)
        self.add(self.translate)

        self._angle = Rotate(angle = angle)
        self.add(self._angle)

        self.translate2 = Translate(0, 40)
        self.add(self.translate2)

        self.note = Rectangle(texture=Image("pictures/note.png").texture, pos = (-5,-7), size = (10,15))

        self.add(self.note)

        self.add(PopMatrix())

        self.vel = np.array((0,20), dtype= np.float)

        self.color.a = 1

    def on_update(self, dt):

        self.color.a -= dt
        # apply translation
        self.translate2.xy = (self.translate2.x, self.translate2.y + self.vel[1] * dt)

        # returns true if note is visible and on the screen
        return self.color.a > 0