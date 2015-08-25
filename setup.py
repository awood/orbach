#! /usr/bin/env python3

import os
import re
import subprocess

from glob import glob

from setuptools import setup, find_packages

from distutils import cmd, log
from distutils.command.clean import clean as _clean
from distutils.command.install_data import install_data as _install_data
from distutils.command.build import build as _build
from distutils.command.build_py import build_py

from distutils.dir_util import remove_tree
from distutils.version import StrictVersion

VERSIONFILE = "orbach/version.py"

# Why do this instead of just importing the module?
# See http://stackoverflow.com/a/7071358
line = open(VERSIONFILE, "r").read()
# Getting multiple captures from repetition doesn't work.  See http://stackoverflow.com/a/4651893
VERSION_INFO_RE = r"^__version_info__\s*=\s*\(((['\"]\S+['\"],?\s*)+)\)"
m = re.search(VERSION_INFO_RE, line, re.M)
if m:
    version_string = ".".join(re.findall(r"\b\S+\b", m.group(1)))
else:
    raise RuntimeError("Unable to find version string in %s." % VERSIONFILE)


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


class keys(build_py):
    description = 'Create a new keys file for gettext'
    user_options = [
        ('keys-file=', 'k', "keys file to write to"),
        ('merge', 'm', "run msgmerge on po files [default]"),
        ('no-merge', None, "don't run msgmerge on po files"),
    ]
    boolean_options = ['merge']
    negative_opt = {'no-merge': 'merge'}

    def initialize_options(self):
        super().initialize_options()
        self.keys_file = os.path.join(os.curdir, "po", "keys.pot")
        self.merge = True

    def finalize_options(self):
        super().finalize_options()

    def run(self):
        po_dir = os.path.join(os.curdir, "po")
        po_list = os.path.join(po_dir, "POTFILES.in")
        with open(po_list, "wt") as f:
            for source_file in self.get_source_files():
                f.write("%s\n" % source_file)
        cmd = ["xgettext", "-f", po_list, "-o", self.keys_file]
        rc = subprocess.call(cmd)
        if rc != 0:
            raise RuntimeError("xgettext failed")

        if self.merge:
            for f in glob(os.path.join(po_dir, '*.po')):
                log.info("Merging %s" % os.path.basename(f))
                cmd = ["msgmerge", "-N", "--backup", "none", "-U", f, self.keys_file]
                rc = subprocess.call(cmd)
                if rc != 0:
                    raise RuntimeError("msgmerge failed for %s" % os.path.basename(f))


# Courtesy http://wiki.maemo.org/Internationalize_a_Python_application
class build_trans(cmd.Command):
    description = 'Compile .po files into .mo files'

    user_options = [
        ('build-base', 'b', "build base directory"),
        ('in-place', 'i', "build .mo files in place"),
        ('domain', 'd', 'gettext domain (advanced users only)'),
    ]
    boolean_options = ['in-place']

    def initialize_options(self):
        self.build_lib = None
        self.in_place = False
        self.domain = "django"

    def finalize_options(self):
        self.set_undefined_options('build', ('build_lib', 'build_lib'))

    def compile(self, src, dest):
        log.info("Compiling %s" % src)
        cmd = ['msgfmt', '-c', '--statistics', '-o', dest, src]
        rc = subprocess.call(cmd)
        if rc != 0:
            raise RuntimeError("msgfmt failed for %s to %s" % (src, dest))

    def run(self):
        po_dir = os.path.join(os.curdir, 'po')
        for path, _, filenames in os.walk(po_dir):
            for f in filenames:
                if f.endswith('.po'):
                    lang = f[:-3]
                    src = os.path.join(path, f)
                    if self.in_place:
                        dest_path = os.path.join(os.curdir, 'orbach', 'locale', lang, 'LC_MESSAGES')
                    else:
                        dest_path = os.path.join(self.build_lib, 'orbach', 'locale', lang, 'LC_MESSAGES')
                    dest = os.path.join(dest_path, "%s.mo" % self.domain)
                    if not os.path.exists(dest_path):
                        os.makedirs(dest_path)
                    if not os.path.exists(dest):
                        self.compile(src, dest)
                    else:
                        src_mtime = os.stat(src)[8]
                        dest_mtime = os.stat(dest)[8]
                        if src_mtime > dest_mtime:
                            self.compile(src, dest)


class build(_build):
    sub_commands = _build.sub_commands + [('build_trans', None)]

    def run(self):
        _build.run(self)


class install_data(_install_data):
    def run(self):
        for lang in os.listdir('build/locale/'):
            lang_dir = os.path.join('share', 'locale', lang, 'LC_MESSAGES')
            lang_file = os.path.join('build', 'locale', lang, 'LC_MESSAGES', 'orbach.mo')
            self.data_files.append((lang_dir, [lang_file]))
        _install_data.run(self)


cmdclass = {
    'clean': clean,
    'build': build,
    'build_trans': build_trans,
    'install_data': install_data,
    'keys': keys,
}

install_requires = [
    'Django',
    'django-annoying',
    'djangorestframework',
    'django-guardian',
    'django-bcrypt',
    'django-crispy-forms',
    'django-pipeline',
    'pytz',
    'bcrypt',
    'Pillow',
    'cssmin',
    'pyScss',
    'pathlib',
    'urlpath',
]

tests_require = [
    'selenium',
    'nose',
    'yanc',
    'django-nose',
    'coverage',
    'factory_boy',
] + install_requires

version = StrictVersion("1.0.0")

setup(
    name='Orbach',
    version=version_string,
    author='Alex Wood',
    description='A simple gallery display tool',
    license='GPLv3',
    cmdclass=cmdclass,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    test_suite='nose.collector',
    tests_require=tests_require,
    install_requires=install_requires,
)
