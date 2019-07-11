# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .default import DefaultConfig


__all__ = ['DevelopConfig']


class DevelopConfig(DefaultConfig):
    POSTGRESQL_DATABASE = 'db'
