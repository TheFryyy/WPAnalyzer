from lib import vector
import math as m


def vectorize(point1, point2):
    return vector.Vector(point2.x - point1.x, point2.y - point1.y)


class Point:

    def __init__(self, init_x, init_y):
        self.x = init_x
        self.y = init_y

    def __str__(self):
        return "x=" + str(self.x) + ", y=" + str(self.y)

    def __add__(self, other):
        if type(other) is Point:
            return Point(self.x + other.x, self.y + other.y)
        else:
            return Point(self.x + other[0], self.y + other[1])

    def __mul__(self, other):
        if type(other) is vector.Vector:
            return Point(self.x + other.a, self.y + other.b)

    def to_array(self):
        return [self.x, self.y]

    def equidistant(self, point):
        return Point((self.x + point.x) / 2, (self.y + point.y) / 2)

    def distance(self, point):
        return m.sqrt((self.x - point.x) ** 2 + (self.y - point.y) ** 2)

    def invert_base(self):
        return Point(self.y, self.x)