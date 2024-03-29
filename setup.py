#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Quicksets
~~~~~~~~~

Quicksets is a lightweight settings library based on Python classes.

No dependency!

It provides inheriting settings classes.
Rewrite just attributes that you really need to change:

      >>> # File: `myapp.settings.develop.py`
      >>> class DevelopConfig:
      ...     POSTGRESQL_HOST = 'localhost'
      ...     POSTGRESQL_PORT = 5432
      ...     POSTGRESQL_USERNAME = 'postgres'
      ...     POSTGRESQL_PASSWORD = None
      ...     POSTGRESQL_DATABASE = 'db'
      ...     POSTGRESQL_POOL_MIN_SIZE = 4
      ...     POSTGRESQL_POOL_MAX_SIZE = 32
      ...     POSTGRESQL_POOL_RECYCLE = True
      ...
      ...     @property
      ...     def POSTGRESQL_CONNECTION_OPTIONS(self):
      ...         return {
      ...             'user': self.POSTGRESQL_USERNAME,
      ...             'password': self.POSTGRESQL_PASSWORD,
      ...             'host': self.POSTGRESQL_HOST,
      ...             'port': self.POSTGRESQL_PORT,
      ...             'database': self.POSTGRESQL_DATABASE,
      ...             'minsize': self.POSTGRESQL_POOL_MIN_SIZE,
      ...             'maxsize': self.POSTGRESQL_POOL_MAX_SIZE,
      ...             'pool_recycle': self.POSTGRESQL_POOL_RECYCLE
      ...         }
      ...

      >>> # File: `myapp.settings.testing.py`
      >>> from myapp.settings.develop import DevelopConfig
      >>>
      >>> class TestingConfig(DevelopConfig):
      ...     POSTGRESQL_DATABASE = 'db_test'
      ...

      >>> # File: `myapp.settings.product.py`
      >>> from myapp.settings.develop import DevelopConfig
      >>>
      >>> class ProductConfig(DevelopConfig):
      ...     POSTGRESQL_HOST = '10.0.0.1'
      ...     POSTGRESQL_DATABASE = 'db_prod'
      ...     POSTGRESQL_USERNAME = 'prod_user'
      ...     POSTGRESQL_PASSWORD = '?????????'
      ...

      >>> # File: `myapp.application.py`
      >>> # run bash command `export SETTINGS="myapp.settings.product"`
      >>> from quicksets import settings
      >>>
      >>> settings.POSTGRESQL_CONNECTION_OPTIONS
      {'minsize': 4, 'maxsize': 32, 'host': '10.0.0.1', 'user': 'prod_user', 'database': 'db_prod', 'pool_recycle': True, 'password': '?????????', 'port': 5432}

:copyright: Copyright 2019-2020 by the Ihor Nahuliak, see AUTHORS.
:license: GNU General Public License v3 (GPLv3), see LICENSE for details.
"""
import os
import sys
from shutil import rmtree

try:
    from setuptools import setup, find_packages, Command
    have_setuptools = True
except ImportError:
    from distutils.core import setup

    def find_packages(*args, **kwargs):
        return [
            'quicksets',
        ]

    have_setuptools = False


__author__ = 'Ihor Nahuliak'
__author_email__ = 'ihor.nahuliak@gmail.com'
__url__ = 'https://github.com/ihor-nahuliak/quicksets'
__license__ = 'GPL v.3.0'
__version__ = '0.0.1'

__python_requires__ = [
    '>=2.7',
    '!=3.0.*',
    '!=3.1.*',
    '!=3.2.*',
    '!=3.3.*',
    '!=3.4.*',
]
__install_requires__ = [
]
__extras_requires__ = {
    'dev': [
        'setuptools',
        'twine',
        'pytest',
        'pytest-flakes',
        'pytest-mock',
        'pytest-cov',
        'python-coveralls',
    ],
}


ROOT = os.path.abspath(os.path.dirname(__file__))


# Note: To use the 'upload' functionality of this file, you must:
# $ pip install twine --dev
if have_setuptools:

    class UploadCommand(Command):
        """Support of `setup.py upload`."""

        description = 'Build and publish the package.'
        user_options = []

        @staticmethod
        def status(s):
            # print in bold font
            print('\033[1m{0}\033[0m'.format(s))

        def initialize_options(self):
            pass

        def finalize_options(self):
            pass

        def run(self):
            try:
                self.status('Removing previous builds…')
                rmtree(os.path.join(ROOT, 'dist'))
            except OSError:
                pass

            self.status('Building Source and Wheel (universal) distribution…')
            os.system('{0} setup.py sdist bdist_wheel '
                      '--universal'.format(sys.executable))

            self.status('Uploading the package to PyPI via Twine…')
            os.system('twine upload dist/*')

            # self.status('Pushing git tags…')
            # os.system('git tag v{0}'.format(__version__))
            # os.system('git push --tags')

            sys.exit()


    cmdclass = {'upload': UploadCommand}

else:
    cmdclass = None


setup(
    name='quicksets',
    version=__version__,
    description=__doc__,
    # long_description=__doc__,
    # long_description_content_type='text/plain',
    author=__author__,
    author_email=__author_email__,
    url=__url__,
    packages=find_packages(exclude=['tests']),
    platforms='any',
    zip_safe=False,
    include_package_data=True,
    python_requires=', '.join(__python_requires__),
    install_requires=__install_requires__,
    extras_require=__extras_requires__,
    license=__license__,
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Development Status :: 1 - Planning',
    ],
    # $ setup.py publish support.
    cmdclass=cmdclass,
)
