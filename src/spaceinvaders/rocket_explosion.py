from spaceinvaders.animation import Animation
from spaceinvaders.rocket import Rocket
from spaceinvaders.sprite import Sprite


class RocketExplosion(Sprite):

    def __init__(self):
        rocket = Rocket()
        animation = Animation(1,                       # img
                              16, 16,                  # width, height
                              0, 40,                   # origx, origy
                              4,                       # count
                              loop=False,
                              fps=10)
        Sprite.__init__(self,
                        1,                             # depth
                        Rocket().pos.copy(),
                        Rocket().speed.copy(),
                        animation)
