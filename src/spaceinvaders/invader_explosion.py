from random import randrange

from spaceinvaders.animation import Animation
from spaceinvaders.sprite import Sprite


class InvaderExplosion(Sprite):

    def __init__(self, invader):
        animation = Animation(0,                       # img
                              16, 16,                  # width, height
                              0, randrange(3, 7)*16,   # origx, origy
                              10,                      # count
                              loop=False,
                              fps=3)
        super().__init__(1,                             # depth
                        invader.pos(),                 # pos
                        invader.speed,                 # speed
                        animation)
