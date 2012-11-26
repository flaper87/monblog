from __future__ import absolute_import

VERSION = (0, 0, 1)
__version__ = '.'.join(map(str, VERSION[0:3])) + ''.join(VERSION[3:])
__author__ = 'Flavio [flaper87] Percoco'
__contact__ = 'flaper87@flaper87.org'
__homepage__ = 'http://github.com/FlaPer87/monblog'
__docformat__ = 'restructuredtext en'
__doc__ = 'restructuredtext en'

# -eof meta-

import os
import sys

if sys.version_info < (2, 5):  # pragma: no cover
    if sys.version_info >= (2, 4):
        raise Exception(
                'Python 2.4 is not supported by this version. '
                'Please use Monblog versions 1.x.')
    else:
        raise Exception('Monblog requires Python versions 2.5 or later.')
