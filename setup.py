#! /usr/bin/env python

from setuptools import setup, find_packages

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
    install_requires=[
        'Flask >= 0.10.1',
        'Flask-Admin >= 1.0.8',
        'Flask-Plugins >= 1.4',
        'Flask-WTF >= 0.9.5',
        'sigal >= 0.7.0',
        'Pillow >= 2.5.1',
    ]
)
