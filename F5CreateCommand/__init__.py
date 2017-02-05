#!/usr/bin/env python
# -*- coding: utf8 -*-

from CreateLtmCommandV11 import *
__author__ = 'stttt2003pk'

CreateLtmMonitorV11 = CreateLtmCommandV11().SetCreateHealthMonitorCommandV11
CreateLtmPoolV11 = CreateLtmCommandV11().SetCreateLtmPoolCommandV11
CreateLtmVirtualV11 = CreateLtmCommandV11().SetCreateLtmVsCommandV11

CreateVsHttpV11 = CreateLtmCommandV11().SetVsPlusHttp
CreateVsHttpsV11 = CreateLtmCommandV11().SetVsPlusHttps

ModifyVsHttpClassV11 = CreateLtmCommandV11().SetModifyLtmVsHttpClassV11

IsVsExist = CreateLtmCommandV11().IsVsExist
IsHttpClassFit = CreateLtmCommandV11().IsHttpClassFit

CreateLtmPolicyV1161 = CreateLtmCommandV11().SetCreateVsPolicyV1161
ModifyLtmPolicyV1161 = CreateLtmCommandV11().SetModifyVsPolicyV1161