from postgis import Point


def test_point_geojson():
    point = Point(1, 2)
    assert point.geojson == {"type": "Point", "coordinates": (1, 2)}


def test_point_geojson_as_string():
    point = Point(1, 2)
    geojson = str(point.geojson)
    assert '"type": "Point"' in geojson
    assert '"coordinates": [1.0, 2.0]' in geojson


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


def test_string_are_cast():
    point = Point('1', '2', '3')
    assert point.x == 1.0
    assert point.y == 2.0
    assert point.z == 3


def test_0_as_z_is_considered():
    point = Point(1, 2, 0)
    assert point.x == 1.0
    assert point.y == 2.0
    assert point.z == 0


def test_0_as_m_is_considered():
    point = Point(1, 2, 3, 0)
    assert point.x == 1.0
    assert point.y == 2.0
    assert point.z == 3
    assert point.m == 0


def test_point_is_hashable():
    p1 = Point(1, 1)
    p2 = Point(1, 1)
    p3 = Point(2, 2)
    assert {p1, p2, p3} == {p1, p3}
    p1 = Point(1, 1, srid=4326)
    p2 = Point(1, 1, srid=3857)
    assert len({p1, p2}) == 2
