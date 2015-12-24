[![Circle CI](https://circleci.com/gh/yohanboniface/psycopg-postgis.svg?style=svg)](https://circleci.com/gh/yohanboniface/psycopg-postgis)

# psycopg-postgis

PostGIS helpers for psycopg2.

## Install

Not pypi release yet:

    pip install git+https://github.com/yohanboniface/psycopg-postgis

You can first install cython to have a compiled version:

    pip install cython


## Usage

You need to register the extension:

    > import postgis
    > postgis.register(mydatabase.get_cursor())

Then you can pass python geometries instance to psycopg:

    > cursor.execute('INSERT INTO table (geom) VALUES (%s)', [Point(x=1, y=2, srid=4326)])

And retrieve data as python geometries instances:

    > cursor.execute('SELECT geom FROM points LIMIT 1')
    > geom = cursor.fetchone()[0]
    > geom
    <Point POINT(1.0 2.0)>


## Example

    > import psycopg2
    > from postgis import register, LineString
    > db = psycopg2.connect(dbname="test")
    > cursor = db.cursor()
    > register(cursor)
    > cursor.execute('CREATE TABLE IF NOT EXISTS mytable ("geom" geometry(LineString) NOT NULL)')
    > cursor.execute('INSERT INTO mytable (geom) VALUES (%s)', [LineString([(1, 2), (3, 4)], srid=4326)])
    > cursor.execute('SELECT geom FROM mytable LIMIT 1')
    > geom = cursor.fetchone()[0]
    > geom
    <LineString LINESTRING(1.0 2.0, 3.0 4.0)>
    > geom[0]
    <Point POINT(1.0 2.0)>
    > geom.coords
    ((1.0, 2.0), (3.0, 4.0))
    > geom.geojson
    {'coordinates': ((1.0, 2.0), (3.0, 4.0)), 'type': 'LineString'}
    > str(geom.geojson)
    '{"type": "LineString", "coordinates": [[1, 2], [3, 4]]}'
