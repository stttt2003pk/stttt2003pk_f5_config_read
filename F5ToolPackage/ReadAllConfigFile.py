#!/usr/bin/env python
# -*- coding: utf8 -*-

from __init__ import *

__author__ = 'stttt2003pk'

class Singleton(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance

class ReadAllConfig(Singleton):
    def __init__(self, LtmConfigV11, GtmConfigV11, GtmConfigV10):
        self.LtmConfigV11_Object = GetF5V11LtmConfig(LtmConfigV11)
        self.GtmConfigV11_Object = GetF5V11GtmConfig(GtmConfigV11)
        self.GtmConfigV10_Object = GetF5V10GtmConfig(GtmConfigV10)


