import math as m


class Vector:

    def __init__(self, init_a, init_b):
        self.a = init_a
        self.b = init_b

    def __str__(self):
        return "a=" + str(self.a) + ", b=" + str(self.b)

    def __mul__(self, other):
        if type(other) is int:
            return Vector(self.a * other, self.b * other)

    def __neg__(self):
        return Vector(- self.a, - self.b)

    def orientation(self):
        if self.a >= 0 and self.b >= 0:
            return 0
        elif self.a >= 0 and self.b <= 0:
            return 1
        elif self.a <= 0 and self.b <= 0:
            return 2
        elif self.a <= 0 and self.b >= 0:
            return 3

    def norm(self):
        return m.sqrt((self.a * self.a) + (self.b * self.b))
