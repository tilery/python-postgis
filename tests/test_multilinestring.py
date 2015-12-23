import pytest

from postgis import MultiLineString, LineString


@pytest.mark.parametrize('expected', [
    (((30, 10), (10, 30)), ((40, 10), (10, 40))),
])
def test_multipoint_should_round(cursor, expected):
    params = [MultiLineString(expected, srid=4326)]
    cursor.execute('INSERT INTO multilinestring (geom) VALUES (%s)', params)
    cursor.execute('SELECT geom FROM multilinestring WHERE geom=%s', params)
    geom = cursor.fetchone()[0]
    assert geom.coords == expected


def test_multipoint_geojson():
    multi = MultiLineString((((30, 10), (10, 30)), ((40, 10), (10, 40))))
    assert multi.geojson == {
        "type": "MultiLineString",
        "coordinates": (((30, 10), (10, 30)), ((40, 10), (10, 40)))
    }


def test_geom_should_compare_with_coords():
    assert (((30, 10), (10, 30)), ((40, 10), (10, 40))) == MultiLineString((((30, 10), (10, 30)), ((40, 10), (10, 40))))  # noqa


def test_multipolygon_get_item():
    multi = MultiLineString((((30, 10), (10, 30)), ((40, 10), (10, 40))))
    assert multi[0] == LineString(((30, 10), (10, 30)))
