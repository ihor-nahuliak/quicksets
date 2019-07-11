# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .default import DefaultConfig


__all__ = ['TestingConfig']


class TestingConfig(DefaultConfig):
    POSTGRESQL_DATABASE = 'db_test'
