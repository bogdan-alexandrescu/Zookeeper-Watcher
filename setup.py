import ast
from codecs import open  # To use a consistent encoding
import os
import setuptools
import setuptools.command.sdist
import sys

setuptools.command.sdist.READMES = tuple(list(setuptools.command.sdist.READMES) + ['README.md'])
here = os.path.abspath(os.path.dirname(__file__))


# Get the long description and other data from the relevant files
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
with open(os.path.join(here, 'zookeeper_watcher/zookeeper_watcher.py'), encoding='utf-8') as f:
    lines = [l.strip() for l in f if l.startswith('__')]
metadata = ast.literal_eval("{'" + ", '".join([l.replace(' = ', "': ") for l in lines]) + '}')
__author__, __license__, __version__ = [metadata[k] for k in ('__author__', '__license__', '__version__')]
if not all((__author__, __license__, __version__)):
    raise ValueError('Failed to obtain metadata from module.')


# Setup definition.
setuptools.setup(
    name='Zookeeper-Watcher',
    version=__version__,

    description='Watches a designated node in Zookeeper for data or member changes and trigger a function when an event is detected.',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/Bogdan-Alexandrescu/Zookeeper-Watcher',

    # Author details
    author=__author__,
    author_email='balex@ucdavis.edu',

    # Choose your license
    license=__license__,

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
    ],

    # What does your project relate to?
    keywords='zookeeper watch watcher kazoo nodes children',

    platforms='any',

    packages=['zookeeper_watcher'],
    zip_safe=True,

    # List run-time dependencies here.  These will be installed by pip when your
    # project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/technical.html#install-requires-vs-requirements-files
    install_requires=['kazoo'],

)