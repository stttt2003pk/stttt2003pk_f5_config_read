#!/usr/bin/env python
# -*- coding: utf8 -*-

__author__ = "jian.lin@f5.com"
__copyright__ = "stttt2003pk&&Variegated Carp"

class LtmMember(object):
    def __init__(self):
        self.name = ""
        self.ip = ""
        self.port = ""
        self.monitor = ""
        self.priority = ""
        self.ratio = ""
        self.enabled = "enabled"


class LtmPool(object):
    def __init__(self):
        self.name = ""
        self.monitor = {}
        self.members = []
        self.lbmethod = ""
        self.min = "0"
        self.slow='0'
        self.session=''


class LtmMonitor(object):
    def __init__(self):
        self.name = ''
        self.port = ''
        self.type = ''
        self.dest = "default"
        self.interval = ''
        self.recv = ''
        self.send = ''
        self.timeout = ''
        self.defaultFrom = ''
        self.timeuntilup = ''
        self.cipherlist= ''
        self.compatibility = ''



class LtmVirtualServer(object):
    def __init__(self):
        self.ip = ""
        self.mask=''
        self.connectionLimit=''
        self.port = ""
        self.dest=''
        self.protocol = ""
        self.name = ""
        self.pool = ""
        self.snat_pool = ""
        self.snat_type=''
        self.profile = []
        self.persist = []
        self.httpclass = []
        self.transAdd=''
        self.transPort=''
        self.vlans=[]
        self.vlanEnable=''
        self.source=''
        self.rules=[]

class LtmProfileHttpClass(object):
    def __init__(self):
        self.name = ''
        self.asm = ''
        self.defaultFrom = ''
        self.path = ''
        self.headers = ''
        self.pool=''
        self.redirect=''
        self.uri_rewrite = ''



####gtm class below

class GtmWideip(object):
    def __init__(self):
        self.name = ""
        self.pool = ""


class GtmPool(object):
    def __init__(self):
        self.name = ""
        self.member = []
        self.alternatemode = ""
        self.lbmethod = ""
        self.ttl = ""


class GtmServer(object):
    def __init__(self):
        self.name = ""
        self.address = ""
        self.devicename = ""
        self.datacenter = ""
        self.monitor = ""
        self.probepool = ""
        self.product = ""



