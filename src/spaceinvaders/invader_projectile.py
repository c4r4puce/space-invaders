from spaceinvaders.animation      import Animation
from spaceinvaders.path           import Path
from spaceinvaders.projectile     import Projectile
from spaceinvaders.rocket         import Rocket
from spaceinvaders.vertical_speed import VerticalSpeed


class InvaderProjectile(Projectile):

    def __init__(self, invader):
        animation = Animation(0,                          # img
                              8, 8,                       # width, height
                              8, 112,                     # origx, origy
                              5)                          # count
        super().__init__(1, invader.pos.copy(), Path([VerticalSpeed(3.0)], loop=True), animation)

    def handle_collision(self):
        rocket = Rocket()
        if self.collide_with(rocket) or rocket.collide_with(self):
            self.hit_by(rocket)
            rocket.hit_by(self)
