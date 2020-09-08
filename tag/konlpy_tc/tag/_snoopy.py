#! /usr/bin/python
# -*- coding: utf-8 -*-


class Snoopy():

    def morphs(self, phrase):
        raise NotImplementedError

    def nouns(self, phrase):
        raise NotImplementedError

    def phrases(self, phrase):
        raise NotImplementedError

    def pos(self, phrase, flatten=True, norm=False, stem=False):
        raise NotImplementedError

    def __init__(self, dicpath=''):
        raise NotImplementedError
