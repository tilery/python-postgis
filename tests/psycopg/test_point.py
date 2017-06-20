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


def test_point_with_geography_column(cursor):
    cursor.execute('CREATE TABLE geography_point ("geom" geography(PointZ))')
    params = [Point(1, 2, 3, srid=4326)]
    cursor.execute('INSERT INTO geography_point (geom) VALUES (%s)', params)
    cursor.execute('SELECT geom FROM geography_point WHERE geom=%s', params)
    geom = cursor.fetchone()[0]
    assert geom.coords == (1, 2, 3)
    cursor.execute('DROP TABLE geography_point')
