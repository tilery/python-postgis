"""Pyscopg and asyncpg helpers to work with PostGIS."""

import sys
from pathlib import Path

from setuptools import Extension, find_packages, setup


def list_modules(dirname):
    paths = Path(dirname).glob("*.py")
    return [p.stem for p in paths if p.stem != "__init__"]


try:
    from Cython.Distutils import build_ext

    CYTHON = True
except ImportError:
    sys.stdout.write(
        "\nNOTE: Cython not installed. python-postgis will "
        "still work fine, but may run a bit slower.\n\n"
    )
    CYTHON = False
    cmdclass = {}
    ext_modules = []
else:
    ext_modules = [
        Extension("postgis." + ext, [str(Path("postgis") / f"{ext}.py")])
        for ext in list_modules(Path("postgis"))
    ]

    cmdclass = {"build_ext": build_ext}


VERSION = (1, 0, 4)

setup(
    name="postgis",
    version=".".join(map(str, VERSION)),
    description=__doc__,
    long_description=Path("README.md").read_text(),
    url="https://github.com/tilery/python-postgis",
    author="Yohan Boniface",
    author_email="yohanboniface@free.fr",
    license="WTFPL",
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: GIS",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    keywords="psycopg postgis gis asyncpg",
    packages=find_packages(exclude=["tests"]),
    extras_require={
        "test": ["pytest", "pytest-asyncio", "psycopg2", "asyncpg"],
        "docs": "mkdocs",
    },
    include_package_data=True,
    cmdclass=cmdclass,
    ext_modules=ext_modules,
)
