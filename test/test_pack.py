#!/usr/bin/env python
# -*- coding: utf8 -*-

import json

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

print json.dumps(f5config.LtmPoolSet, sort_keys=False, indent=4, separators=(',', ': '))

print F5CreateCommand.CreateLtmPoolV11()
