# psycopg-postgis

PostGIS helpers for psycopg2.

**Warning: experimental work in progress, only Point, LineString, Polygon supported at this time**

## Install

Not pypi release yet:

    pip install git+https://github.com/yohanboniface/psycopg-postigs

You can first install cython to have a compiled version:

    pip install cython


## Usage

You need to register the extension:

    from postgis import register
    register(mydatabase.get_cursor())

Then you can pass points to psycopg:

    cursor.execute('INSERT INTO table (geom) VALUES (%s)', [Point(x=1, y=2, srid=4326)])
    cursor.execute('SELECT geom FROM linestrings LIMIT 1')
    geom = cursor.fetchone()[0]
    assert geom.coords == (1, 2)
