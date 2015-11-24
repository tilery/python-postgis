import binascii
from io import BytesIO
import struct


class Typed(type):

    types = {}

    def __new__(mcs, name, bases, attrs, **kwargs):
        cls = super().__new__(mcs, name, bases, attrs, **kwargs)
        if hasattr(cls, 'TYPE'):
            Typed.types[cls.TYPE] = cls
        return cls


class EWKBReader(object):
    # Should we use shapely/libgeos instead?

    def __init__(self, stream):
        self.stream = stream

    def clone(self):
        return EWKBReader(self.stream)

    def read(self):
        # https://en.wikipedia.org/wiki/Well-known_text#Well-known_binary
        byte_order = self.stream.read(1)
        if byte_order == b'\x00':
            self._endianness = b'>'
        elif byte_order == b'\x01':
            self._endianness = b'<'
        else:
            raise Exception('invalid EWKB encoding')

        type_ = self.read_int()
        self.has_z = bool(type_ & 0x80000000)
        self.has_m = bool(type_ & 0x40000000)
        srid = self.read_int() if bool(type_ & 0x20000000) else None
        type_ &= 0x1fffffff

        try:
            class_ = Typed.types[type_]
        except KeyError:
            raise ValueError('unsupported geometry type {0}'.format(type_))
        else:
            return class_.from_ewkb_body(self, srid)

    def read_int(self):
        return struct.unpack(self._endianness + b'I', self.stream.read(4))[0]

    def read_double(self):
        return struct.unpack(self._endianness + b'd', self.stream.read(8))[0]

    @classmethod
    def from_hex(cls, value):
        return cls(BytesIO(binascii.a2b_hex(value))).read()
