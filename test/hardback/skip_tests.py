"""
Rules to skip tests based on environment variables
"""

import os
from unittest import skipIf


def _check(env):
    return os.getenv(env, '').lower().startswith('t')


travis = skipIf(_check('TRAVIS'), 'Tests that fail in Travis')
