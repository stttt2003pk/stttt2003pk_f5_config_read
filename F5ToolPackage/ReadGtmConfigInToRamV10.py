#!/usr/bin/env python
# -*- coding: utf8 -*-

from ReadGtmConfigInToRamV11 import *
import re

__author__ = 'stttt2003pk&&jian.lin@f5.com'
__copyright__ = "stttt2003pk&&Variegated Carp"


class Singleton(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance


class ReadGtmConfigInToRamV10(Singleton):
    def __init__(self,  GtmFileNameV10):
        self.__GtmFileNameV10 = GtmFileNameV10

        self.__GtmSet = {}
        self.__GtmPoolSet = {}
        self.__GtmServerSet = {}
        self.__GtmPoolAttributeSet = {}

        self.__ReadGtmConfig()

    @property
    def GtmSet(self):
        return self.__GtmSet

    @property
    def GtmPoolSet(self):
        return self.__GtmPoolSet

    @property
    def GtmServerSet(self):
        return self.__GtmServerSet

    def __isWideip(self, line):
        if re.match(r"^wideip\s{.*$", line):
            return True

    def __isGTMPool(self, line):
        if re.match(r"^pool\s{.*$", line):
            return True

    def __isGTMServer(self, line):
        if re.match(r"^server\s{.*$", line):
            return True

    def __ReadGtmConfig(self):
        with open(self.__GtmFileNameV10, 'rb') as f:
            while 1:
                row = f.readline()
                ####read v10 Gtm server
                if self.__isGTMServer(row):
                    server = GtmServer()
                    server.datacenter = re.search("^server\s{\s//\sdatacenter=(\S+),.*$", row).group(1)

                    while 1:
                        row = f.readline()
                        if re.match(r"^\s+box\s{.*$", row):
                            while 1:
                                row = f.readline()
                                if re.match(r"^\s+address\s.*$", row):
                                    server.address = re.search(r"^\s+address\s(\d+\.\d+\.\d+\.\d+)$", row).group(1)
                                    continue
                                if re.match("^\s+}\s+$", row):
                                    break
                            continue

                        if re.match(r"^\s+name\s+\"(\S+)\"$", row):
                            server.name = re.search(r"^\s+name\s+\"(\S+)\"$", row).group(1)
                            continue

                        if re.match("^}$", row):
                            self.__GtmServerSet[server.name + '-datacenter'] = server.datacenter
                            self.__GtmServerSet[server.name + '-ip'] = server.address
                            break

                ####read GTM v10 pool
                if self.__isGTMPool(row):
                    pool = GtmPool()

                    while 1:
                        row = f.readline()
                        if re.match(r"^\s+name\s+\"(\S+)\"$", row):
                            pool.name = re.search(r"^\s+name\s+\"(\S+)\"$", row).group(1)
                            continue
                        if re.match(r"^\s+ttl\s+(\S+)$", row):
                            pool.ttl = re.search(r"^\s+ttl\s+(\S+)$", row).group(1)
                            continue
                        if re.match(r"^\s+member\s{.*$", row):
                            continue
                        if re.match(r"^\s+member\s+.*$", row):
                            pool.member.append(re.search(r"^\s+member\s+(\S+)$", row).group(1).split(':')[0])
                            continue
                        if re.match(r"^\s+address\s+.*$", row):
                            pool.member.append(re.search(r"^\s+address\s+(\S+)$", row).group(1).split(':')[0])
                            continue
                        if re.match(r"^}$", row):
                            self.__GtmPoolAttributeSet[pool.name + '-name'] = pool.name
                            self.__GtmPoolAttributeSet[pool.name + '-ttl'] = pool.ttl
                            self.__GtmPoolSet[pool.name] = pool.member
                            break

                ####read GTM v10 widip
                if self.__isWideip(row):

                    wideip = GtmWideip()

                    while 1:
                        row = f.readline()
                        if re.match(r"^\s+name\s+\"(\S+)\"$", row):
                            wideip.name = re.search(r"^\s+name\s+\"(\S+)\"$", row).group(1)
                            continue
                        if re.match(r"^\s+pool\s+\"(\S+)\"$", row):
                            wideip.pool = re.search(r"^\s+pool\s+\"(\S+)\"$", row).group(1)
                            continue
                        if re.match(r"^}$", row):
                            self.__GtmSet[wideip.name + '-name'] = wideip.name
                            self.__GtmSet[wideip.name + '-wideippool'] = wideip.pool
                            break

                    continue

                if row == "":
                    break

                row = row.rstrip()



