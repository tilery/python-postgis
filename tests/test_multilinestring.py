from postgis import MultiLineString, LineString


def test_multilinestring_geojson():
    multi = MultiLineString((((30, 10), (10, 30)), ((40, 10), (10, 40))))
    assert multi.geojson == {
        "type": "MultiLineString",
        "coordinates": (((30, 10), (10, 30)), ((40, 10), (10, 40)))
    }


def test_geom_should_compare_with_coords():
    assert (((30, 10), (10, 30)), ((40, 10), (10, 40))) == MultiLineString((((30, 10), (10, 30)), ((40, 10), (10, 40))))  # noqa


def test_multilinestring_get_item():
    multi = MultiLineString((((30, 10), (10, 30)), ((40, 10), (10, 40))))
    assert multi[0] == LineString(((30, 10), (10, 30)))
