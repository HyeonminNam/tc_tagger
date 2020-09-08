# -*- coding: utf-8 -*-
from __future__ import absolute_import

from konlpy_tc.about import *

try:
    from konlpy_tc.downloader import download
except IOError:
    pass

from konlpy_tc.jvm import init_jvm
from konlpy_tc import (
    corpus,
    data,
    internals,
    tag
)
