# -*- coding: utf-8 -*-
"""
Only ConfigD must be taken, the rest of
declared objects are not classes and must be ignored.
"""
from __future__ import unicode_literals


ConfigA = 123

ConfigB = 'xyz'

ConfigC = lambda x: x * x  # noqa: E731


class ConfigD:
    pass
