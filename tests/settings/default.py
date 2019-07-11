# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class DefaultConfig:
    POSTGRESQL_HOST = 'localhost'
    POSTGRESQL_PORT = 5432
    POSTGRESQL_USERNAME = 'postgres'
    POSTGRESQL_PASSWORD = None
    POSTGRESQL_DATABASE = 'postgres'
    POSTGRESQL_POOL_MIN_SIZE = 4
    POSTGRESQL_POOL_MAX_SIZE = 32
    POSTGRESQL_POOL_RECYCLE = True

    @property
    def POSTGRESQL_CONNECTION_OPTIONS(self):
        return {
            'user': self.POSTGRESQL_USERNAME,
            'password': self.POSTGRESQL_PASSWORD,
            'host': self.POSTGRESQL_HOST,
            'port': self.POSTGRESQL_PORT,
            'database': self.POSTGRESQL_DATABASE,
            'minsize': self.POSTGRESQL_POOL_MIN_SIZE,
            'maxsize': self.POSTGRESQL_POOL_MAX_SIZE,
            'pool_recycle': self.POSTGRESQL_POOL_RECYCLE
        }
