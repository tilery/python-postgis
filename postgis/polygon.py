from .geometry import Geometry
from .linestring import LineString


class Polygon(Geometry):

    TYPE = 3

    def __init__(self, rings, srid=None):
        self.rings = rings
        if srid:
            self.srid = srid

    def __iter__(self):
        for line in self.rings:
            if not isinstance(line, LineString):
                line = LineString(line)
            yield line

    @property
    def has_z(self):
        return self.rings[0].has_z

    @property
    def has_m(self):
        return self.rings[0].has_m

    @classmethod
    def from_ewkb_body(cls, reader, srid=None):
        return cls([LineString.from_ewkb_body(reader)
                   for index in range(reader.read_int())], srid)

    @property
    def wkt_coords(self):
        return ', '.join('({})'.format(r.wkt_coords) for r in self)

    @property
    def coords(self):
        return tuple(r.coords for r in self)
