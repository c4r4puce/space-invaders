from spaceinvaders.invader_projectile import InvaderProjectile
from spaceinvaders.weapon import Weapon


class InvaderWeapon(Weapon):

    def __init__(self, invader):
        super().__init__(100)
        self.invader = invader

    def projectile(self):
        return InvaderProjectile(self.invader)
