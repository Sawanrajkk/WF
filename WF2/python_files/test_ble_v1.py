"""
///////////////////////////////////////////////////////////
/** @file: test_ble_v1.py
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

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test CDM
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-166440
    +timeout:120
    +asset:Connectivity
    +delivery_team:Connectivity
    +feature_team:WiredWiFiSolns
    +test_framework: TUF
    +name: test_ble_service
    +test :
        +title: test_ble_service
        +guid: e5a01cd0-2a6a-4827-9b64-600b30a702f1
        +dut:
            +type: Engine
            +configuration: WebServices=CDM & CloudSolution=Telemetry
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ble_service(cdm):
    servicesDiscovery = cdm.get(cdm.SERVICES_DISCOVERY)
    for service in servicesDiscovery["services"]:
        if service["serviceGun"] == "com.hp.cdm.service.ble.version.1" :
            assert "1.3.0" in service["version"]
            for link in service["links"]:
                if "hrefTemplate" in link :
                    print(link["hrefTemplate"])
                    print("dynamic resources should not be discoverable!")
                    assert(0)
                else:
                    if link["href"] == "/cdm/ble/v1/configuration"  :
                        print(link["href"] + " - is supported and discoverable")
                    if "/alerts" in link["href"]  and "service.alert" not in service["serviceGun"]:
                        print("service alert resource should not be discoverable!")
                        assert(0)

                    if link["href"] == "/cdm/ble/v1/configuration"  :
                        print(link["href"] + " - supports pubsub")


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test CDM
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-166440
    +timeout:120
    +asset:Connectivity
    +delivery_team:Connectivity
    +feature_team:WiredWiFiSolns
    +test_framework: TUF
    +name: test_ble_resource_bleConfiguration
    +test :
        +title: test_ble_resource_bleConfiguration
        +guid: 82cecfc5-0651-4ae5-89ab-628b0afa05fd
        +dut:
            +type: Engine
            +configuration: WebServices=CDM & CloudSolution=Telemetry
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ble_resource_bleConfiguration(cdm):
    cdmUtil = CdmTestUtils()
    cdmUtil.set_cdm(cdm)
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    print( "-----------------------------------------------------" )

    #test unsupported methods of bleConfiguration
    timeout = 4.0
    claimScope = cdm.ScopeAlias.PUBLIC
    #trying PATCH
    ENDPOINT = "cdm/ble/v1/configuration"
    res = {"version": "2.3.0"}
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.ble.version.1","cdm/ble/v1/configuration","PATCH")
    print(claimScopes)
    if len(claimScopes) > 0: 
        claimScope = cdmUtil.mapClaimScopeToCdm(cdm, claimScopes[0])
    headers = {}
    resp = cdm.patch_raw(ENDPOINT, res, headers=headers,  scope_alias=claimScope, timeout=timeout)
    print( resp )
    assert resp.status_code == 405
    print( "------------------------------------------------" )
    claimScope = cdm.ScopeAlias.PUBLIC
    #trying POST
    ENDPOINT = "cdm/ble/v1/configuration"
    res = {"version": "2.3.0"}
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.ble.version.1","cdm/ble/v1/configuration","POST")
    print(claimScopes)
    if len(claimScopes) > 0: 
        claimScope = cdmUtil.mapClaimScopeToCdm(cdm, claimScopes[0])
    headers = {}
    resp = cdm.post_raw(ENDPOINT, res, headers=headers, scope_alias=claimScope, timeout=timeout)
    print( resp )
    assert resp.status_code == 405
    print( "------------------------------------------------" )
    claimScope = cdm.ScopeAlias.PUBLIC
    #trying DELETE
    ENDPOINT = "cdm/ble/v1/configuration"
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.ble.version.1","cdm/ble/v1/configuration","DELETE")
    print(claimScopes)
    if len(claimScopes) > 0: 
        claimScope = cdmUtil.mapClaimScopeToCdm(cdm, claimScopes[0])
    headers = {}
    resp = cdm.delete_raw(ENDPOINT, headers=headers, scope_alias=claimScope, timeout=timeout)
    print( resp )
    assert resp.status_code == 405
    print( "------------------------------------------------" )

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test CDM
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-166440
    +timeout:120
    +asset:Connectivity
    +delivery_team:Connectivity
    +feature_team:WiredWiFiSolns
    +test_framework: TUF
    +name: test_bleConfiguration_get
    +test :
        +title: test_bleConfiguration_get
        +guid: 1090b5e4-3b35-45d9-a996-00fec30084b8
        +dut:
            +type: Engine
            +configuration: WebServices=CDM & CloudSolution=Telemetry
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_bleConfiguration_get(cdm, udw):
    cdmUtil = CdmTestUtils()
    cdmUtil.set_cdm(cdm)
    responses = [200,301,404,413,500,502,503]
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.ble.version.1","cdm/ble/v1/configuration","GET")
    print(claimScopes)
    if len(claimScopes) > 0: 
        claimScope = cdmUtil.mapClaimScopeToCdm(cdm, claimScopes[0])
    if "/alerts" in "cdm/ble/v1/configuration" and "service.alert" not in "com.hp.cdm.service.ble.version.1" and claimScope == cdm.ScopeAlias.PUBLIC:
        print("service alert resource should not be available with public claim scope!")
        assert(0)
    headers = {}
    timeout = 4.0
    ENDPOINT="cdm/ble/v1/configuration"
    resp = cdm.get_raw(ENDPOINT, headers=headers, scope_alias=claimScope, timeout=timeout)
    print(resp.status_code)
    assert resp.status_code == 200
    
    if claimScope != cdm.ScopeAlias.PUBLIC :
        #try get  with public claim scope
        r = cdm.get_raw(ENDPOINT, headers=headers, scope_alias=cdm.ScopeAlias.PUBLIC, timeout=timeout)
        print(r.status_code)
        assert r.status_code == 403
    print( "--------------------------------------------------------" )

    if claimScope == cdm.ScopeAlias.PUBLIC :
        if 401 in responses or 403 in responses:
            print("Incorrect response codes (401, 403) with PUBLIC claimScope")
            assert(0)
    print("----if resource supports data change, get etag -----")
    r0 = cdmUtil.getResource(ENDPOINT, claimScope, headers)
    if r0.status_code == 200 : 
        old_etag = cdmUtil.getETag(r0.headers["ETag"])
        powerCycleCount = old_etag/1000000 
        seqNum = old_etag - powerCycleCount * 1000000
        print("power cycle count : {}".format(powerCycleCount))
        print("seq num : {}".format(seqNum))

        print("---------GET with If-Match with the old ETag --------- ")
        headers = {'if-Match': str(old_etag), 'Accept-Encoding':''}
        r1 = cdmUtil.getResource(ENDPOINT, claimScope, headers)
        new_etag = cdmUtil.getETag( r1.headers["ETag"])
        assert r1.status_code == 200 

        print("---------GET with If-None-Match with the old ETag --------- ")
        headers = {'if-None-Match': str(old_etag)}
        r3 = cdmUtil.getResource(ENDPOINT, claimScope, headers)
        assert r3.status_code == 304 

    print( "--------------------------------------------------------" )

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test CDM
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-166440
    +timeout:120
    +asset:Connectivity
    +delivery_team:Connectivity
    +feature_team:WiredWiFiSolns
    +test_framework: TUF
    +name: test_bleConfiguration_put
    +test :
        +title: test_bleConfiguration_put
        +guid: f747b4b3-cb7e-4d56-a3a1-e8aece88baff
        +dut:
            +type: Engine
            +configuration: WebServices=CDM & CloudSolution=Telemetry
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_bleConfiguration_put(cdm, udw):
    cdmUtil = CdmTestUtils()
    cdmUtil.set_cdm(cdm)
    responses = [200,301,400,401,403,404,413,500,502,503]
    claimScope = cdm.ScopeAlias.PUBLIC
    getClaimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.ble.version.1","cdm/ble/v1/configuration","PUT")
    print(claimScopes)
    if len(claimScopes) > 0: 
        claimScope = cdmUtil.mapClaimScopeToCdm(cdm, claimScopes[0])
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.ble.version.1","cdm/ble/v1/configuration","GET")
    print(claimScopes)
    if len(claimScopes) > 0: 
        getClaimScope = cdmUtil.mapClaimScopeToCdm(cdm, claimScopes[0])
    headers = {}
    timeout = 4.0
    ENDPOINT = "cdm/ble/v1/configuration"
    
    if claimScope == cdm.ScopeAlias.PUBLIC :
        if 401 in responses or 403 in responses:
            print("incorrect response codes 401, 403")
            assert(0)
    print("-----if resource supports data change, get etag----")
    r0 = cdmUtil.getResource(ENDPOINT, getClaimScope, headers)
    if r0.status_code == 200 : 
        oldEtag = cdmUtil.getETag(r0.headers["ETag"])
        powerCycleCount = oldEtag//1000000 
        seqNum = oldEtag - powerCycleCount * 1000000
        print("power cycle count : {}".format(powerCycleCount))
        print("seq num : {}".format(seqNum))
    print("--------- change the resource with put ---------")
    #test put with empty data 
    resource = ""
    r = cdm.put_raw(ENDPOINT, resource, headers=headers, scope_alias=claimScope, timeout=timeout)
    print(r.status_code)
    assert (r.status_code == 400  or  r.status_code == 404)
    
    #test put with empty json 
    resource = {
    }
    r = cdm.put_raw(ENDPOINT, resource, headers=headers, scope_alias=claimScope, timeout=timeout)
    print(r.status_code)
    assert r.status_code == 400
    
    #test put with json containing only version
    resource = {
    "version": "2.3.0",
    }
    r = cdm.put_raw(ENDPOINT, resource, headers=headers, scope_alias=claimScope, timeout=timeout)
    print(r.status_code)
    assert r.status_code == 400
    
    print("--------- check the etag ---------")
    r1Get = cdmUtil.getResource(ENDPOINT, getClaimScope, headers)
    print(r1Get)
    if r1Get.status_code == 200 : 
        print(r1Get.headers["ETag"])
        newEtag = cdmUtil.getETag(r0.headers["ETag"])
        powerCycleCount = newEtag//1000000 
        newSeqNum = newEtag - powerCycleCount * 1000000
        print("power cycle count : {}".format(powerCycleCount))
        print("seq num : {}".format(newSeqNum))
        newSeqNum == seqNum
    
    if claimScope != cdm.ScopeAlias.PUBLIC :
        #try put  with public claim scope
        r = cdm.put_raw(ENDPOINT, resource, headers=headers, scope_alias=cdm.ScopeAlias.PUBLIC, timeout=timeout)
        print(r.status_code)
        assert r.status_code == 403
    print( "-------------------------------------------------------" )

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test CDM
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-166440
    +timeout:120
    +asset:Connectivity
    +delivery_team:Connectivity
    +feature_team:WiredWiFiSolns
    +test_framework: TUF
    +name: test_ble_pubsub_resources
    +test :
        +title: test_ble_pubsub_resources
        +guid: ef015cfe-c2b6-4c51-90f4-2128a3efe75f
        +dut:
            +type: Engine
            +configuration: WebServices=CDM & CloudSolution=Telemetry
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ble_pubsub_resources(cdm):
    cdmUtil = CdmTestUtils()
    cdmUtil.set_cdm(cdm)
    print( "--------------------------------------------------------" )
    ENDPOINT_PUBSUB = "cdm/pubsub/v2/subscriptions"
    ENDPOINT_PUBSUB_ONDEMAND = "cdm/pubsub/v2/desires"
    pubsubClientId = "ble_test"
    cdmUtil.deleteSubscriptions(pubsubClientId)
    pubsubClientInstanceId = "bleConfiguration"
    print("----- Check for PubSub " + "com.hp.cdm.service.ble.version.1.bleConfiguration" +"-----")
    resource = {
        "version": "2.3.0",
        "clientId" : "test",
        "clientInstanceId" : "instanceId_test1",
        "resources" : [
            { "gun" : "com.hp.cdm.service.ble.version.1.resource.bleConfiguration"}
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
    cdmUtil.deleteSubscriptions(pubsubClientId)
    print( "----------------------------------------------------" )
    
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test CDM
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-166440
    +timeout:120
    +asset:Connectivity
    +delivery_team:Connectivity
    +feature_team:WiredWiFiSolns
    +test_framework: TUF
    +name: test_ble_non_pubsub_resources
    +test :
        +title: test_ble_non_pubsub_resources
        +guid: 909e7f93-15f7-4813-a540-8402b5143bfa
        +dut:
            +type: Engine
            +configuration: WebServices=CDM & CloudSolution=Telemetry
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_ble_non_pubsub_resources(cdm):
    cdmUtil = CdmTestUtils()
    cdmUtil.set_cdm(cdm)
    print( "-----------------------------------------------------------" )
    ENDPOINT_PUBSUB = "cdm/pubsub/v2/subscriptions"
    ENDPOINT_PUBSUB_ONDEMAND = "cdm/pubsub/v2/desires"
    pubsubClientId = "ble_test"
    cdmUtil.deleteSubscriptions(pubsubClientId)
    pubsubClientInstanceId = "bleConfiguration"
    cdmUtil.deleteSubscriptions(pubsubClientId)
    print( "--------------------------------------------------" )
    

