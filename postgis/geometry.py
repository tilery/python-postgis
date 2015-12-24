from psycopg2 import extensions as _ext
from .reader import EWKBReader, Typed
from .geojson import GeoJSON


class Geometry(object, metaclass=Typed):

    @property
    def has_z(self):
        return False

    @property
    def has_m(self):
        return False

    @property
    def has_srid(self):
        return hasattr(self, 'srid')

    @staticmethod
    def from_ewkb(value, cursor=None):
        if not value:
            return None
        return EWKBReader.from_hex(value)

    def __conform__(self, protocol):
        if protocol is _ext.ISQLQuote:
            return self

    def getquoted(self):
        return "ST_GeometryFromText('{}', {})".format(self.wkt, self.srid)

    def __str__(self):
        return self.wkt

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.wkt)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            other = other.coords
        return self.coords == other

    @property
    def name(self):
        return self.__class__.__name__

    @property
    def wkt(self):
        return "{}({})".format(self.name.upper(), self.wkt_coords)

    @property
    def geojson(self):
        return GeoJSON({
            'type': self.name,
            'coordinates': self.coords
        })


def register(cursor):
    cursor.execute("SELECT NULL::geometry")
    oid = cursor.description[0][1]
    GEOMETRY = _ext.new_type((oid, ), "GEOMETRY", Geometry.from_ewkb)
    _ext.register_type(GEOMETRY)
