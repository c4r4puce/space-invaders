class Vector:
    """A vector.

    """

    def __init__(self, x, y):
        assert type(x) in (int, float), "x must be a number"
        assert type(y) in (int, float), "y must be a number"

        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __add__(self, v):
        """All adding vectors, u + v."""
        return Vector(self.x + v.x, self.y + v.y)

    def __iadd__(self, v):
        """All adding vectors in-place, i.e., u += v."""
        assert isinstance(v, Vector),      "v must be a Vector"
        assert type(v.x) in (int, float),  "v.x must be a number"
        assert type(v.y) in (int, float),  "v.y must be a number"

        self.x += v.x
        self.y += v.y
        return self

    def to_tuple(self):
        return (self.x, self.y)

    def copy(self):
        return Vector(self.x, self.y)


