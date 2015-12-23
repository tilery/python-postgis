import pytest

from postgis import MultiPoint, Point


@pytest.mark.parametrize('expected', [
    ((30, 10), (10, 30)),
])
def test_multipoint_should_round(cursor, expected):
    params = [MultiPoint(expected, srid=4326)]
    cursor.execute('INSERT INTO multipoint (geom) VALUES (%s)', params)
    cursor.execute('SELECT geom FROM multipoint WHERE geom=%s', params)
    geom = cursor.fetchone()[0]
    assert geom.coords == expected


def test_multipoint_geojson():
    line = MultiPoint(((1, 2), (3, 4)))
    assert line.geojson == {"type": "MultiPoint",
                            "coordinates": ((1, 2), (3, 4))}


def test_geom_should_compare_with_coords():
    assert ((30, 10), (10, 30), (40, 40)) == MultiPoint(((30, 10), (10, 30), (40, 40)))  # noqa


def test_multipoint_get_item():
    multi = MultiPoint(((30, 10), (10, 30), (40, 40)))
    assert multi[0] == Point(30, 10)
