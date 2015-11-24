# psycopg-postgis

PostGIS helpers for psycopg2.

**Warning: experimental work in progress, only Point, LineString, Polygon supported at this time**

## Install

Not pypi release yet:

    pip install git+https://github.com/yohanboniface/psycopg-postgis

You can first install cython to have a compiled version:

    pip install cython


## Usage

You need to register the extension:

    import postgis
    postgis.register(mydatabase.get_cursor())

Then you can pass geoms to psycopg:

    cursor.execute('INSERT INTO table (geom) VALUES (%s)', [Point(x=1, y=2, srid=4326)])
    cursor.execute('SELECT geom FROM points LIMIT 1')
    geom = cursor.fetchone()[0]
    assert geom.coords == (1, 2)
