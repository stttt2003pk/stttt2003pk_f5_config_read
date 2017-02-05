#!/usr/bin/env python
# -*- coding: utf8 -*-
import os, sys
cur_dir = os.path.dirname(os.path.abspath(__file__))
pack_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))

if pack_dir:
    sys.path.append(pack_dir)

from F5ToolPackage.F5_Parameter import *

__author__ = 'stttt2003pk'

class CreateLtmCommandV11(object):
    def __init__(self):
        pass

####create monitor command
    def SetCreateHealthMonitorCommandV11(self, **kwargs):
        HealthMonitorName=kwargs.get('name')
        HealthMonitorType=kwargs.get('type')
        HealthMonitorDest=kwargs.get('destination')
        #HealthMonitorPort=kwargs.get('port')
        HealthMonitorSend=kwargs.get('send')
        HealthMonitorRecv=kwargs.get('recv')
        HealthMonitorCipherlist=kwargs.get('cipherlist')
        HealthMonitorInterval=kwargs.get('interval')
        HealthMonitorTimeUntilup=kwargs.get('timeuntilup')
        HealthMonitorTimeOut=kwargs.get('timeout')
        HealthMonitorDefaultFrom=kwargs.get('defaultfrom')

        if HealthMonitorType == 'external':
            InitCreateLtmMonitor='EAV ' + HealthMonitorName + ' should be config manual'

        if HealthMonitorName == None or HealthMonitorType == None or HealthMonitorDest == None:
            raise NameError('The Monitor s Name and the Type must be define, The Destination to be define')
        else:
            ####tcp monitor
            if HealthMonitorType == 'tcp':
                '''
                CreateLtmMonitorCommand = 'tmsh create ltm monitor tcp ' + HealthMonitorName \
                                          + ' destination ' + HealthMonitorDest \
                                          + ' interval ' + HealthMonitorInterval \
                                          + ' time-until-up ' + HealthMonitorTimeUntilup \
                                          + ' timeout ' + HealthMonitorTimeOut
                '''
                InitCreateLtmMonitor = 'tmsh create ltm monitor tcp ' + HealthMonitorName + ' destination ' + HealthMonitorDest
                if HealthMonitorDefaultFrom != None:
                    MonitorDefaultFrom = ' defaults-from ' + HealthMonitorDefaultFrom
                    InitCreateLtmMonitor+=MonitorDefaultFrom
                '''
                if HealthMonitorDest != None:
                    MonitorDest=' destination ' + HealthMonitorDest
                    InitCreateLtmMonitor+=MonitorDest
                '''
                if HealthMonitorInterval != None:
                    MonitorInterval = ' interval ' + HealthMonitorInterval
                    InitCreateLtmMonitor+=MonitorInterval
                if HealthMonitorRecv != None:
                    MonitorRecv=' recv ' + HealthMonitorRecv
                    InitCreateLtmMonitor+=MonitorRecv
                if HealthMonitorSend != None:
                    MonitorSend=' send ' + HealthMonitorSend
                    InitCreateLtmMonitor+=MonitorSend
                if HealthMonitorTimeUntilup != None:
                    MonitorTimeUntilUp=' time-until-up ' + HealthMonitorTimeUntilup
                    InitCreateLtmMonitor+=MonitorTimeUntilUp
                if HealthMonitorTimeOut != None:
                    MonitorTimeOut=' timeout ' + HealthMonitorTimeOut
                    InitCreateLtmMonitor+=MonitorTimeOut

            ####http monitor
            elif HealthMonitorType == 'http':
                InitCreateLtmMonitor='tmsh create ltm monitor http ' + HealthMonitorName + ' destination ' + HealthMonitorDest
                if HealthMonitorDefaultFrom != None:
                    MonitorDefaultFrom = ' defaults-from ' + HealthMonitorDefaultFrom
                    InitCreateLtmMonitor+=MonitorDefaultFrom
                if HealthMonitorInterval != None:
                    MonitorInterval = ' interval ' + HealthMonitorInterval
                    InitCreateLtmMonitor+=MonitorInterval
                if HealthMonitorRecv != None:
                    if HealthMonitorRecv.find('\\') != -1:
                        HealthMonitorRecv=HealthMonitorRecv.replace('\\', '\\\\')
                    MonitorRecv=' recv ' + HealthMonitorRecv
                    InitCreateLtmMonitor+=MonitorRecv
                if HealthMonitorSend != None:
                    MonitorSend=' send ' + HealthMonitorSend
                    InitCreateLtmMonitor+=MonitorSend
                if HealthMonitorTimeUntilup != None:
                    MonitorTimeUntilUp=' time-until-up ' + HealthMonitorTimeUntilup
                    InitCreateLtmMonitor+=MonitorTimeUntilUp
                if HealthMonitorTimeOut != None:
                    MonitorTimeOut=' timeout ' + HealthMonitorTimeOut
                    InitCreateLtmMonitor+=MonitorTimeOut

            elif HealthMonitorType == 'https':
                InitCreateLtmMonitor='tmsh create ltm monitor https ' + HealthMonitorName + ' destination ' + HealthMonitorDest
                if HealthMonitorDefaultFrom != None:
                    MonitorDefaultFrom = ' defaults-from ' + HealthMonitorDefaultFrom
                    InitCreateLtmMonitor+=MonitorDefaultFrom
                if HealthMonitorInterval != None:
                    MonitorInterval = ' interval ' + HealthMonitorInterval
                    InitCreateLtmMonitor+=MonitorInterval
                if HealthMonitorRecv != None:
                    if HealthMonitorRecv.find('\\') != -1:
                        HealthMonitorRecv=HealthMonitorRecv.replace('\\', '\\\\')
                    MonitorRecv=' recv ' + HealthMonitorRecv
                    InitCreateLtmMonitor+=MonitorRecv
                if HealthMonitorSend != None:
                    MonitorSend=' send ' + HealthMonitorSend
                    InitCreateLtmMonitor+=MonitorSend
                if HealthMonitorTimeUntilup != None:
                    MonitorTimeUntilUp=' time-until-up ' + HealthMonitorTimeUntilup
                    InitCreateLtmMonitor+=MonitorTimeUntilUp
                if HealthMonitorTimeOut != None:
                    MonitorTimeOut=' timeout ' + HealthMonitorTimeOut
                    InitCreateLtmMonitor+=MonitorTimeOut

                '''
                if HealthMonitorSend == None or HealthMonitorRecv == None:
                    raise AttributeError('Send and Recv Should Not Be NoneType')
                else:
                    CreateLtmMonitorCommand = 'tmsh create ltm monitor ' + HealthMonitorType + ' ' + HealthMonitorName + ' send ' + HealthMonitorSend + ' recv ' + HealthMonitorRecv + ' destination ' + HealthMonitorDest
                '''
        return InitCreateLtmMonitor

####create ltm pool command
    def SetCreateLtmPoolCommandV11(self, **kwargs):

        RealServerList = kwargs.get('LtmPoolMembers')
        ####PoolMemberPort = kwargs.get('Port')
        LtmPoolName = kwargs.get('LtmPoolName', None)
        LtmPoolMinActive=kwargs.get('LtmPoolMinActive', None)
        LtmPoolMonitor = kwargs.get('LtmPoolMonitor', None)
        LtmPoolSlow=kwargs.get('LtmPoolSlow', None)
        LtmPoolLBM=kwargs.get('LtmPoolLBM', None)

        RealSeverListStr = ''

        InitCreateLtmPool='tmsh create ltm pool '
        if LtmPoolName == None:
            raise  NameError('LtmPoolName should Not be None')
        else:
            InitCreateLtmPool+=LtmPoolName
            if isinstance(RealServerList, list):
                for values in RealServerList:
                    OnePoolMember = ' ' + values
                    RealSeverListStr+=OnePoolMember

                MemberStr=' members add {' + RealSeverListStr + '}'
                InitCreateLtmPool+=MemberStr
            else:
                ####raise AttributeError('LtmPoolMembersList must be a List and PoolMemberPort should not be None')
                pass

            if LtmPoolMinActive != None:
                MinActiveStr=' min-active-members ' + LtmPoolMinActive
                InitCreateLtmPool+=MinActiveStr
            if LtmPoolMonitor != None:
                MonitorStr=' monitor ' + LtmPoolMonitor
                InitCreateLtmPool+=MonitorStr
            if LtmPoolSlow != None:
                SlowStr=' slow-ramp-time ' + LtmPoolSlow
                InitCreateLtmPool+=SlowStr
            if LtmPoolLBM != None:
                LBMStr=' load-balancing-mode ' + LtmPoolLBM
                InitCreateLtmPool+=LBMStr


        return InitCreateLtmPool

####create Vs command
    def SetCreateLtmVsCommandV11(self, **kwargs):
        InitCreateLtmVsStr = 'tmsh create ltm virtual'

        LtmVirtualServerName = kwargs.get('name')
        LtmVirtualServerDest = kwargs.get('dest')
        LtmVirtualServerMask=kwargs.get('mask')
        LtmVirtualServerConnectionLimit=kwargs.get('connectionlimit')
        LtmVirtualServerPersist = kwargs.get('persist')
        LtmVirtualServerPool = kwargs.get('pool')
        LtmVirtualServerProfiles = kwargs.get('profiles')
        LtmVirtualServerRules = kwargs.get('rules')
        LtmVirtualServerSource=kwargs.get('source')
        LtmVirtualServerIpProtocol = kwargs.get('protocol')
        LtmVirtualServerTransAdd=kwargs.get('transAdd')
        LtmVirtualServerTransPort=kwargs.get('transPort')
        LtmVirtualServerVlanEnable=kwargs.get('vlanEnable')
        LtmVirtualServerVlans=kwargs.get('vlans')
        LtmVirtualServerSnatPool=kwargs.get('snatPool')
        LtmVirtualServerSnatType=kwargs.get('snatType')

        ####11.2.1httpclass
        LtmVirtualServerHttpClass = kwargs.get('httpclass')

        if LtmVirtualServerName != None:
            LtmVirtualServerName = ' ' + LtmVirtualServerName
            InitCreateLtmVsStr += LtmVirtualServerName
        else:
            raise NameError('Virtual ServerName Must Be Define')

        if LtmVirtualServerDest != None:
            LtmVirtualServerDest = ' destination ' + LtmVirtualServerDest
            InitCreateLtmVsStr += LtmVirtualServerDest
        else:
            # print LtmVirtualServerName
            raise AttributeError('Virtual Server Dest Must Be Define')

        if LtmVirtualServerMask != None:
            LtmVirtualServerMask=' mask ' + LtmVirtualServerMask
            InitCreateLtmVsStr+=LtmVirtualServerMask

        if LtmVirtualServerConnectionLimit != None:
            LtmVirtualServerConnectionLimit=' connection-limit ' + LtmVirtualServerConnectionLimit
            InitCreateLtmVsStr+=LtmVirtualServerConnectionLimit

        if LtmVirtualServerPool != None:
            LtmVirtualServerPool = ' pool ' + LtmVirtualServerPool
            InitCreateLtmVsStr += LtmVirtualServerPool

        LtmVirtualServerPersistStr = ''
        if LtmVirtualServerPersist != None:
            for value in LtmVirtualServerPersist:
                OnePersist = ' ' + value
                LtmVirtualServerPersistStr += OnePersist

            LtmVirtualServerPersist = ' persist replace-all-with {' + LtmVirtualServerPersistStr + ' }'
            InitCreateLtmVsStr += LtmVirtualServerPersist

        if LtmVirtualServerIpProtocol != None:
            LtmVirtualServerIpProtocol = ' ip-protocol ' + LtmVirtualServerIpProtocol
            InitCreateLtmVsStr += LtmVirtualServerIpProtocol

        LtmVirtualServerProfilesStr=''
        if LtmVirtualServerProfiles != None:
            '''
            LtmVirtualServerProfiles = ' profiles add { ' + LtmVirtualServerProfiles + ' }'
            InitCreateLtmVsStr += LtmVirtualServerProfiles
            '''
            for value in LtmVirtualServerProfiles:
                OneProfile=' ' + value
                LtmVirtualServerProfilesStr += OneProfile

            LtmVirtualServerProfiles = ' profiles replace-all-with {' + LtmVirtualServerProfilesStr + ' }'
            InitCreateLtmVsStr+=LtmVirtualServerProfiles

        LtmVirtualServerRulesStr=''
        if LtmVirtualServerRules != None:
            for value in LtmVirtualServerRules:
                OneRule=' ' + value
                LtmVirtualServerRulesStr+=OneRule

            LtmVirtualServerRules = ' rules {' + LtmVirtualServerRulesStr + ' }'
            InitCreateLtmVsStr+=LtmVirtualServerRules


        if LtmVirtualServerSource != None:
            LtmVirtualServerSource=' source ' + LtmVirtualServerSource
            InitCreateLtmVsStr+=LtmVirtualServerSource

        if LtmVirtualServerSnatPool != None or LtmVirtualServerSnatType != None:
            LtmVirtualServerSnatStrInside=''
            if LtmVirtualServerSnatPool != None:
                LtmVirtualServerSnatStrInsidePool=' pool ' + LtmVirtualServerSnatPool + ' '
            if LtmVirtualServerSnatType != None:
                LtmVirtualServerSnatStrInsideType=' type ' + LtmVirtualServerSnatType + ''

            LtmVirtualServerSnatStrInside=LtmVirtualServerSnatStrInsidePool + LtmVirtualServerSnatStrInsideType
            LtmVirtualServerSnat=' source-address-translation {' + LtmVirtualServerSnatStrInside + ' }'
            InitCreateLtmVsStr+=LtmVirtualServerSnat

        if LtmVirtualServerTransAdd != None:
            LtmVirtualServerTransAdd=' translate-address ' + LtmVirtualServerTransAdd
            InitCreateLtmVsStr+=LtmVirtualServerTransAdd

        if LtmVirtualServerTransPort != None:
            LtmVirtualServerTransPort=' translate-port ' + LtmVirtualServerTransPort
            InitCreateLtmVsStr+=LtmVirtualServerTransPort

        if LtmVirtualServerVlanEnable != None and LtmVirtualServerVlanEnable == 'vlans-enabled':
            InitCreateLtmVsStr+=' vlans-enabled'

        LtmVirtualServerVlansStr=''
        if LtmVirtualServerVlans != None:
            for value in LtmVirtualServerVlans:
                OneVlan=' ' + value
                LtmVirtualServerVlansStr+=OneVlan

            LtmVirtualServerVlans=' vlans replace-all-with {' + LtmVirtualServerVlansStr + ' }'
            InitCreateLtmVsStr+=LtmVirtualServerVlans

        ####11.2.1httpclass
        if LtmVirtualServerHttpClass != None:
            LtmVirtualServerHttpClass = ' http-class { ' + LtmVirtualServerHttpClass + ' }'
            InitCreateLtmVsStr += LtmVirtualServerHttpClass

        CreateLtmVirtualCommandV11 = InitCreateLtmVsStr

        return  CreateLtmVirtualCommandV11

####modify ltm virtual httpclass
    def SetModifyLtmVsHttpClassV11(self, Vs, HttpClass):
        return 'tmsh modify ltm virtual ' + Vs + ' http-class { ' + HttpClass + ' }'

####vs+_http
    def SetVsPlusHttp(self, Vs):
        return Vs + '_http'
####vs+ https
    def SetVsPlusHttps(self, Vs):
        return Vs + '_https'
####is Vs exist
    def IsVsExist(self, Vs, VsSet):
        Vs = Vs + '-name'
        return VsSet.has_key(Vs)
####is http class right?
    def IsHttpClassFit(self, HttpClass, HttpClassToFit):
        return HttpClass == HttpClassToFit



####create policy,the version must be later then 11.4.0
    def SetCreateVsPolicyV1161(self, **kwargs):
         InitCreateLtmVsPolicyStr = 'tmsh create ltm policy'
         LtmVsPolicyName = kwargs.get('name')
         LtmVsStrategy = kwargs.get('strategy')
         LtmVsRequires = kwargs.get('requires')
         LtmVsControls = kwargs.get('controls')

         if LtmVsPolicyName != None:
             LtmVsPolicyName = ' ' + LtmVsPolicyName
             InitCreateLtmVsPolicyStr += LtmVsPolicyName

         if LtmVsStrategy != None:
             LtmVsStrategy = ' strategy ' + LtmVsStrategy
             InitCreateLtmVsPolicyStr += LtmVsStrategy

         if LtmVsRequires != None:
             LtmVsRequires = ' requires add { ' + LtmVsRequires + ' }'
             InitCreateLtmVsPolicyStr += LtmVsRequires

         if LtmVsControls != None:
             LtmVsControls = ' controls add { ' + LtmVsControls + ' }'
             InitCreateLtmVsPolicyStr += LtmVsControls


         return  InitCreateLtmVsPolicyStr
####rule
    def SetModifyVsPolicyV1161(self, **kwargs):
        PolicyName = kwargs.get('PolicyName')
        defualt_rule = kwargs.get('defualt_rule')
        rules = kwargs.get('rules')

        InitModifyLtmPolicyStr = 'tmsh modify ltm policy'

        if PolicyName != None:
            PolicyName = ' ' + PolicyName
            InitModifyLtmPolicyStr += PolicyName
        else:
            pass

        if defualt_rule != None:
            defualt_rule = 'defualt-rule-asm { conditions none actions add { 0 { asm disable policy Default_ASM_Policy } } ordinal 1 }'
            defualt_rule_str = ' rules add { ' + defualt_rule + ' }'
            InitModifyLtmPolicyStr += defualt_rule_str
            return  InitModifyLtmPolicyStr
        else:
            pass

        if rules != None:
            rules_str = ' rules add { ' + rules + '}'
            InitModifyLtmPolicyStr+=rules_str
            return InitModifyLtmPolicyStr

####rule details
    def RuleDetails(self, **kwargs):
        rule_name = kwargs.get('rule_name')
        conditions = kwargs.get('conditions')
        actions = kwargs.get('actions')
        ordinal = kwargs.get('ordinal')

        RuleInitStr = rule_name + ' { '

        if conditions != None:
            conditions_str = 'conditions add {' + conditions + '}'
            RuleInitStr += conditions_str

        if actions != None:
            actions_str = ' actions add {' + actions + '}'
            RuleInitStr += actions_str

        if ordinal != None:
            ordinal_str =  ' ordinal ' + str(ordinal) + ' } '
            RuleInitStr += ordinal_str

        return RuleInitStr

####rule condition
    def RuleCondition(self, **kwargs):
        ConditionsList = kwargs.get('ConditionsList')

        ConditionsList_str = ''
        for condition in ConditionsList:
            ConditionsList_str += condition

        return  ConditionsList_str

####rule actions
    def RuleActions(self, **kwargs):
        ActionsList = kwargs.get('ActionsList')

        ActionsList_str = ''
        for actions in ActionsList:
            ActionsList_str += actions

        return  ActionsList_str

####link policy with vs
    def ModifyAddPolicyToVs(self, **kwargs):
        Vs_Name = kwargs.get('Vs_Name')
        Asm_Need = kwargs.get('Asm_Need')
        policies = kwargs.get('policies')

        InitStr = 'tmsh modify ltm virtual '

        if Vs_Name != None:
            InitStr = InitStr + Vs_Name + ' '
            if Asm_Need == True:
                InitStr = InitStr + ' profiles add { websecurity } policies add { ' + policies + ' }'
            else:
                InitStr = InitStr + 'policies add { ' + policies + ' }'

        return InitStr















