#!/usr/bin/env python

import os
import sys

from distutils.util import convert_path
from distutils.core import Command
from fnmatch import fnmatchcase
from setuptools import setup, find_packages
from subprocess import call

try:
    long_description = open('README.md', 'rt').read()
except IOError:
    long_description = ''

def read_version_string():
    version = None
    sys.path.insert(0, os.path.join(os.getcwd()))
    from service_registry_cli import __version__
    version = __version__
    sys.path.pop(0)
    return version

# Commands based on Libcloud setup.py:
# https://github.com/apache/libcloud/blob/trunk/setup.py

class Pep8Command(Command):
    description = 'Run pep8 script'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            import pep8
            pep8
        except ImportError:
            print ('Missing "pep8" library. You can install it using pip: '
                   'pip install pep8')
            sys.exit(1)

        cwd = os.getcwd()
        retcode = call(('pep8 %s/service_registry_cli/' % (cwd)).split(' '))
        sys.exit(retcode)


setup(
    name='service-registry-cli',
    version=read_version_string(),
    description='Command line client for Rackspace Service Registry',
    long_description=long_description,
    author='Rackspace Hosting',
    author_email='sr@rackspace.com',
    url='https://github.com/racker/python-service-registry-cli',
    classifiers=['Development Status :: 4 - Beta',
                 'License :: OSI Approved :: Apache Software License',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2.6',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: Implementation :: PyPy',
                 'Environment :: Console',
                 ],
    cmdclass={
        'pep8': Pep8Command,
    },
    platforms=['Any'],
    install_requires=[
        # newer version is broken in 2.6, see
        # https://bitbucket.org/catherinedevlin/cmd2/issue/3/fix-a-failure-under-python-26
        'cmd2 == 0.6.4',
        'cliff >= 1.2.2-dev',
        'cliff-tablib >= 1.0',
        'cliff-rackspace >= 0.1.1',
        'service-registry >= 0.2.0, < 0.3.0'
    ],
    dependency_links = [
        'https://github.com/Kami/cliff/tarball/dev#egg=cliff-1.2.2-dev'
    ],
    packages=find_packages(),
    package_dir={
        'service_registry_cli': 'service_registry_cli'
    },
    package_data={
        'service_registry_cli': ['data/cacert.pem'],
    },
    entry_points={
        'console_scripts': [
            'raxsr = service_registry_cli.main:main'
        ],
        'cliff.formatter.list': [
            'paginated_table = cliff_rackspace.formatters:PaginatedListFormatter',
        ],
    }
)
