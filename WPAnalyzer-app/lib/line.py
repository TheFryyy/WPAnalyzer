import numpy as np
from lib import point, vector


class Line:

    def __init__(self, rho, theta):
        self.vector = vector.Vector(np.cos(theta), np.sin(theta))
        self.origin = point.Point(self.vector.a * rho, self.vector.b * rho)

    def __str__(self):
        return "origin=" + str(self.origin) + ", vector=" + str(self.vector)

    def get_tracing_point(self):
        point1 = (int(self.origin.x + 2000 * (- self.vector.b)),
                  int(self.origin.y + 2000 * self.vector.a))
        point2 = (int(self.origin.x - 2000 * (- self.vector.b)),
                  int(self.origin.y - 2000 * self.vector.a))
        return point1, point2

    def get_point(self, parameter):
        return point.Point((self.origin.x + parameter * (- self.vector.b)), (self.origin.y + parameter * self.vector.a))

    def get_intersection(self, line):
        v1 = vector.Vector(- self.vector.b, self.vector.a)
        v2 = vector.Vector(- line.vector.b, line.vector.a)
        d = v1.a * v2.b - v1.b * v2.a
        if abs(d) <= 0.0005:
            return None
        else:
            t = ((v2.b * (line.origin.x - self.origin.x)) -
                 (v2.a * (line.origin.y - self.origin.y))) / d
            u = ((v1.b * (line.origin.x - self.origin.x)) -
                 (v1.a * (line.origin.y - self.origin.y))) / d
            point1 = self.get_point(t)
            point2 = line.get_point(u)
            intersection = point1.equidistant(point2)
            return intersection
