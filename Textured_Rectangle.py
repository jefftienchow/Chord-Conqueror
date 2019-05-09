import numpy as np
from kivy.core.image import Image
from kivy.graphics import Color, Rectangle
from kivy.graphics import PushMatrix, PopMatrix, Translate, Rotate
from kivy.graphics.instructions import InstructionGroup

class Textured_Rectangle(InstructionGroup):
    def __init__(self, pos, col, dim):
        super(Textured_Rectangle, self).__init__()
        self.add(Color(*col))
        self.rectangle = Rectangle(pos = pos, size = dim)
        