
from random import randrange

import pyxel

from spaceinvaders.animation import Animation, TOP_TO_BOTTOM
from spaceinvaders.sprite import Sprite


class Star(Sprite):

    def __init__(self):
        animation = Animation(1,                        # img
                              8, 8,                     # width, height
                              randrange(0, 9) * 8, 16,  # origx, origy
                              1,                        # count
                              direction=TOP_TO_BOTTOM,
                              fps=10)
        super().__init__(0,                                 # depth
                        (randrange(0, pyxel.width-8), -8), # pos
                        randrange(2, 4),                   # speed
                        animation)
