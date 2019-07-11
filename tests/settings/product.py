# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .default import DefaultConfig


__all__ = ['ProductConfig']


class ProductConfig(DefaultConfig):
    POSTGRESQL_HOST = '10.0.0.1'
    POSTGRESQL_DATABASE = 'db_prod'
    POSTGRESQL_USERNAME = 'prod_user'
    POSTGRESQL_PASSWORD = '?????????'
