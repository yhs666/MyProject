#!/usr/bin/env python
#coding:utf-8
'''
Created on Jan 9, 2016

@author: yang.hongsheng
'''
#!/usr/bin/env python
#coding:utf-8
'''
Created on 2016��1��9��

@author:yang.hongsheng 
'''

import cPickle 
import redis
import time
import logging
import sys,os
import hashlib
import threading
import getpass

ip ="waps-20"
password = "www.wasu.com"
time_out = 60
local_thread = threading.local()
FILE=os.getcwd()
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s:%(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename = os.path.join(FILE,'log.txt'),
                    filemode='w')
try:
    myredis = redis.Redis(host=ip,password=password,port = 6379)
    print "Connect Redis OK!"
    logging.info('Connect Redis OK!')

except:
    print "Redis connect issue!"
    logging.info('Redis connect issue!')
    sys.exit()



def user_cmd(username,key):
    r = username + ":" +key
    return r 

def user_get(username):
    a = [user_cmd(username, "cmds"),user_cmd(username, "status")]
    return a


def set_to_redis(cmd_str):
    
    try:

        key1 = user_name +":cmd" 
        key2 = user_name +":status" 
        key3 = user_name + ":time"
        myredis.mset({key2:"submit", key3:time.ctime(), key1:cmd_str})
        
        msg = "  Commands: %s   Status: %s " % (cmd_str,"submit")
        logging.info(msg)
        return True
    except:
        msg = "  Commands: %s   Status: %s " % (cmd_str,"issue!")
        logging.info(msg)
        return False

 

cluster = [
    "BJBPrdApp01",
    "BJBPrdApp02",
    "BJBPrdApp03",
    "BJBPrdApp04",
    "BJBPrdApp05",
    "SH2PrdApp01",
    "SH2PrdApp02",
    "SHAPrdApp01",
    "SHAPrdApp02",
    "SH3PrdApp01",
    "SH3PrdApp02",
    "BJBPrdDDC01",
    "BJBPrdDDC02",
    "BJBPrdPFCC01",
    "BJBPrdStr01",
    "BJBPrdStr02",
    "SH2PrdPFCC01",
    "SH2PrdStr01",
    "SHAPrdDDC01",
    "SHAPrdPFCC01",
    "SHAPrdStr01",
    "SH3PrdDDC01",
    "SH3PrdPFCC01",
    "SH3PrdStp01",

    ]

cmd_list =[
           "GetAclConfigurationForInterface",
            "GetAllMachinePoolsContainerPolicy",
            "GetAllNetworkAllocationHeaders",
            "GetAllReservedVips",
            "GetAllReservedVipsFromNM",
            "GetAppConfigSettings",
            "GetAssignedReservedVipsForNextTenantUpdate",
            "GetBladeDetails",
            "GetBladeFaultDetails",
            "GetBladeInfo",
            "GetBuildVersion",
            "GetCertificatesOfImage",
            "GetClouds",
            "GetClusterPrimary",
            "GetClusterReplicas",
            "GetClusterUtilization",
            "GetClusterVipRanges",
            "GetComponentHealth",
            "GetComputeUtilization",
            "GetConfig",
            "GetContainerConfiguration",
            "GetContainerDetails",
            "GetContainerIdFromMac",
            "GetContainerNode",
            "GetContainerRecoveryStatus",
            "GetContainersPendingNetworkRelease",
            "GetContainerStates",
            "GetContainerUserAccounts",
            "GetCurrentAddOperationsContext",
            "GetCurrentBackupContainerUri",
            "GetCurrentBackupRestoreStatus",
            "GetCurrentFabricComponentVersion",
            "GetCurrentHostingEnvironment",
            "GetCurrentImageOperationsContext",
            "GetCurrentlyUpdatingHudsAndNodes",
            "GetCustomServiceThrottlingSettings",
            "GetDeletedImageList",
            "GetDeviceInfo",
            "GetDhcpInfo",
            "GetDirectoryServiceConfiguration",
            "GetDripRanges",
            "GetEffectiveRouteTable",
            "GetEntireConfiguration",
            "GetEntireInventory",
            "GetEntireMacToIp",
            "GetExpectedNetworkManagerVersionNumber",
            "GetFabricWorkEvents",
            "GetFaultDomain",
            "GetFaultManagerNodesInRecovery",
            "GetFaultManagerNodesWithPredictedFaults",
            "GetFaultManagerStatus",
            "GetFile",
            "GetGuestAgentVersionImageName",
            "GetGuestAgentVersions",
            "GetHostPluginExecutionStatus",
            "GetIaaSRootUpdateDeploymentInfo",
            "GetIdentitiesInSecurityRole",
            "GetIdentityNamespaces",
            "GetImageCount",
            "GetImageData",
            "GetImageID",
            "GetImageInventory",
            "GetImageList",
            "GetImageMeta",
            "GetImagesBelowReplicationLevel",
            "GetImagesBlockingHealthMonitor",
            "GetImageUrls",
            "GetInstanceReport",
            "GetInternalModel",
            "GetInventory",
            "GetIRBackupSettings",
            "GetIROperatingModeOverride",
            "GetJobEvents",
            "GetJobWaitEvents",
            "GetLatestCheckpoint",
            "GetLBSettingsForVip",
            "GetLeaseRequestsInProgress",
            "GetLeasesInfosBlockingContainerDestruction",
            "GetLEDState",
            "GetLoadBalancerSets",
            "GetLocation",
            "GetMacAddressInventory",
            "GetMacFromPort",
            "GetMachinePoolDetails",
            "GetMachinePoolUtilization",
            "GetMaxUpdateDomain",
            "GetMeteringConfigData",
            "GetMissingImageList",
            "GetMissingVirtualNetworks",
            "GetMonitoredComponentStatus",
            "GetMonitoringFile",
            "GetMRTenantPolicy",
            "GetNetworkAllocationDataById",
            "GetNetworkAllocationsToBeReconciled",
            "GetNetworkAllocationSummary",
            "GetNetworkingStateForNode",
            "GetNmSetting",
            "GetNodeByIP",
            "GetNodeCert",
            "GetNodeContainers",
            "GetNodeCurrentOs",
            "GetNodeEntityHealthDetails",
            "GetNodeEvents",
            "GetNodeFaultRecoveryHistory",
            "GetNodeHealthState",
            "GetNodeImageList",
            "GetNodeInternals",
            "GetNodeIpAddress",
            "GetNodeMeteringInNm",
            "GetNodeMeteringTierInfo",
            "GetNodePredictedFaultHistory",
            "GetNodeProgrammingState",
            "GetNodeProtectionStatus",
            "GetNodeRoles",
            "GetNodes",
            "GetNodesByAllocationType",
            "GetNodesInAvailabilityState",
            "GetNodesInDomain",
            "GetNodesInFaultDomain",
            "GetNodesInMachinePool",
            "GetNodesNotInStableGoalState",
            "GetNodesOutOfGoalState",
            "GetNodesRequiringRootHEUpdate",
            "GetNodeState",
            "GetNodeStatus",
            "GetNodeUpdateDomain",
            "GetNodeUtilizationDetails",
            "GetNodeVariableHbInfo",
            "GetNodeWDSSessions",
            "GetOperationsPolicy",
            "GetOriginalF5ApplianceIdOwningVip",
            "GetOSVersionImageName",
            "GetOSVersions",
            "GetPDUConnections",
            "GetPendingApprovalsDocument",
            "GetPendingDripSettings",
            "GetPhysicalInventoryVersion",
            "GetPortFromMac",
            "GetPowerState",
            "GetPrimaryUpTime",
            "GetQOSConfigurationForInterface",
            "GetRepository",
            "GetRequestStatus",
            "GetReservedVips",
            "GetRoleConfig",
            "GetRoleInstanceContainerDeploymentProgressInfo",
            "GetRoleInstanceContainerProvisioningDetails",
            "GetRoleInstanceDetails",
            "GetRoleInstanceLeaseInfoByTenant",
            "GetRoleInstanceLeaseInfos",
            "GetRoleInstanceNetworkConfiguration",
            "GetRoleInstances",
            "GetRoleInstanceUpdateActions",
            "GetRoleList",
            "GetRoleLocation",
            "GetRoleSnatVipConfiguration",
            "GetRolloutVersionInfo",
            "GetRootHEConflictingNodes",
            "GetRootHENotification",
            "GetRootHEUpdateProgressInfo",
            "GetRootHEUpdateSetNodes",
            "GetRootHEUpdateSetTenants",
            "GetRouteConfigurationForInterface",
            "GetRouterSets",
            "GetRoutesConfiguration",
            "GetScheduledStateChanges",
            "GetScheduledStateChangesByType",
            "GetSecurityRolesForIdentity",
            "GetServiceHealingStatus",
            "GetServiceInstances",
            "GetServiceNameFromInstance",
            "GetServiceNames",
            "GetServiceRoles",
            "GetSetting",
            "GetSlaManagerDocument",
            "GetSlbInformation",
            "GetSlbPendingTasks",
            "GetStaticRoleMap",
            "GetSubnetAllocations",
            "GetSupportedTestPoints",
            "GetSupportedTestSuites",
            "GetTenantAccountGroup",
            "GetTenantAllocationInfo",
            "GetTenantAllocationMap",
            "GetTenantAllowedTraits",
            "GetTenantArtifacts",
            "GetTenantByVIP",
            "GetTenantCert",
            "GetTenantContainers",
            "GetTenantDeploymentProgress",
            "GetTenantDetails",
            "GetTenantDripSettings",
            "GetTenantEvents",
            "GetTenantGenerationDeploymentProgress",
            "GetTenantGenerations",
            "GetTenantHealthStatus",
            "GetTenantHEInfo",
            "GetTenantIDnsSuffix",
            "GetTenantInfo",
            "GetTenantInitiatedFshThrottlingRate",
            "GetTenantJobs",
            "GetTenantJobStatus",
            "GetTenantLBSettings",
            "GetTenantNetworkAllocationData",
            "GetTenantNodes",
            "GetTenantNodesInUpdateDomain",
            "GetTenantPolicyAgentDocument",
            "GetTenantPolicyAgentStatus",
            "GetTenantPolicySettings",
            "GetTenantProperty",
            "GetTenantProtectionStatus",
            "GetTenantPublicIP",
            "GetTenantResourceAllocationStatus",
            "GetTenants",
            "GetTenantServiceInstances",
            "GetTenantServices",
            "GetTenantSettingOverrideValue",
            "GetTenantStatus",
            "GetTenantSummary",
            "GetTenantsWithNetworkFault",
            "GetTenantsWithProperties",
            "GetTenantsWithUnReconciledNetworkAllocation",
            "GetTenantTargetFDs",
            "GetTenantTargetMachinePools",
            "GetTenantTimeoutDetails",
            "GetTenantTraits",
            "GetTenantUDWalkBlockInfo",
            "GetTenantUpdateDomain",
            "GetTenantUpdateDomainState",
            "GetTenantVips",
            "GetTenantVirtualNetwork",
            "GetTIMOperations",
            "GetTMAllocationPolicy",
            "GetTMClusterAllocationCapabilities",
            "GetUnusedImages",
            "GetValidDomains",
            "GetVersion",
            "GetVfpFiltersForContainer",
            "GetVipLBSettings",
            "GetVipProgrammingTask",
            "GetVipStatus",
            "GetVipSwapOperationDetails",
            "GetVipSwapTasksForOperation",
            "GetVirtualNetworkSnapshot",
            "GetVirtualNetworkVersionInfo",
            "GetVnetAddressMappingForCAFromNmAgent",
            "GetVNetUtilization",
            "GetVolatileSetting",
            "ListAllLBSettings",
            "ListBackups",
            "ListBladeDetailByLabel",
            "ListBladeFaultDetails",
            "ListBladeInfoByProperty",
            "ListDevicesByType",
            "ListFaultedContainers",
            "ListHumanInvestigateDetails",
            "ListNodeCerts",
            "ListRepositories",
            "ListRMADetails",
            "ListTenantCerts",
            "ListTenantManagedCertificates",
            "ListTenantSecrets",
            "ListTenantSecretsById",
            "ListTenantSecretsInUse",
            "ListVirtualNetworks",
            "ListVirtualNetworksRegional",
            "ListVirtualNetworkTenants",
            "ListVirtualNetworkVersionInfo",
            "ListVNetsPendingMigration",

           
           
           ]
        
from  autopy import alert
user_name = getpass.getuser()
print user_name
while True:
    cmds = raw_input("Please input FC commands:")
    print cmds
    cmds =cmds.strip().strip(';')
    cmds_list = cmds.split()
    
    cl = ','.join(cluster).lower()
    if len(cmds) > 26 and len(cmds_list) >=3 and len(cmds_list) <=8  and  cmds_list[1].split(':')[1].lower()  in cl:
        print cmds

    else:
        cmds_list = cmds.split()
        alert.alert("Input command have issue","Alert")
        continue
    
    
#     if set_to_redis(cmds):
#         pass
#     else:
#         
#         msg = "set to redisk issue : %s " % cmds
#         logging.info(msg)
#         print msg
#             
#     print "--------------Done---------------"
#     time.sleep(1)
    
  
    
myredis.bgrewriteaof()

print "RUn over!"        

