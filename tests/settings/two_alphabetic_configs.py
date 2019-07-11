# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .default import DefaultConfig


__all__ = ['ConfigA', 'ConfigB']


class ConfigA(DefaultConfig):
    pass


class ConfigB(DefaultConfig):
    pass
