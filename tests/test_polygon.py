import pytest

from postgis import Polygon


@pytest.mark.parametrize('expected', [
    (((35, 10), (45, 45), (15, 40), (10, 20), (35, 10)), ((20, 30), (35, 35), (30, 20), (20, 30))),  # noqa
])
def test_polyggon_should_round(cursor, expected):
    params = [Polygon(expected, srid=4326)]
    cursor.execute('INSERT INTO polygon (geom) VALUES (%s)', params)
    cursor.execute('SELECT geom FROM polygon WHERE geom=%s', params)
    geom = cursor.fetchone()[0]
    assert geom.coords == expected


def test_geom_should_compare_with_coords():
    assert (((35, 10), (45, 45), (15, 40), (10, 20), (35, 10)), ((20, 30), (35, 35), (30, 20), (20, 30))) == Polygon((((35, 10), (45, 45), (15, 40), (10, 20), (35, 10)), ((20, 30), (35, 35), (30, 20), (20, 30))))  # noqa


def test_polygon_geojson():
    poly = Polygon((((1, 2), (3, 4), (5, 6), (1, 2)),))
    assert poly.geojson == {"type": "Polygon",
                            "coordinates": (((1, 2), (3, 4), (5, 6), (1, 2)),)}
