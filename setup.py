# -*- coding: utf-8 -*-
import os
from setuptools import setup
from setuptools import find_packages
from os.path import join, abspath, normpath, dirname

with open(join(dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

with open(join(dirname(__file__), 'VERSION')) as f:
    VERSION = f.read()

tests_require = ['pytest']
with open(join(dirname(abspath(__file__)), 'requirements.txt')) as f:
    for line in f:
        tests_require.append(line.strip())

# allow setup.py to be run from any path
os.chdir(normpath(join(abspath(__file__), os.pardir)))

setup(
    name='allocation',
    version=VERSION,
    author=u'louden',
    author_email='',
    packages=find_packages(),
    include_package_data=True,
    url='http://github.com/py-study-design/allocation',
    license='MIT license, see LICENSE',
    description='Functions to allocate new subjects to a trial',
    long_description=README,
    zip_safe=False,
    keywords='statistics randomization experimental-design',
    install_requires=['scipy'],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    python_requires=">=3.6",
    tests_require=tests_require,
    test_suite='runtests.main',
)
