"""Setup for xdgmenu
Shamelessly copy-pasted from:

https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='xdgmenu',
    version='0.0.0',

    description='A simple freedesktop based Applications menu using ncurses',
    long_description=long_description,

    url='https://github.com/crichon/xdgmenu',
    author='crichon',
    author_email='richon.c@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
	'Intended Audience :: End Users/Desktop',
	'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        # 'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='ncurses freedesktop application_launcher',

    py_modules=["xdgmenu"],
    install_requires=['urwid', 'pyxdg'],

    # $ pip install -e .[dev,test]
    extras_require={
        'dev': ['check-manifest', 'pylint'],
        # 'test': ['coverage', 'tox', 'pytest'],
    },

    entry_points={
        'console_scripts': [
            'xdgmenu=xdgmenu:main',
        ],
    },

    include_package_data=True
)
