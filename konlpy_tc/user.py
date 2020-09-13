#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

import os

from . import utils


def addterm(term):
    dicfilename = os.path.join(utils.installpath, "data", "dictionary.tsv")
    with open(dicfilename, 'a') as f:
        f.write(term)
