from .geometry import Geometry


class Point(Geometry):

    TYPE = 1

    def __init__(self, x, y, z=None, m=None, srid=None):
        self.x = x
        self.y = y
        self.z = z
        self.m = m
        if srid is not None:
            self.srid = srid

    def __getitem__(self, item):
        if item in (0, 'x'):
            return self.x
        elif item in (1, 'y'):
            return self.y

    @property
    def has_z(self):
        return self.z is not None

    @classmethod
    def from_ewkb_body(cls, reader, srid=None):
        return cls(reader.read_double(), reader.read_double(),
                   reader.read_double() if reader.has_z else None,
                   reader.read_double() if reader.has_m else None,
                   srid)

    @property
    def wkt(self):
        return "POINT({})".format(self.wkt_coords)

    @property
    def wkt_coords(self):
        return ' '.join(map(str, self.coords))

    @property
    def coords(self):
        return tuple(p for p in (self.x, self.y, self.z, self.m)
                     if p is not None)
