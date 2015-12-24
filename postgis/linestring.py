from .geometry import Geometry
from .point import Point


class LineString(Geometry):

    TYPE = 2

    def __init__(self, points, srid=None):
        self.points = list(points)
        if srid:
            self.srid = srid

    def __iter__(self):
        for point in self.points:
            if not isinstance(point, Point):
                point = Point(*point)
            yield point

    @property
    def has_z(self):
        return self.points[0].has_z

    @property
    def has_m(self):
        return self.points[0].has_m

    def __getitem__(self, item):
        return self.points[item]

    @classmethod
    def from_ewkb_body(cls, reader, srid=None):
        return cls([Point.from_ewkb_body(reader)
                   for index in range(reader.read_int())], srid)

    @property
    def wkt_coords(self):
        return ', '.join(p.wkt_coords for p in self)

    @property
    def coords(self):
        return tuple(p.coords for p in self)
