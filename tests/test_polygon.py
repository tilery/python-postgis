from postgis import Polygon


def test_geom_should_compare_with_coords():
    assert (((35, 10), (45, 45), (15, 40), (10, 20), (35, 10)), ((20, 30), (35, 35), (30, 20), (20, 30))) == Polygon((((35, 10), (45, 45), (15, 40), (10, 20), (35, 10)), ((20, 30), (35, 35), (30, 20), (20, 30))))  # noqa


def test_polygon_geojson():
    poly = Polygon((((1, 2), (3, 4), (5, 6), (1, 2)),))
    assert poly.geojson == {"type": "Polygon",
                            "coordinates": (((1, 2), (3, 4), (5, 6), (1, 2)),)}


def test_polygon_wkt():
    poly = Polygon((((1, 2), (3, 4), (5, 6), (1, 2)),))
    wkt = poly.wkt
    wkt = wkt.replace('.0','')
    wkt = wkt.replace(', ',',')
    assert wkt == 'POLYGON((1 2,3 4,5 6,1 2))'
