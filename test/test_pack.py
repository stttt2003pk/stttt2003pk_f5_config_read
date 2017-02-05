#!/usr/bin/env python
# -*- coding: utf8 -*-

__author__ = 'stttt2003pk'

import os, sys

cur_dir = os.path.dirname(os.path.abspath(__file__))
pack_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))

if pack_dir:
    sys.path.append(pack_dir)

import F5CreateCommand
import F5SearchToolFunction

config_file = os.path.abspath(os.path.join(cur_dir, 'bigip.conf'))

f5config = F5SearchToolFunction.SearchF5()
f5config.SetLtmConfigV11(config_file)

print f5config.GetVsList

print F5CreateCommand.CreateLtmPoolV11()
