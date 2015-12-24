import glob
import imp
from setuptools import setup, find_packages, Extension
from codecs import open  # To use a consistent encoding
from os import path
import sys

META = imp.load_source('meta', path.join('.', 'postgis', '__meta__.py'))

HERE = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


def is_pkg(line):
    return line and not line.startswith(('--', 'git', '#'))


def list_modules(dirname):
    filenames = glob.glob(path.join(dirname, '*.py'))

    module_names = []
    for name in filenames:
        module, ext = path.splitext(path.basename(name))
        if module != '__init__':
            module_names.append(module)

    return module_names

with open('requirements.txt', encoding='utf-8') as reqs:
    install_requires = [l for l in reqs.read().split('\n') if is_pkg(l)]

try:
    from Cython.Distutils import build_ext
    CYTHON = True
except ImportError:
    sys.stdout.write('\nNOTE: Cython not installed. psycopg-postgis will '
                     'still work fine, but may run a bit slower.\n\n')
    CYTHON = False
    cmdclass = {}
    ext_modules = []
else:
    ext_modules = [
        Extension('postgis.' + ext, [path.join('postgis', ext + '.py')])
        for ext in list_modules(path.join(HERE, 'postgis'))]

    cmdclass = {'build_ext': build_ext}


setup(
    name='psycopg-postgis',
    version=META.__version__,
    description=META.__doc__,
    long_description=long_description,
    url=META.__homepage__,
    author=META.__author__,
    author_email=META.__contact__,
    license='WTFPL',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: GIS',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='psycopg postgis gis',
    packages=find_packages(exclude=['tests']),
    install_requires=install_requires,
    extras_require={'test': ['pytest'], 'docs': 'mkdocs'},
    include_package_data=True,
    cmdclass=cmdclass,
    ext_modules=ext_modules,
)
