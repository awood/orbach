#! /usr/bin/env python

import os

from glob import glob

from setuptools import setup, find_packages

from distutils import log
from distutils.command.clean import clean as _clean
from distutils.dir_util import remove_tree


class clean(_clean):
    def initialize_options(self):
        self.egg_base = None
        _clean.initialize_options(self)

    def finalize_options(self):
        self.set_undefined_options('egg_info', ('egg_base', 'egg_base'))
        _clean.finalize_options(self)

    def run(self):
        if self.all:
            for f in glob(os.path.join(self.egg_base, '*.egg-info')):
                log.info("removing %s" % f)
                remove_tree(f, dry_run=self.dry_run)
        _clean.run(self)


cmdclass = {
    'clean': clean,
}

install_requires = [
    'SQLAlchemy >= 0.9.7',
    'alembic >= 0.6.7',
    'bcrypt >= 1.0.1',
    'Flask >= 0.10.1',
    'Flask-Admin >= 1.0.8',
    'Flask-Assets < 0.10.0',
    'Flask-Login >= 0.2.11',
    'Flask-Plugins >= 1.4',
    'Flask-Script >= 2.0.3',
    'Flask-SQLAlchemy >= 1.0',
    'Flask-Uploads >= 0.1.3',
    'Flask-WTF >= 0.9.5',
    'Pillow >= 2.5.1',
    'cssmin >= 0.2.0',
    'pyScss >= 1.2.0',
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
    cmdclass=cmdclass,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    test_suite='nose.collector',
    tests_require=tests_require,
    install_requires=install_requires,
)
