#!/usr/bin/env python
__usage__ = "setup.py command [--options]"
__description__ = "standard install script"
__author__ = "philippe.landry@ligo.org"

#-------------------------------------------------

from setuptools import (setup, find_packages)
import glob

setup(
    name = 'ns-inf-from-eos',
    version = '0.0',
    url = 'https://github.com/landryp/ns-inf-from-eos',
    author = __author__,
    author_email = 'philippe.landry@ligo.org',
    description = __description__,
    license = '',
    scripts = glob.glob('bin/*'),
    packages = find_packages(),
    data_files = [],
    requires = [],
)
