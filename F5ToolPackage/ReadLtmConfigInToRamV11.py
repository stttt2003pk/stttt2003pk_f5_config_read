#!/usr/bin/env python
# -*- coding: utf8 -*-

from F5_Parameter import *
import re

__author__ = "jian.lin@f5.com"
__copyright__ = "stttt2003pk&&Variegated Carp"

class Singleton(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance

class ReadLtmConfigInToRamV11(Singleton):
    def __init__(self, LtmFileNameV11):

        self.__LtmFileNameV11 = LtmFileNameV11
        self.__VsSet = {}
        ####self.vsAtt = ''
        self.__LtmPoolSet = {}
        self.__MemberSet = {}
        self.__SnatPoolSet = {}
        self.__MonitorSet = {}
        self.__HttpClassSet = {}
        self.__ReadLtmConfig()

    @property
    def VsSet(self):
        return self.__VsSet

    @property
    def LtmPoolSet(self):
        return  self.__LtmPoolSet

    @property
    def MemberSet(self):
        return  self.__MemberSet

    @property
    def MonitorSet(self):
        return self.__MonitorSet

    @property
    def HttpClassSet(self):
        return self.__HttpClassSet

    def __isVirtualServer(self, line):
        if re.match(r"^ltm\svirtual\s\S+\s{$", line):
            return True

    def __isPool(self, line):
        if re.match(r"ltm\spool\s\S+\s{$", line):
            return True

    def __isMonitor(self, line):
        if re.match(r"^ltm\smonitor\s\S+\s\S+\s{$", line):
            return True

    def __isSnatPool(self, line):
        if re.match(r"^ltm\spool\s\S+\s{$", line):
            return True

    def __isLtmProfileHttpClass(self, line):
        if re.match(r"^ltm\sprofile\shttpclass.*$", line):
            return True

    def __ReadLtmConfig(self):

        with open(self.__LtmFileNameV11, 'rb') as f:
            while 1:
                row = f.readline()
                ######read pool config
                if self.__isPool(row):
                    pool = LtmPool()
                    pool.name = re.search("^ltm\spool\s(\S+)\s{$", row).group(1).split('/Common/')[1]
                    self.__LtmPoolSet[pool.name + '-name']=pool.name

                    while 1:
                        row = f.readline()

                        if re.match(r"^\s+members\s{.*$", row):

                            while 1:
                                row = f.readline()
                                if re.match(r"^\s+\/Common\/(\S+):(\d+)\s{.*$", row):

                                    member = LtmMember()
                                    member.name = re.search(r"^\s+\/Common\/(\S+):(\d+)\s{.*$", row).group(1)
                                    member.port = re.search(r"^\s+\/Common\/(\S+):(\d+)\s{.*$", row).group(2)
                                    self.__MemberSet[member.name + '-port'] = member.port
                                    pool.members.append(member.name + ':' + member.port)

                                    while 1:

                                        row = f.readline()
                                        if re.match(r"^\s+address\s+(\d+\.\d+\.\d+\.\d+).*$", row):
                                            member.ip = re.search(r"^\s+address\s+(\d+\.\d+\.\d+\.\d+).*$", row).group(1)
                                            self.__MemberSet[member.name + '-' + pool.name + '-ip'] = member.ip
                                            continue
                                        if re.match(r"^\s+monitor\s+(\S+).*$", row):
                                            member.monitor = re.search(r"^\s+monitor\s+(\S+).*$", row).group(1)
                                            self.__MemberSet[member.name + '-' + pool.name + '-monitor']=member.monitor
                                            continue
                                        if re.match(r"^\s+priority-group\s+(\S+).*$", row):
                                            member.priority = re.search(r"^\s+priority-group\s+(\S+).*$", row).group(1)
                                            self.__MemberSet[member.name + '-' + pool.name + '-priority-group']=member.priority
                                            continue
                                        if re.match(r"^\s+ratio\s.*$", row):
                                            member.ratio=re.search(r"^\s+ratio\s(.*)$", row).group(1)
                                            self.__MemberSet[member.name + '-' + pool.name + '-ratio']=member.ratio
                                            continue
                                        if re.match(r"^\s+session\s.*$", row):
                                            pool.session=re.search(r"^\s+session\s(.*)$", row).group(1)
                                            self.__MemberSet[member.name + '-' + pool.name + '-session']=pool.session
                                            continue

                                        if re.match("^\s+}.*$", row):
                                            #pool.member.append(member.name)
                                            #self.MemberSet[member.name + "-ip"] = member.ip
                                            #self.MemberSet[member.name + "-port"] = member.port
                                            break

                                    continue

                                if re.match("^\s+}.*$", row):
                                    break

                        if re.match(r"^\s+min-active-members\s\d+.*$", row):
                            pool.min = re.search(r"^\s+min-active-members\s(\d+).*$", row).group(1)
                            self.__LtmPoolSet[pool.name + '-min']=pool.min
                            continue
                        if re.match(r"^\s+monitor\s(\S+).*$", row):
                            pool.monitor = re.search(r"^\s+monitor\s(.*)$", row).group(1)
                            self.__LtmPoolSet[pool.name + '-monitor'] = pool.monitor
                            continue
                        if re.match(r"^\s+slow-ramp-time\s.*$", row):
                            pool.slow=re.search(r"^\s+slow-ramp-time\s(.*)$", row).group(1)
                            self.__LtmPoolSet[pool.name + '-slow-ramp-time']=pool.slow
                            continue
                        if re.match(r"\s+load-balancing-mode\s.*$", row):
                            pool.lbmethod=re.search(r"\s+load-balancing-mode\s(.*)$", row).group(1)
                            self.__LtmPoolSet[pool.name + '-load-balancing-mode']=pool.lbmethod
                            continue

                        if re.match("^}$", row):
                            self.__LtmPoolSet[pool.name] = pool.members
                            break

                ######read virtualserver config
                if self.__isVirtualServer(row):
                    vs = LtmVirtualServer()
                    vs.name = re.search("^ltm\svirtual\s(\S+)\s{$", row).group(1)

                    while 1:
                        row = f.readline()
                        if (not row) or (re.match("^\S.*$", row)):
                            self.__VsSet[vs.name + '-name'] = vs.name
                            if row != '':
                                row = row.rstrip()
                            break
                        row = row.rstrip()
                        if re.match("^\s+destination\s\/Common\/(\d+\.\d+\.\d+\.\d+):(\S+)$", row) or re.match("^[\s]{4}destination\s.*$", row):
                            if re.match("^\s+destination\s\/Common\/(\d+\.\d+\.\d+\.\d+):(\S+)$", row):
                                vs.ip = re.search("^\s+destination\s\/Common\/(\d+\.\d+\.\d+\.\d+):(\S+)$", row).group(1)

                            # vs.port = re.search("^\s+destination\s\/Common\/(\d+\.\d+\.\d+\.\d+):(\S+)$", row).group(2)
                            vs.port = row.split(':')[1]
                            self.__VsSet[vs.name + '-ip'] = vs.ip
                            self.__VsSet[vs.name + '-port'] = vs.port
                            self.__VsSet[vs.name + '-destination']=re.search("^\s+destination\s(.*)$", row).group(1)

                            continue
                        if re.match("^\s+mask\s.*$", row):
                            vs.mask=re.search("^\s+mask\s(.*)$", row).group(1)
                            self.__VsSet[vs.name + '-mask']=vs.mask
                            continue

                        if re.match("^\s+connection-limit\s.*$", row):
                            vs.connectionLimit=re.search("^\s+connection-limit\s(.*)$", row).group(1)
                            self.__VsSet[vs.name + '-connection-limit']=vs.connectionLimit
                            continue

                        if re.match("^\s+disabled.*$", row):
                            vs.enable = "disable"
                            # self.vsAttSet[self.vlans_enabled] = vs.enable
                            continue

                        if re.match("^\s+ip-protocol\s(.*)$", row):
                            vs.protocol = re.search("^\s+ip-protocol\s(.*)$", row).group(1)
                            self.__VsSet[vs.name + '-protocol'] = vs.protocol
                            continue

                        if re.match("^\s+source\s(.*)$", row):
                            vs.source=re.search("^\s+source\s(.*)$", row).group(1)
                            self.__VsSet[vs.name + '-source'] = vs.source
                            continue

                        if re.match("^\s+translate-address\s.*$", row):
                            vs.transAdd=re.search("^\s+translate-address\s(.*)$", row).group(1)
                            self.__VsSet[vs.name + '-translate-address']=vs.transAdd
                            continue

                        if re.match("^\s+translate-port\s.*$", row):
                            vs.transPort=re.search("^\s+translate-port\s(.*)$", row).group(1)
                            self.__VsSet[vs.name + '-translate-port']=vs.transPort
                            continue

                        if re.match("^\s+pool\s(.*)$", row):
                            # vs.pool = re.search("^\s+pool\s(.*)$", row).group(1)
                            vs.pool = row.split('/Common/')[1]
                            self.__VsSet[vs.name + '-pool'] = vs.pool
                            continue

                        if re.match("^[\s]{4}vlans-enabled$", row):
                            vs.vlanEnable='vlans-enabled'
                            self.__VsSet[vs.name + '-vlans-enabled']=vs.vlanEnable
                            continue

                        if re.match("^\s+source-address-translation\s{$", row):
                            while 1:
                                row = f.readline()
                                if re.match("^\s+pool\s(.*)$", row):
                                    vs.snat_pool = re.search("^\s+pool\s(.*)$", row).group(1)
                                    self.__VsSet[vs.name + '-snat'] = vs.snat_pool
                                    self.__VsSet[vs.name + '-snat-pool']=vs.snat_pool
                                    continue

                                if re.match("^\s+type\s(.*)$", row):
                                    vs.snat_type=re.search("^\s+type\s(.*)$", row).group(1)
                                    self.__VsSet[vs.name + '-snat-type']=vs.snat_type
                                    continue

                                if re.match("^\s+}.*$", row):
                                    break

                        if re.match("^\s+profiles\s{$", row):
                            while 1:
                                row = f.readline()
                                if re.match("^\s+\/Common\/(\S+)\s{.*$", row):
                                    #vs.profile += re.search("^\s+\/Common\/(\S+)\s{.*$", row).group(1) + ' '
                                    vs.profile.append(re.search("^\s+\/Common\/(\S+)\s{.*$", row).group(1))
                                    self.__VsSet[vs.name + '-profile'] = vs.profile
                                if re.match("^\s\s\s\s}.*$", row):
                                    break

                        if re.match("^[\s]{4}rules\s{$", row):
                            while 1:
                                row=f.readline()
                                if re.match("^\s+\/Common\/.*$", row):
                                    vs.rules.append(re.search("^\s+\/Common\/(.*)$", row).group(1))
                                    self.__VsSet[vs.name + '-rules']=vs.rules
                                    continue
                                if re.match("^[\s]{4}}.*$", row):
                                    break

                        if re.match("^\s+vlans\s{$", row):
                            while 1:
                                row=f.readline()
                                if re.match("^\s+\/Common\/.*$", row):
                                    vs.vlans.append(re.search("^\s+\/Common\/(.*)$", row).group(1))
                                    self.__VsSet[vs.name + '-vlans']=vs.vlans
                                    continue
                                if re.match("^[\s]{4}}.*$", row):
                                    break

                        if re.match("^\s+persist\s{$", row):
                            while 1:
                                row = f.readline()
                                if re.match("^\s+\/Common\/(\S+)\s{.*$", row):
                                    #vs.profile += re.search("^\s+\/Common\/(\S+)\s{.*$", row).group(1) + ' '
                                    #vs.profile.append(re.search("^\s+\/Common\/(\S+)\s{.*$", row).group(1))
                                    vs.persist.append(re.search("^\s+\/Common\/(\S+)\s{.*$", row).group(1))
                                    self.__VsSet[vs.name + '-persist'] = vs.persist
                                if re.match("^\s\s\s\s}.*$", row):
                                    break

                        if re.match("^\s+http-class\s{$", row):
                            while 1:
                                row = f.readline()
                                if re.match("^\s+\/Common\/(\S+).*$", row):
                                    #vs.httpclass = re.search("^\s+\/Common\/(\S+).*$", row).group(1)
                                    vs.httpclass.append(re.search("^\s+\/Common\/(\S+).*$", row).group(1))
                                    self.__VsSet[vs.name + '-http-class'] = vs.httpclass
                                if re.match("^\s+}.*$", row):
                                    break

                        if re.match("^}.*$", row):
                            break

                        '''
                        self.vsAtt = 'ip:%s,port:%s,protocol:%s,pool:%s,profile:%s' % (
                        vs.ip, vs.port, vs.protocol, vs.pool, vs.profile)
                        attrs = {
                            "name": vs.name,
                            "ip": vs.ip,
                            "port": vs.port,
                            "protocol": vs.protocol,
                            "pool": vs.pool,
                            "profile": vs.profile,
                        }
                        # self.vsSet[vs.name] = attrs
                        # self.vsSet[vs.name] = self.vsAtt
                        '''


                    continue

                if self.__isMonitor(row):
                    HM = LtmMonitor()
                    HM.name = re.search("^ltm\smonitor\s(\S+)\s(\S+)\s{$", row).group(2)
                    HM.type = re.search("^ltm\smonitor\s(\S+)\s(\S+)\s{$", row).group(1)
                    self.__MonitorSet[HM.name + '-name'] = HM.name
                    self.__MonitorSet[HM.name + '-type'] = HM.type

                    while 1:
                        row = f.readline()
                        if re.match("^[\s]{4}cipherlist\s(.*)$", row):
                            HM.cipherlist=re.search("^[\s]{4}cipherlist\s(.*)$", row).group(1)
                            self.__MonitorSet[HM.name + '-cipherlist'] = HM.cipherlist
                            continue
                        if re.match("^\s+defaults-from\s(.*)$", row):
                            HM.defaultFrom = re.search("^\s+defaults-from\s(.*)$", row).group(1)
                            self.__MonitorSet[HM.name + '-defaults-from'] = HM.defaultFrom
                            continue
                        if re.match("^\s+destination\s(.*)$", row):
                            HM.dest = re.search("^\s+destination\s(.*)$", row).group(1)
                            self.__MonitorSet[HM.name + '-destination'] = HM.dest
                            continue
                        if re.match("^\s+interval\s(.*)$", row):
                            HM.interval = re.search("^\s+interval\s(.*)$", row).group(1)
                            self.__MonitorSet[HM.name + '-interval'] = HM.interval
                            continue
                        if re.match("^\s+recv\s(.*)$", row):
                            HM.recv = re.search("^\s+recv\s(.*)$", row).group(1)
                            self.__MonitorSet[HM.name + '-recv'] = HM.recv
                            continue
                        if re.match("^\s+send\s(.*)$", row):
                            HM.send = re.search("^\s+send\s(.*)$", row).group(1)
                            self.__MonitorSet[HM.name + '-send'] = HM.send
                            continue
                        if re.match("^\s+time-until-up\s(.*)$", row):
                            HM.timeuntilup = re.search("^\s+time-until-up\s(.*)$", row).group(1)
                            self.__MonitorSet[HM.name + '-time-until-up'] = HM.timeuntilup
                            continue
                        if re.match("^\s+timeout\s(.*)$", row):
                            HM.timeout = re.search("^\s+timeout\s(.*)$", row).group(1)
                            self.__MonitorSet[HM.name + '-timeout'] = HM.timeout
                            continue
                        if re.match("^}.*$", row):
                            break


                ####httpclass line
                if self.__isLtmProfileHttpClass(row):
                    HC = LtmProfileHttpClass()
                    HC.name = re.search("^ltm\sprofile\shttpclass\s(.*)\s{$", row).group(1).split('/Common/')[1]
                    # print HC.name
                    self.__HttpClassSet[HC.name + '-name'] = HC.name

                    ####inside the httpclss

                    while 1:
                        row = f.readline()
                        ####break
                        if re.match("^}.*$", row):
                            break

                        if re.match("^\s+asm\s(.*)$", row):
                            HC.asm = re.search("^\s+asm\s(.*)$", row).group(1)
                            self.__HttpClassSet[HC.name + '-asm'] = HC.asm
                            continue

                        if re.match("^\s+paths\s\{\sregex:(.*)\s\}$", row):
                            HC.path = re.search("^\s+paths\s\{\sregex:(.*)\s\}$", row).group(1)
                            self.__HttpClassSet[HC.name + '-path'] = HC.path
                            continue

                        if re.match("^\s+headers\s\{\sregex:(.*)\s\}$", row):
                            HC.headers = re.search("^\s+headers\s\{\sregex:(.*)\s\}$", row).group(1)
                            self.__HttpClassSet[HC.name + '-headers'] = HC.headers
                            continue

                        if re.match("^\s+pool\s(.*)$", row):
                            HC.pool = re.search("^\s+pool\s(.*)$", row).group(1).split('/Common/')[1]
                            self.__HttpClassSet[HC.name + '-pool'] = HC.pool
                            continue


                        if re.match("^\s{4}url-rewrite\s(.*)$", row):
                            HC.uri_rewrite = re.search("^\s+url-rewrite\s(.*)$", row).group(1)
                            # print HC.uri_rewrite
                            self.__HttpClassSet[HC.name + '-urirw'] = HC.uri_rewrite
                            continue

                if row == '':
                    break

                row = row.rstrip()

        #return self.vsSet

