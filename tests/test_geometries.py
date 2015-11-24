import pytest

from postgis import Point, LineString, Polygon


@pytest.mark.parametrize('expected', [
    (1, -2),
    (-1.123456789, 2.987654321),
])
def test_point_should_round(cursor, expected):
    cursor.execute('INSERT INTO points (geom) VALUES (%s)',
                   [Point(*expected, srid=4326)])
    cursor.execute('SELECT geom FROM points LIMIT 1')
    geom = cursor.fetchone()[0]
    assert geom.coords == expected


@pytest.mark.parametrize('expected', [
    ((30, 10), (10, 30), (40, 40)),
])
def test_linestring_should_round(cursor, expected):
    cursor.execute('INSERT INTO linestrings (geom) VALUES (%s)',
                   [LineString(expected, srid=4326)])
    cursor.execute('SELECT geom FROM linestrings LIMIT 1')
    geom = cursor.fetchone()[0]
    assert geom.coords == expected


@pytest.mark.parametrize('expected', [
    (((35, 10), (45, 45), (15, 40), (10, 20), (35, 10)), ((20, 30), (35, 35), (30, 20), (20, 30))),  # noqa
])
def test_polyggon_should_round(cursor, expected):
    cursor.execute('INSERT INTO polygons (geom) VALUES (%s)',
                   [Polygon(expected, srid=4326)])
    cursor.execute('SELECT geom FROM polygons LIMIT 1')
    geom = cursor.fetchone()[0]
    assert geom.coords == expected


@pytest.mark.parametrize('left,right', [
    ((1, -2), Point(1, -2)),
    (Point(1, -2), Point(1, -2)),
    ((-1.123456789, 2.987654321), Point(-1.123456789, 2.987654321),),
    (((30, 10), (10, 30), (40, 40)), LineString(((30, 10), (10, 30), (40, 40)))),  # noqa
    ((((35, 10), (45, 45), (15, 40), (10, 20), (35, 10)), ((20, 30), (35, 35), (30, 20), (20, 30))), Polygon((((35, 10), (45, 45), (15, 40), (10, 20), (35, 10)), ((20, 30), (35, 35), (30, 20), (20, 30))))),  # noqa
])
def test_geom_should_compare_with_coords(left, right):
    assert left == right
