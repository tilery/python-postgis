import psycopg2
import pytest

from postgis import register


db = psycopg2.connect(dbname="test")
cur = db.cursor()
register(cur)


def pytest_configure(config):
    cur.execute('CREATE TABLE IF NOT EXISTS points ("geom" geometry(Point) NOT NULL)')  # noqa
    cur.execute('CREATE TABLE IF NOT EXISTS linestrings ("geom" geometry(LineString) NOT NULL)')  # noqa
    cur.execute('CREATE TABLE IF NOT EXISTS polygons ("geom" geometry(Polygon) NOT NULL)')  # noqa


def pytest_unconfigure(config):
    cur.execute('DROP TABLE points')
    cur.execute('DROP TABLE linestrings')
    cur.execute('DROP TABLE polygons')


@pytest.fixture
def cursor():
    # Make sure tables are clean.
    cur.execute('TRUNCATE TABLE points')
    cur.execute('TRUNCATE TABLE linestrings')
    cur.execute('TRUNCATE TABLE polygons')
    return cur
