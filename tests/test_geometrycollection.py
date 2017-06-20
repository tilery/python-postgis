from postgis import Point, LineString, Polygon, GeometryCollection

POLYGON = Polygon((
    ((1, 2), (3, 4), (5, 6), (1, 2)),
    ((2, 3), (4, 5), (6, 7), (2, 3))
))

COLLECTION = [
    Point(1, 2),
    LineString(((1, 2), (3, 4))),
    POLYGON
]


def test_geometrycollection_geojson():
    collection = GeometryCollection(COLLECTION)
    assert collection.geojson == {
        "type": "GeometryCollection",
        "geometries": [
            {'type': 'Point', 'coordinates': (1, 2)},
            {'type': 'LineString', 'coordinates': ((1, 2), (3, 4))},
            {'type': 'Polygon', 'coordinates': (
                ((1, 2), (3, 4), (5, 6), (1, 2)),
                ((2, 3), (4, 5), (6, 7), (2, 3))
            )},
        ]
    }


def test_geometrycollection_get_item():
    collection = GeometryCollection(COLLECTION)
    assert collection[2] == POLYGON


def test_geometrycollection_iter():
    collection = GeometryCollection(COLLECTION)
    for i, geom in enumerate(collection):
        assert geom == COLLECTION[i]
