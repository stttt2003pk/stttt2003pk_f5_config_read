#!/usr/bin/env python
# -*- coding: utf8 -*-
import os, sys

cur_dir = os.path.dirname(os.path.abspath(__file__))
pack_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
#print pack_dir

if pack_dir:
    sys.path.append(pack_dir)

import F5ToolPackage
import re

__author__ = 'stttt2003pk'

'''
make some functions to search the Config more easily

'''

class ConfigSearchFunctions(object):
    def __init__(self):

        self.__WideIpToGtmPoolV11 = ''
        self.__WideIpToServerListV11 = []
        self.__IpToVsListV11 = []
        self.__VsToHttpClassV11 = None
        self.__VsToProfilesV11 = None
        self.__VsIpList = []

        self.__LtmMonitorList=[]
        self.__LtmPoolList=[]
        self.__LtmVsList=[]

    def SetLtmConfigV11(self, LtmConfigFileNameV11):
        self.__LtmConfigV11 = F5ToolPackage.GetF5V11LtmConfig(LtmConfigFileNameV11)

    def SetGtmConfigV11(self, GtmConfigFileNameV11):
        self.__GtmConfigV11 = F5ToolPackage.GetF5V11GtmConfig(GtmConfigFileNameV11)

    def SetGtmConfigV10(self, GtmConfigFileNameV10):
        self.__GtmConfigV10 = F5ToolPackage.GetF5V10GtmConfig(GtmConfigFileNameV10)

    @property
    def VsSet(self):
        return self.__LtmConfigV11.VsSet
    @property
    def LtmConfigV11(self):
        return self.__LtmConfigV11
    @property
    def LtmPoolSet(self):
        return self.__LtmConfigV11.LtmPoolSet
    @property
    def MemberSet(self):
        return self.__LtmConfigV11.MemberSet
    @property
    def MonitorSet(self):
        return self.__LtmConfigV11.MonitorSet

    @property
    def GtmSetV11(self):
        return self.__GtmConfigV11.GtmSet
    @property
    def GtmServerSetV11(self):
        return self.__GtmConfigV11.GtmServerSet
    @property
    def GtmPoolSetV11(self):
        return self.__GtmConfigV11.GtmPoolSet

    @property
    def GtmSetV10(self):
        return self.__GtmConfigV10.GtmSet
    @property
    def GtmServerSetV10(self):
        return self.__GtmConfigV10.GtmServerSet
    @property
    def GtmPoolSetV10(self):
        return self.__GtmConfigV10.GtmPoolSet

    def GetWideIpToGtmPoolV11(self, WideIp):
        return self.__SearchWideIpToGtmPoolV11(WideIp)

    def GetWideIpToServerListV11(self, WideIp):
        return self.__SearchWideipToSeverListV11(WideIp)

    def GetIpToVsListV11(self, AIp):
        return self.__SearchIpToVsV11(AIp)

    def GetVsToHttpClassV11(self, Vs):
        return self.__SearchVsToHttpClassV11(Vs)

    def GetVsToProfilesV11(self, Vs):
        return self.__SearchVsToProfilesV11(Vs)

    def GetVsToPoolName(self, Vs):
        return self.__SearchVsToPoolName(Vs)

    def GetLtmPoolNameToPoolMembersList(self, LtmPoolName):
        return self.__SearchLtmPoolNameToPoolMembersList(LtmPoolName)

    def GetVsIpList(self):
        return self.__SearchVsIpListV11()

    def GetIpToGtmServer(self, AIp):
        return self.__SearchIpToGtmServer(AIp)

    def GetGtmServerNameToGtmPoolList(self, ServerName):
        return self.__SearchGtmServerNameToGtmPoolList(ServerName)

    def GetGtmPoolListToGtmWideipList(self, GtmPoolNameList):
        return self.__SearchGtmPoolListToGtmWideipList(GtmPoolNameList)

    def GetIpToVsZero(self, Ip):
        return self.__SearchIpToVsZero(Ip)

    @property
    def GetMonitorList(self):
        for key,value in self.__LtmConfigV11.MonitorSet.items():
            if key.find('-name') == -1:
                continue
            else:
                self.__LtmMonitorList.append(value)
                continue
        return self.__LtmMonitorList

    @property
    def GetPoolList(self):
        for key,value in self.__LtmConfigV11.LtmPoolSet.items():
            if key.find('-name') == -1:
                continue
            else:
                self.__LtmPoolList.append(value)
                continue
        return set(self.__LtmPoolList)

    @property
    def GetVsList(self):
        for key,value in self.__LtmConfigV11.VsSet.items():
            if key.find('-name') == -1:
                continue
            else:
                self.__LtmVsList.append(value)
                continue
        return set(self.__LtmVsList)



####input an WideIp,find out Gtm Pool
    def __SearchWideIpToGtmPoolV11(self, WideIp):
        WideIpPool = WideIp + '-wideippool'
        return  self.__GtmConfigV11.GtmSet.get(WideIpPool, None)

####input an WideIp, Find out Gtm Servers
    def __SearchWideipToSeverListV11(self, WideIp):
        GtmPoolName = self.__SearchWideIpToGtmPoolV11(WideIp)
        return  self.__GtmConfigV11.GtmPoolSet.get(GtmPoolName, None)

####input an IP or A record , Find out the VSs
    def __SearchIpToVsV11(self, AIp):
        VsList = []
        VsSet = self.__LtmConfigV11.VsSet
        VsSetList = self.__LtmConfigV11.VsSet.items()

        for (keys, value) in VsSetList:

            if keys.find('-ip') == -1:
                continue
            else:
                if value == AIp:
                    str = keys.split('-ip')[0] + '-port'
                    VsList.append(keys.split('-ip')[0] + ':' + VsSet.get(str, None))
        return VsList

####input an VS name,output this VS s http-class
    def __SearchVsToHttpClassV11(self, Vs):
        GetVsHttpClassStr = Vs + '-http-class'
        return self.__LtmConfigV11.VsSet.get(GetVsHttpClassStr, None)

####input an Vs name, outpu this Vs s profiles
    def __SearchVsToProfilesV11(self, Vs):
        GetVsProfilesStr = Vs + '-profile'
        return self.__LtmConfigV11.VsSet.get(GetVsProfilesStr, None)

####input an Vs name, output this Vs s pool
    def __SearchVsToPoolName(self, Vs):
        GetVsPoolStr = Vs + '-pool'
        return self.__LtmConfigV11.VsSet.get(GetVsPoolStr, None)

####input an pool name, output this pool members list
    def __SearchLtmPoolNameToPoolMembersList(self, LtmPoolName):
        return self.__LtmConfigV11.LtmPoolSet.get(LtmPoolName, None)

####get all vs ip from bigip.conf
    def __SearchVsIpListV11(self):
        VsIpList = []
        VsSet = self.__LtmConfigV11.VsSet
        VsSetList = VsSet.items()
        for (keys, value) in VsSetList:
            if keys.find('-ip') == -1:
                continue
            else:
                #print F5ToolPackage.GetF5V11LtmConfig(LtmConfigFileNameV11).VsSet.get(keys, None)
                VsIpList.append(VsSet.get(keys, None))
        return list(set(VsIpList))

####input an IP, find out gtm server name
    def __SearchIpToGtmServer(self, AIp):
        GtmServerName = ''
        GtmServerSetV11List = self.__GtmConfigV11.GtmServerSet.items()
        GtmServerSetV10List = self.__GtmConfigV10.GtmServerSet.items()

        for (keys, value) in GtmServerSetV10List:
            if keys.find('-ip') == -1:
                continue
            else:
                if value == AIp:
                    GtmServerName = AIp

        for (keys, value) in GtmServerSetV11List:
            if keys.find('-ip') == -1:
                continue
            else:
                if value == AIp:
                    GtmServerName = keys.split('-ip')[0]

        return GtmServerName

####search servername to gtm pool, using gtmpool as [], because a gtm server can be attached to multiply gtm pool
    def __SearchGtmServerNameToGtmPoolList(self, ServerName):
        WideIpPoolNanme = []
        GtmPoolSetV10List = self.__GtmConfigV10.GtmPoolSet.items()
        GtmPoolSetV11List = self.__GtmConfigV11.GtmPoolSet.items()

        if re.match(r"^\d+\.\d+\.\d+\.\d+$", ServerName):
            for (keys, value) in GtmPoolSetV10List:
                for PoolIP in value:
                    if PoolIP == ServerName:
                        WideIpPoolNanme.append(keys)
        else:
            for (keys, value) in GtmPoolSetV11List:
                for MemberName in value:
                    if MemberName == ServerName:
                        WideIpPoolNanme.append(keys)

        WideIpPoolNanme = list(set(WideIpPoolNanme))
        return WideIpPoolNanme

    def __SearchGtmPoolListToGtmWideipList(self, GtmPoolNameList):
        WideipName = []
        GtmWideipSetV10List = self.__GtmConfigV10.GtmSet.items()
        GtmWideipSetV11List = self.__GtmConfigV11.GtmSet.items()

        for (keys, value) in GtmWideipSetV10List:
            if keys.find('-wideippool') == -1:
                continue
            else:
                for GtmPoolName in GtmPoolNameList:
                    if value == GtmPoolName:
                        WideipName.append(keys.split('-wideippool')[0])

        for (keys, value) in GtmWideipSetV11List:
            if keys.find('-wideippool') == -1:
                continue
            else:
                for GtmPoolName in GtmPoolNameList:
                    if value == GtmPoolName:
                        WideipName.append(keys.split('-wideippool')[0])

        WideipName = list(set(WideipName))
        return  WideipName

####input an IP , to get the VS:0 we need to create some command
    def __SearchIpToVsZero(self, Ip):
        for value in self.__SearchIpToVsV11(Ip):
            if value.split(':')[1] == '0':
                break
        return value.split(':')[0]

####get ltm monitor list
    ####def __Get









