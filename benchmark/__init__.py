from timeit import timeit

from postgis import Point


def main():
    point = Point([1.23456789, 48.765432])
    ewkb = point.to_ewkb()
    time = timeit('read(ewkb)',
                  setup='from postgis.ewkb import read',
                  number=1000000, globals=locals())
    print("Read Point", time)
    time = timeit('point.to_ewkb()',
                  number=1000000, globals=locals())
    print("Write Point", time)


if __name__ == '__main__':
    main()
