from spaceinvaders.sprite_manager import SpriteManager


class Weapon:

    def __init__(self, cooldown):
        self.cooldown_reload = cooldown
        self.cooldown_current = 0

    def update(self):
        if self.cooldown_current > 0:
            self.cooldown_current -= 1

    def reload(self):
        self.cooldown_current = self.cooldown_reload

    def ready(self):
        return self.cooldown_current == 0

    def projectile(self):
        raise NotImplementedError()

    # Try to fire. Return True if fired, False otherwise.
    def fire(self):
        if not self.ready():
            return False
        SpriteManager().attach(self.projectile())
        self.reload()
        return True
