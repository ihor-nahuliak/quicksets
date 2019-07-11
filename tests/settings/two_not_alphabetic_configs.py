# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .default import DefaultConfig


__all__ = ['ConfigB', 'ConfigA']


class ConfigB(DefaultConfig):
    pass


class ConfigA(DefaultConfig):
    pass
