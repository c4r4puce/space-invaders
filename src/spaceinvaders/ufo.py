from spaceinvaders.animation import Animation
from spaceinvaders.sprite import Sprite


class UFO(Sprite):

    def __init__(self):
        UFO_animation = Animation(1,                          # img
                                  16, 16,                     # width, height
                                  0, 24,                      # origx, origy
                                  7,                          # count
                                  fps=6)
        super().__init__(self,
                          1,                                  # depth
                          (-16, 50),                          # pos
                          3,                                  # speed
                          UFO_animation)
