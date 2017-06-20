from postgis import LineString


def test_linestring_geojson():
    line = LineString(((1, 2), (3, 4)))
    assert line.geojson == {"type": "LineString",
                            "coordinates": ((1, 2), (3, 4))}


def test_linestring_geojson_as_string():
    line = LineString(((1, 2), (3, 4)))
    geojson = str(line.geojson)
    assert '"type": "LineString"' in geojson
    assert '"coordinates": [[1.0, 2.0], [3.0, 4.0]]' in geojson


def test_geom_should_compare_with_coords():
    assert ((30, 10), (10, 30), (40, 40)) == LineString(((30, 10), (10, 30), (40, 40)))  # noqa


def test_linestring_get_item():
    line = LineString(((30, 10), (10, 30), (40, 40)))
    assert line[0] == (30, 10)
