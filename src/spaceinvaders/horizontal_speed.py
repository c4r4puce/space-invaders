from spaceinvaders.vector import Vector


class HorizontalSpeed(Vector):
    def __init__(self, speed):
        super().__init__(speed, 0)
