import pyxel

from spaceinvaders.animation         import Animation, TOP_TO_BOTTOM
from spaceinvaders.path              import Path
from spaceinvaders.sprite            import Sprite
from spaceinvaders.sprite_manager    import SpriteManager
from spaceinvaders.vector            import Vector
from spaceinvaders.vertical_speed    import VerticalSpeed
from spaceinvaders.horizontal_speed  import HorizontalSpeed


class UFO(Sprite):

    def __init__(self):
        animation = Animation(1,                          # img
                              16, 16,                     # width, height
                              0, 24,                      # origx, origy
                              7,                          # count
                              fps=6)
        
        r = HorizontalSpeed(1.0)
        l = HorizontalSpeed(-1.0)
        moves = 128*[r] + 128*[l]
          
        super().__init__(1,                                  # depth
                         Vector(-16, 32),                    # pos
                         Path(moves, loop=True),             # speed
                         animation)
