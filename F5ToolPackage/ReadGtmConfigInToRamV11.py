#!/usr/bin/env python
# -*- coding: utf8 -*-

from F5_Parameter import *
import re

__author__ = 'stttt2003pk&&jian.lin@f5.com'
__copyright__ = "stttt2003pk&&Variegated Carp"

class Singleton(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance

class ReadGtmConfigInToRamV11(Singleton):
    def __init__(self, GtmFileNameV11):
        self.__GtmFileNameV11 = GtmFileNameV11

        self.__GtmSet = {}
        self.__GtmPoolSet = {}
        self.__GtmServerSet = {}

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
        if re.match(r"gtm\swideip\s\S+\s{$", line):
            return True

    def __isGTMPool(self, line):
        if re.match(r"^gtm\spool\s\S+\s{$", line):
            return True

    def __isGTMServer(self, line):
        if re.match(r"^gtm\sserver\s\S+\s{$", line):
            return True

    def __ReadGtmConfig(self):
        with open(self.__GtmFileNameV11, 'rb') as f:
            while 1:
                row = f.readline()

                ####read gtm server config
                if self.__isGTMServer(row):
                    server = GtmServer()
                    server.name = re.search("^gtm\sserver\s\/Common\/(\S+)\s{$", row).group(1)

                    while 1:
                        row = f.readline()

                        if re.match(r"^\s+addresses\s{.*$", row):
                            while 1:
                                row = f.readline()
                                if re.match(r"^\s+(\d+\.\d+\.\d+\.\d+)\s{.*$", row):
                                    server.address = re.search(r"^\s+(\d+\.\d+\.\d+\.\d+)\s{.*$", row).group(1)
                                    while 1:
                                        row = f.readline()
                                        if re.match(r"^\s+device-name\s+(\S+).*$", row):
                                            server.devicename = re.search(r"^\s+device-name\s+(\S+).*$", row).group(1)
                                            self.__GtmServerSet[server.name + '-ip'] = server.address
                                            self.__GtmServerSet[server.name + '-devicename'] = server.devicename
                                            continue
                                        if re.match("^\s+}\s+$", row):
                                            break
                                    continue

                                if re.match("^\s+}\s+$", row):
                                    break
                            continue

                        if re.match(r"^\s+datacenter\s(\S+).*$", row):
                            server.datacenter = re.search(r"^\s+datacenter\s(\S+).*$", row).group(1)
                            self.__GtmServerSet[server.name + '-DC'] = server.datacenter
                            continue

                        if re.match(r"^\s+monitor\s(\S+).*$", row):
                            server.monitor = re.search(r"^\s+monitor\s(\S+).*$", row).group(1)
                            self.__GtmServerSet[server.name + '-monitor'] = server.monitor

                        if re.match(r"^\s+prober-pool\s(\S+).*$", row):
                            server.probepool = re.search(r"^\s+prober-pool\s(\S+).*$", row).group(1)
                            self.__GtmServerSet[server.name + '-probepool'] = server.probepool

                        if re.match(r"^\s+product\s(\S+).*$", row):
                            server.product = re.search(r"^\s+product\s(\S+).*$", row).group(1)
                            self.__GtmServerSet[server.name + '-product'] = server.product

                        if re.match("^}$", row):

                            break

                ####read GTM pool config
                if self.__isGTMPool(row):
                    pool = GtmPool()
                    pool.name = re.search("^gtm\spool\s\/Common\/(\S+)\s{$", row).group(1)

                    while 1:
                        row = f.readline()

                        if re.match(r"^\s+alternate-mode\s\d+.*$", row):
                            pool.alternatemode = re.search(r"^\s+alternate-mode\s(\d+).*$", row).group(1)
                            continue
                        if re.match(r"^\s+load-balancing-mode\s(\S+).*$", row):
                            pool.lbmethod = re.search(r"^\s+load-balancing-mode\s(\S+).*$", row).group(1)
                            continue
                        if re.match(r"^\s+ttl\s(\S+).*$", row):
                            pool.ttl = re.search(r"^\s+ttl\s(\S+).*$", row).group(1)
                            continue

                        if re.match(r"^\s+members\s{.*$", row):

                            while 1:
                                row = f.readline()

                                if re.match(r"^\s+\/Common\/(\S+)\s{.*$", row):
                                    combostring = re.search(r"^\s+\/Common\/(\S+)\s{.*$", row).group(1)
                                    pool.member.append(combostring.split(":")[0])

                                    while 1:
                                        row = f.readline()
                                        if re.match("^\s+}\s+$", row):
                                            break
                                    continue

                                if re.match("^\s+}\s+$", row):
                                    break
                            continue
                        if re.match("^}$", row):
                            self.__GtmPoolSet[pool.name] = pool.member
                            break

                ####read GTM wideip config
                if self.__isWideip(row):
                    wideip = GtmWideip()
                    wideip.name = re.search("^gtm\swideip\s\/Common\/(\S+)\s{$", row).group(1)
                    self.__GtmSet[wideip.name + '-name'] = wideip.name
                    while 1:
                        row = f.readline()
                        if re.match(r"^\s+\/Common\/(\S+)\s{.*$",row):
                            wideip.pool = re.match(r"^\s+\/Common\/(\S+)\s{.*$",row).group(1)
                            self.__GtmSet[wideip.name + '-wideippool'] = wideip.pool

                        if re.match("^}$",row):
                            break

                    continue

                if row == "":
                    break

                row = row.rstrip()

        #return self.gtmSet
