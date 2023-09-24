from spaceinvaders.animation      import Animation
from spaceinvaders.projectile     import Projectile
from spaceinvaders.sprite_manager import SpriteManager
from spaceinvaders.vertical_speed import VerticalSpeed


class RocketProjectile(Projectile):

    def __init__(self):
        animation = Animation(0,                          # img
                              8, 8,                       # width, height
                              0, 112,                     # origx, origy
                              1)                          # count
        rocket = SpriteManager().get("Rocket")[0]
        super().__init__(1,                               # depth
                         rocket.pos.copy(),
                         VerticalSpeed(-3.0),
                         animation)

    def handle_collision(self):
        for invader in SpriteManager().get("Invader"):
            if self.collide_with(invader) or invader.collide_with(self):
                self.hit_by(invader)
                invader.hit_by(self)
