from spaceinvaders.sprite import Sprite


class Projectile(Sprite):

    def __init__(self, depth, pos, path, animation):
        super().__init__(depth,
                        pos,
                        path,
                        animation)

    def handle_collision(self):
        pass

    def update(self):
        super().update()

        if self.destroyed:
            return

        self.handle_collision()
