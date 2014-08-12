#! /usr/bin/env python

from setuptools import setup, find_packages


install_requires = [
    'Flask >= 0.10.1',
    'Flask-Admin >= 1.0.8',
    'Flask-Login >= 0.2.11',
    'Flask-Plugins >= 1.4',
    'Flask-SQLAlchemy >= 1.0',
    'Flask-Uploads >= 0.1.3',
    'Flask-WTF >= 0.9.5',
    'Pillow >= 2.5.1',
    'sigal >= 0.7.0',
]

tests_require = [
    'mock >= 1.0.1',
    'nose >= 1.3.3',
    'Flask-Testing >= 0.4.2',
] + install_requires

setup(
    name='Orbach',
    version='1.0',
    author='Alex Wood',
    description='A simple gallery display tool',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    test_suite='nose.collector',
    tests_require=tests_require,
    install_requires=install_requires,
)
