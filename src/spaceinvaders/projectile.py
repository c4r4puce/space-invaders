from spaceinvaders.sprite import Sprite


class Projectile(Sprite):

    def __init__(self, depth, pos, speed, animation):
        super().__init__(depth,
                        pos,
                        speed,
                        animation)

    def handle_collision(self):
        pass

    def update(self):
        super().update()

        if self.destroyed:
            return

        self.handle_collision()
