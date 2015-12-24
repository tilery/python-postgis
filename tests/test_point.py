import pytest

from postgis import Point


@pytest.mark.parametrize('expected', [
    (1, -2),
    (-1.123456789, 2.987654321),
])
def test_point_should_round(cursor, expected):
    params = [Point(*expected, srid=4326)]
    cursor.execute('INSERT INTO point (geom) VALUES (%s)', params)
    cursor.execute('SELECT geom FROM point WHERE geom=%s', params)
    geom = cursor.fetchone()[0]
    assert geom.coords == expected


def test_point_geojson():
    point = Point(1, 2)
    assert point.geojson == {"type": "Point", "coordinates": (1, 2)}


def test_point_should_compare_with_coords():
    assert (-1.123456789, 2.987654321) == Point(-1.123456789, 2.987654321)


def test_two_point_should_compare():
    assert Point(1, -2) == Point(1, -2)


def test_can_create_point_from_list():
    point = Point([1, 2])
    assert point.x == 1
    assert point.y == 2


def test_can_get_point_item():
    point = Point(1, 2)
    assert point[0] == 1
    assert point[1] == 2
    assert point['x'] == 1
    assert point['y'] == 2


def test_can_create_point_with_z():
    point = Point(1, 2, 3)
    assert point.has_z
    assert point.z == 3


def test_point_geojson_with_z():
    point = Point(1, 2, 3)
    assert point.geojson == {"type": "Point", "coordinates": (1, 2, 3)}


def test_point_can_be_unpacked():
    point = Point(1, 2)
    x, y = point
    assert x == 1
    assert y == 2


def test_point_can_be_unpacked_to_dict():
    point = Point(1, 2)
    data = dict(point)
    assert data['x'] == 1
    assert data['y'] == 2
    assert len(data) == 2


def test_point_with_z_can_be_unpacked():
    point = Point(1, 2, 3)
    x, y, z = point
    assert x == 1
    assert y == 2
    assert z == 3


def test_point_with_z_can_be_unpacked_to_dict():
    point = Point(1, 2, 3)
    data = dict(point)
    assert data['x'] == 1
    assert data['y'] == 2
    assert data['z'] == 3
    assert len(data) == 3
