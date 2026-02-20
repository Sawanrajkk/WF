"""
///////////////////////////////////////////////////////////
/** @file: test_email_v1.py
 *  (C) Copyright  2023 HP Development Company, L.P.
 */
///////////////////////////////////////////////////////////
"""
import sys
import pytest
import time
import json
import logging
from dunetuf.cdm.CdmTestUtils import CdmTestUtils

def check_endpoint(cdm, endpoint):
    # Check the endpoint is supported and discoverable
    servicesDiscovery = cdm.get(cdm.SERVICES_DISCOVERY)
    for service in servicesDiscovery["services"]:
        if service["serviceGun"] == "com.hp.cdm.service.email.version.1" :
            link_found = False
            for link in service["links"]:
                print(json.dumps(link, indent=4))
                if link["href"] == endpoint:
                    link_found = True
                    break
            if not link_found:
                print(endpoint + " - is not supported and discoverable")
                return False
    return True

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test CDM
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-180031
    +timeout:120
    +asset: Send
    +delivery_team:WalkupApps
    +feature_team:SendSolns
    +test_framework: TUF
    +name: test_email_pubsub_resources
    +test :
        +title: test_email_pubsub_resources
        +guid: 14b639e0-1610-49a6-8b93-0f45258c8ab4
        +dut:
            +type: Simulator
            +configuration: WebServices=CDM & CloudSolution=Telemetry & DeviceFunction=DigitalSend & ScanDestination=Email
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_email_pubsub_resources(cdm):
    cdmUtil = CdmTestUtils()
    cdmUtil.set_cdm(cdm)
    print( "--------------------------------------------------------" )
    ENDPOINT_PUBSUB = "cdm/pubsub/v2/subscriptions"
    ENDPOINT_PUBSUB_ONDEMAND = "cdm/pubsub/v2/desires"
    pubsubClientId = "email_test"
    cdmUtil.deleteSubscriptions(pubsubClientId)
    pubsubClientInstanceId = "smtpServers"
    print("----- Check for PubSub " + "com.hp.cdm.service.email.version.1.smtpServers" +"-----")
    resource = {
        "version": "2.3.0",
        "clientId" : "test",
        "clientInstanceId" : "instanceId_test1",
        "resources" : [
            { "gun" : "com.hp.cdm.service.email.version.1.resource.smtpServers"}
        ],
        "callbackUri" : "http://15.77.21.145:8080"
    }
    resource["clientId"] = pubsubClientId
    resource["clientInstanceId"] = pubsubClientInstanceId
    print(resource)
    headers = {}
    timeout = 4.0
    r = cdm.post_raw(ENDPOINT_PUBSUB,resource, headers=headers, scope_alias=cdm.ScopeAlias.HP_CLOUD_SERVICE,timeout=timeout)
    print(r.status_code)
    assert (r.status_code == 201)
    if r.status_code == 201 :
        print(r.headers)
        print(r.headers["location"])
        print(r.json())
        subscriptionId = r.json()["subscriptionId"]
        print("subscriptionId: " + subscriptionId)
        print("clientId: " + pubsubClientId)
        ENDPOINT_NODE1 = r.headers["location"]
        print(ENDPOINT_NODE1)
        if(ENDPOINT_NODE1 != None ):
            ENDPOINT_NODE_AGG1 =  ENDPOINT_NODE1 + "/aggregate"
            ENDPOINT_NODE_EV1 =  ENDPOINT_NODE1 + "/events"
            r = cdm.get_raw(ENDPOINT_NODE1, headers=headers, scope_alias=cdm.ScopeAlias.HP_CLOUD_SERVICE, timeout=timeout)
            print( "----------------------  get  --------------" )
            print(r)
            print(r.status_code)
            print(r.headers["etag"])
            r = cdm.get_raw(ENDPOINT_NODE_EV1, headers=headers, scope_alias=cdm.ScopeAlias.HP_CLOUD_SERVICE,timeout=timeout)
            print( "------------- intial events --------------" )
            print(r)
            print(r.json())
            print( "------------------------------------------" )
            r = cdm.get_raw(ENDPOINT_NODE_AGG1, headers=headers, scope_alias=cdm.ScopeAlias.HP_CLOUD_SERVICE,timeout=timeout)
            print( "----------------get aggregate ------------" )
            print(r)
            print(r.json())
            print( "------------------------------------------" )
    pubsubClientInstanceId = "defaultSmtpServers"
    print("----- Check for PubSub " + "com.hp.cdm.service.email.version.1.defaultSmtpServers" +"-----")
    resource = {
        "version": "2.3.0",
        "clientId" : "test",
        "clientInstanceId" : "instanceId_test1",
        "resources" : [
            { "gun" : "com.hp.cdm.service.email.version.1.resource.defaultSmtpServers"}
        ],
        "callbackUri" : "http://15.77.21.145:8080"
    }
    resource["clientId"] = pubsubClientId
    resource["clientInstanceId"] = pubsubClientInstanceId
    print(resource)
    headers = {}
    timeout = 4.0
    r = cdm.post_raw(ENDPOINT_PUBSUB,resource, headers=headers, scope_alias=cdm.ScopeAlias.HP_CLOUD_SERVICE,timeout=timeout)
    print(r.status_code)
    assert (r.status_code == 201)
    if r.status_code == 201 :
        print(r.headers)
        print(r.headers["location"])
        print(r.json())
        subscriptionId = r.json()["subscriptionId"]
        print("subscriptionId: " + subscriptionId)
        print("clientId: " + pubsubClientId)
        ENDPOINT_NODE1 = r.headers["location"]
        print(ENDPOINT_NODE1)
        if(ENDPOINT_NODE1 != None ):
            ENDPOINT_NODE_AGG1 =  ENDPOINT_NODE1 + "/aggregate"
            ENDPOINT_NODE_EV1 =  ENDPOINT_NODE1 + "/events"
            r = cdm.get_raw(ENDPOINT_NODE1, headers=headers, scope_alias=cdm.ScopeAlias.HP_CLOUD_SERVICE, timeout=timeout)
            print( "----------------------  get  --------------" )
            print(r)
            print(r.status_code)
            print(r.headers["etag"])
            r = cdm.get_raw(ENDPOINT_NODE_EV1, headers=headers, scope_alias=cdm.ScopeAlias.HP_CLOUD_SERVICE,timeout=timeout)
            print( "------------- intial events --------------" )
            print(r)
            print(r.json())
            print( "------------------------------------------" )
            r = cdm.get_raw(ENDPOINT_NODE_AGG1, headers=headers, scope_alias=cdm.ScopeAlias.HP_CLOUD_SERVICE,timeout=timeout)
            print( "----------------get aggregate ------------" )
            print(r)
            print(r.json())
            print( "------------------------------------------" )
    pubsubClientInstanceId = "constraints"
    pubsubClientInstanceId = "verifyAccess"
    pubsubClientInstanceId = "verifyAccessConstraints"
    pubsubClientInstanceId = "capabilities"
    pubsubClientInstanceId = "validatePinConstraints"
    pubsubClientInstanceId = "validatePin"
    pubsubClientInstanceId = "allowedEmailDomainsConstraints"
    pubsubClientInstanceId = "allowedEmailDomains"
    print("----- Check for PubSub " + "com.hp.cdm.service.email.version.1.allowedEmailDomains" +"-----")
    resource = {
        "version": "2.3.0",
        "clientId" : "test",
        "clientInstanceId" : "instanceId_test1",
        "resources" : [
            { "gun" : "com.hp.cdm.service.email.version.1.resource.allowedEmailDomains"}
        ],
        "callbackUri" : "http://15.77.21.145:8080"
    }
    resource["clientId"] = pubsubClientId
    resource["clientInstanceId"] = pubsubClientInstanceId
    print(resource)
    headers = {}
    ENDPOINT= "cdm/email/v1/allowedEmailDomains"
    # Check the endpoint is supported and discoverable
    if not check_endpoint(cdm, ENDPOINT):
        return

    timeout = 4.0
    r = cdm.post_raw(ENDPOINT_PUBSUB,resource, headers=headers, scope_alias=cdm.ScopeAlias.HP_CLOUD_SERVICE,timeout=timeout)
    print(r.status_code)
    assert (r.status_code == 201)
    if r.status_code == 201 :
        print(r.headers)
        print(r.headers["location"])
        print(r.json())
        subscriptionId = r.json()["subscriptionId"]
        print("subscriptionId: " + subscriptionId)
        print("clientId: " + pubsubClientId)
        ENDPOINT_NODE1 = r.headers["location"]
        print(ENDPOINT_NODE1)
        if(ENDPOINT_NODE1 != None ):
            ENDPOINT_NODE_AGG1 =  ENDPOINT_NODE1 + "/aggregate"
            ENDPOINT_NODE_EV1 =  ENDPOINT_NODE1 + "/events"
            r = cdm.get_raw(ENDPOINT_NODE1, headers=headers, scope_alias=cdm.ScopeAlias.HP_CLOUD_SERVICE, timeout=timeout)
            print( "----------------------  get  --------------" )
            print(r)
            print(r.status_code)
            print(r.headers["etag"])
            r = cdm.get_raw(ENDPOINT_NODE_EV1, headers=headers, scope_alias=cdm.ScopeAlias.HP_CLOUD_SERVICE,timeout=timeout)
            print( "------------- intial events --------------" )
            print(r)
            print(r.json())
            print( "------------------------------------------" )
            r = cdm.get_raw(ENDPOINT_NODE_AGG1, headers=headers, scope_alias=cdm.ScopeAlias.HP_CLOUD_SERVICE,timeout=timeout)
            print( "----------------get aggregate ------------" )
            print(r)
            print(r.json())
            print( "------------------------------------------" )
    pubsubClientInstanceId = "smtpAutoFind"
    cdmUtil.deleteSubscriptions(pubsubClientId)
    print( "----------------------------------------------------" )
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test CDM
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-180031
    +timeout:120
    +asset: Send
    +delivery_team:WalkupApps
    +feature_team:SendSolns
    +test_framework: TUF
    +name: test_email_non_pubsub_resources
    +test :
        +title: test_email_non_pubsub_resources
        +guid: 4897b85b-5ded-4231-86d0-fb7880de7445
        +dut:
            +type: Simulator
            +configuration: WebServices=CDM & CloudSolution=Telemetry & DeviceFunction=DigitalSend & ScanDestination=Email
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_email_non_pubsub_resources(cdm):
    cdmUtil = CdmTestUtils()
    cdmUtil.set_cdm(cdm)
    print( "-----------------------------------------------------------" )
    ENDPOINT_PUBSUB = "cdm/pubsub/v2/subscriptions"
    ENDPOINT_PUBSUB_ONDEMAND = "cdm/pubsub/v2/desires"
    pubsubClientId = "email_test"
    cdmUtil.deleteSubscriptions(pubsubClientId)
    pubsubClientInstanceId = "smtpServers"
    pubsubClientInstanceId = "defaultSmtpServers"
    pubsubClientInstanceId = "constraints"
    print("----- PubSub not supported for this resource " + "com.hp.cdm.service.email.version.1.constraints" +"-----")
    print("----- Check ondemand desire --------")
    expected_status = 204
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.email.version.1","cdm/email/v1/smtpServers/constraints","GET")
    print(claimScopes)
    if len(claimScopes) > 0: 
        if "com.hp.cdm.auth.alias.deviceRole.hpCloudService" not in claimScopes and "com.hp.cdm.auth.alias.deviceRole.public" not in claimScopes: 
            expected_status = 400
    resource = {
        "version": "2.3.0",
        "desires": [
        {
            "onDemand" : {
            "clientId" : "test",
            "clientInstanceId" : "instanceId_test1",
            "callbackUri" : "http://15.77.21.145:8080"
        },
        "gun" : "com.hp.cdm.service.email.version.1.resource.constraints",
        "path" : "/email/v1//smtpServers/constraints",
        "method" : "get",
        "ackToken" : "onDemandAck",
        }
        ]
    }
    resource["desires"][0]["onDemand"]["clientId"] = pubsubClientId
    resource["desires"][0]["onDemand"]["clientInstanceId"] = pubsubClientInstanceId
    resource["desires"][0]["ackToken"] = "onDemandAck_" + "constraints"
    print(resource)
    headers = {}
    timeout = 4.0
    r = cdm.patch_raw(ENDPOINT_PUBSUB_ONDEMAND, resource, headers=headers, scope_alias=cdm.ScopeAlias.HP_CLOUD_SERVICE, timeout=timeout)
    print(r.status_code)
    assert (r.status_code == expected_status)
    print( "-----------------------------------------" )
    
    pubsubClientInstanceId = "verifyAccess"
    print("----- PubSub not supported for this resource " + "com.hp.cdm.service.email.version.1.verifyAccess" +"-----")
    print("----- Check ondemand desire --------")
    expected_status = 204
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.email.version.1","cdm/email/v1/verifyAccess","GET")
    print(claimScopes)
    if len(claimScopes) > 0: 
        if "com.hp.cdm.auth.alias.deviceRole.hpCloudService" not in claimScopes and "com.hp.cdm.auth.alias.deviceRole.public" not in claimScopes: 
            expected_status = 400
    resource = {
        "version": "2.3.0",
        "desires": [
        {
            "onDemand" : {
            "clientId" : "test",
            "clientInstanceId" : "instanceId_test1",
            "callbackUri" : "http://15.77.21.145:8080"
        },
        "gun" : "com.hp.cdm.service.email.version.1.resource.verifyAccess",
        "path" : "/email/v1//verifyAccess",
        "method" : "get",
        "ackToken" : "onDemandAck",
        }
        ]
    }
    resource["desires"][0]["onDemand"]["clientId"] = pubsubClientId
    resource["desires"][0]["onDemand"]["clientInstanceId"] = pubsubClientInstanceId
    resource["desires"][0]["ackToken"] = "onDemandAck_" + "verifyAccess"
    print(resource)
    headers = {}
    timeout = 4.0
    r = cdm.patch_raw(ENDPOINT_PUBSUB_ONDEMAND, resource, headers=headers, scope_alias=cdm.ScopeAlias.HP_CLOUD_SERVICE, timeout=timeout)
    print(r.status_code)
    assert (r.status_code == expected_status)
    print( "-----------------------------------------" )
    
    pubsubClientInstanceId = "verifyAccessConstraints"
    print("----- PubSub not supported for this resource " + "com.hp.cdm.service.email.version.1.constraints" +"-----")
    print("----- Check ondemand desire --------")
    expected_status = 204
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.email.version.1","cdm/email/v1/verifyAccess/constraints","GET")
    print(claimScopes)
    if len(claimScopes) > 0: 
        if "com.hp.cdm.auth.alias.deviceRole.hpCloudService" not in claimScopes and "com.hp.cdm.auth.alias.deviceRole.public" not in claimScopes: 
            expected_status = 400
    resource = {
        "version": "2.3.0",
        "desires": [
        {
            "onDemand" : {
            "clientId" : "test",
            "clientInstanceId" : "instanceId_test1",
            "callbackUri" : "http://15.77.21.145:8080"
        },
        "gun" : "com.hp.cdm.service.email.version.1.resource.constraints",
        "path" : "/email/v1//verifyAccess/constraints",
        "method" : "get",
        "ackToken" : "onDemandAck",
        }
        ]
    }
    resource["desires"][0]["onDemand"]["clientId"] = pubsubClientId
    resource["desires"][0]["onDemand"]["clientInstanceId"] = pubsubClientInstanceId
    resource["desires"][0]["ackToken"] = "onDemandAck_" + "constraints"
    print(resource)
    headers = {}
    timeout = 4.0
    r = cdm.patch_raw(ENDPOINT_PUBSUB_ONDEMAND, resource, headers=headers, scope_alias=cdm.ScopeAlias.HP_CLOUD_SERVICE, timeout=timeout)
    print(r.status_code)
    assert (r.status_code == expected_status)
    print( "-----------------------------------------" )
    
    pubsubClientInstanceId = "capabilities"
    print("----- PubSub not supported for this resource " + "com.hp.cdm.service.email.version.1.capabilities" +"-----")
    print("----- Check ondemand desire --------")
    expected_status = 204
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.email.version.1","cdm/email/v1/capabilities","GET")
    print(claimScopes)
    if len(claimScopes) > 0: 
        if "com.hp.cdm.auth.alias.deviceRole.hpCloudService" not in claimScopes and "com.hp.cdm.auth.alias.deviceRole.public" not in claimScopes: 
            expected_status = 400
    resource = {
        "version": "2.3.0",
        "desires": [
        {
            "onDemand" : {
            "clientId" : "test",
            "clientInstanceId" : "instanceId_test1",
            "callbackUri" : "http://15.77.21.145:8080"
        },
        "gun" : "com.hp.cdm.service.email.version.1.resource.capabilities",
        "path" : "/email/v1//capabilities",
        "method" : "get",
        "ackToken" : "onDemandAck",
        }
        ]
    }
    resource["desires"][0]["onDemand"]["clientId"] = pubsubClientId
    resource["desires"][0]["onDemand"]["clientInstanceId"] = pubsubClientInstanceId
    resource["desires"][0]["ackToken"] = "onDemandAck_" + "capabilities"
    print(resource)
    headers = {}
    timeout = 4.0
    r = cdm.patch_raw(ENDPOINT_PUBSUB_ONDEMAND, resource, headers=headers, scope_alias=cdm.ScopeAlias.HP_CLOUD_SERVICE, timeout=timeout)
    print(r.status_code)
    assert (r.status_code == expected_status)
    print( "-----------------------------------------" )
    
    pubsubClientInstanceId = "validatePinConstraints"
    print("----- PubSub not supported for this resource " + "com.hp.cdm.service.email.version.1.constraints" +"-----")
    print("----- Check ondemand desire --------")
    expected_status = 204
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.email.version.1","cdm/email/v1/smtpServers/validatePin/constraints","GET")
    print(claimScopes)
    if len(claimScopes) > 0: 
        if "com.hp.cdm.auth.alias.deviceRole.hpCloudService" not in claimScopes and "com.hp.cdm.auth.alias.deviceRole.public" not in claimScopes: 
            expected_status = 400
    resource = {
        "version": "2.3.0",
        "desires": [
        {
            "onDemand" : {
            "clientId" : "test",
            "clientInstanceId" : "instanceId_test1",
            "callbackUri" : "http://15.77.21.145:8080"
        },
        "gun" : "com.hp.cdm.service.email.version.1.resource.constraints",
        "path" : "/email/v1//smtpServers/validatePin/constraints",
        "method" : "get",
        "ackToken" : "onDemandAck",
        }
        ]
    }
    resource["desires"][0]["onDemand"]["clientId"] = pubsubClientId
    resource["desires"][0]["onDemand"]["clientInstanceId"] = pubsubClientInstanceId
    resource["desires"][0]["ackToken"] = "onDemandAck_" + "constraints"
    print(resource)
    headers = {}
    timeout = 4.0
    r = cdm.patch_raw(ENDPOINT_PUBSUB_ONDEMAND, resource, headers=headers, scope_alias=cdm.ScopeAlias.HP_CLOUD_SERVICE, timeout=timeout)
    print(r.status_code)
    assert (r.status_code == expected_status)
    print( "-----------------------------------------" )
    
    pubsubClientInstanceId = "validatePin"
    print("----- PubSub not supported for this resource " + "com.hp.cdm.service.email.version.1.validatePin" +"-----")
    print("----- Check ondemand desire --------")
    expected_status = 204
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.email.version.1","cdm/email/v1/smtpServers/validatePin","GET")
    print(claimScopes)
    if len(claimScopes) > 0: 
        if "com.hp.cdm.auth.alias.deviceRole.hpCloudService" not in claimScopes and "com.hp.cdm.auth.alias.deviceRole.public" not in claimScopes: 
            expected_status = 400
    resource = {
        "version": "2.3.0",
        "desires": [
        {
            "onDemand" : {
            "clientId" : "test",
            "clientInstanceId" : "instanceId_test1",
            "callbackUri" : "http://15.77.21.145:8080"
        },
        "gun" : "com.hp.cdm.service.email.version.1.resource.validatePin",
        "path" : "/email/v1//smtpServers/validatePin",
        "method" : "get",
        "ackToken" : "onDemandAck",
        }
        ]
    }
    resource["desires"][0]["onDemand"]["clientId"] = pubsubClientId
    resource["desires"][0]["onDemand"]["clientInstanceId"] = pubsubClientInstanceId
    resource["desires"][0]["ackToken"] = "onDemandAck_" + "validatePin"
    print(resource)
    headers = {}
    timeout = 4.0
    r = cdm.patch_raw(ENDPOINT_PUBSUB_ONDEMAND, resource, headers=headers, scope_alias=cdm.ScopeAlias.HP_CLOUD_SERVICE, timeout=timeout)
    print(r.status_code)
    assert (r.status_code == 400)
    print( "-----------------------------------------" )
    
    pubsubClientInstanceId = "allowedEmailDomainsConstraints"
    print("----- PubSub not supported for this resource " + "com.hp.cdm.service.email.version.1.constraints" +"-----")
    print("----- Check ondemand desire --------")
    expected_status = 204
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.email.version.1","cdm/email/v1/allowedEmailDomains/constraints","GET")
    print(claimScopes)
    if len(claimScopes) > 0: 
        if "com.hp.cdm.auth.alias.deviceRole.hpCloudService" not in claimScopes and "com.hp.cdm.auth.alias.deviceRole.public" not in claimScopes: 
            expected_status = 400
    resource = {
        "version": "2.3.0",
        "desires": [
        {
            "onDemand" : {
            "clientId" : "test",
            "clientInstanceId" : "instanceId_test1",
            "callbackUri" : "http://15.77.21.145:8080"
        },
        "gun" : "com.hp.cdm.service.email.version.1.resource.constraints",
        "path" : "/email/v1//allowedEmailDomains/constraints",
        "method" : "get",
        "ackToken" : "onDemandAck",
        }
        ]
    }
    resource["desires"][0]["onDemand"]["clientId"] = pubsubClientId
    resource["desires"][0]["onDemand"]["clientInstanceId"] = pubsubClientInstanceId
    resource["desires"][0]["ackToken"] = "onDemandAck_" + "constraints"
    print(resource)
    headers = {}
    timeout = 4.0
    r = cdm.patch_raw(ENDPOINT_PUBSUB_ONDEMAND, resource, headers=headers, scope_alias=cdm.ScopeAlias.HP_CLOUD_SERVICE, timeout=timeout)
    print(r.status_code)
    assert (r.status_code == expected_status)
    print( "-----------------------------------------" )
    
    pubsubClientInstanceId = "allowedEmailDomains"
    pubsubClientInstanceId = "smtpAutoFind"
    print("----- PubSub not supported for this resource " + "com.hp.cdm.service.email.version.1.smtpAutoFind" +"-----")
    print("----- Check ondemand desire --------")
    expected_status = 204
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.email.version.1","cdm/email/v1/smtpAutoFind","GET")
    print(claimScopes)
    if len(claimScopes) > 0: 
        if "com.hp.cdm.auth.alias.deviceRole.hpCloudService" not in claimScopes and "com.hp.cdm.auth.alias.deviceRole.public" not in claimScopes: 
            expected_status = 400
    resource = {
        "version": "2.3.0",
        "desires": [
        {
            "onDemand" : {
            "clientId" : "test",
            "clientInstanceId" : "instanceId_test1",
            "callbackUri" : "http://15.77.21.145:8080"
        },
        "gun" : "com.hp.cdm.service.email.version.1.resource.smtpAutoFind",
        "path" : "/email/v1//smtpAutoFind",
        "method" : "get",
        "ackToken" : "onDemandAck",
        }
        ]
    }
    # Check the endpoint is supported and discoverable
    if not check_endpoint(cdm, "cdm/email/v1/smtpAutoFind"):
        return

    resource["desires"][0]["onDemand"]["clientId"] = pubsubClientId
    resource["desires"][0]["onDemand"]["clientInstanceId"] = pubsubClientInstanceId
    resource["desires"][0]["ackToken"] = "onDemandAck_" + "smtpAutoFind"
    print(resource)
    headers = {}
    timeout = 4.0
    r = cdm.patch_raw(ENDPOINT_PUBSUB_ONDEMAND, resource, headers=headers, scope_alias=cdm.ScopeAlias.HP_CLOUD_SERVICE, timeout=timeout)
    print(r.status_code)
    assert (r.status_code == expected_status)
    print( "-----------------------------------------" )
    
    cdmUtil.deleteSubscriptions(pubsubClientId)
    print( "--------------------------------------------------" )

