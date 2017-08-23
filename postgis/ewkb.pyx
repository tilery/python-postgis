import binascii
from io import BytesIO
import struct
from cpython cimport bool


class Typed(type):

    types = {}

    def __new__(mcs, name, bases, attrs, **kwargs):
        cls = super().__new__(mcs, name, bases, attrs, **kwargs)
        if hasattr(cls, 'TYPE'):
            Typed.types[cls.TYPE] = cls
        return cls

    def __call__(cls, *args, **kwargs):
        # Allow to pass an instance as first argument, for blind casting.
        if args and isinstance(args[0], cls):
            return args[0]
        return super().__call__(*args, **kwargs)


cdef class Reader:

    cdef object stream
    cdef bytes endianness
    cdef public bool has_z
    cdef public bool has_m

    def __cinit__(self, object stream):
        self.stream = stream

    cpdef clone(self):
        return type(self)(self.stream)

    cpdef read(self):
        return self._read()

    cdef _read(self):
        # https://en.wikipedia.org/wiki/Well-known_text#Well-known_binary
        byte_order = self.stream.read(1)
        if byte_order == b'\x00':
            self.endianness = b'>'
        elif byte_order == b'\x01':
            self.endianness = b'<'
        else:
            raise Exception('invalid encoding')

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

    cpdef read_int(self):
        return struct.unpack(self.endianness + b'I', self.stream.read(4))[0]

    cpdef read_double(self):
        return struct.unpack(self.endianness + b'd', self.stream.read(8))[0]


cpdef read(str value):
    return Reader(BytesIO(binascii.a2b_hex(value))).read()


cdef class Writer:

    cdef object stream

    def __cinit__(self, object geometry, object stream=None):
        self.stream = stream or BytesIO()
        try:
            type_ = geometry.TYPE
        except AttributeError:
            raise ValueError('Unknown geometry {}'.format(geometry.__class__))

        # Little endian.
        self.stream.write(b'\x01')
        self.write_int(
            type_ |
            (0x80000000 if geometry.has_z else 0) |
            (0x40000000 if geometry.has_m else 0) |
            (0x20000000 if geometry.has_srid else 0))
        if geometry.has_srid:
            self.write_int(geometry.srid)

    cpdef write_int(self, value):
        self.stream.write(struct.pack(b'<I', value))

    cpdef write_double(self, value):
        self.stream.write(struct.pack(b'<d', value))

    cpdef clone(self, object geometry):
        return type(self)(geometry, self.stream)


cpdef bytes write(object value):
    writer = Writer(value)
    value.write_ewkb_body(writer)
    return binascii.b2a_hex(writer.stream.getvalue()).upper()
