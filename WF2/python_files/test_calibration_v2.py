"""
///////////////////////////////////////////////////////////
/** @file: test_calibration_v2.py
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
    +reqid: DUNE-180010
    +timeout:120
    +asset: CDM
    +delivery_team:PDLJobPQ
    +feature_team:PQsolns
    +test_framework: TUF
    +name: test_calibration_service
    +test :
        +title: test_calibration_service
        +guid: 2ae4639c-7f51-41de-8bd3-5c1d47c64484
        +dut:
            +type: Simulator
            +configuration: WebServices=CDM & CloudSolution=Telemetry
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_calibration_service(cdm):
    servicesDiscovery = cdm.get(cdm.SERVICES_DISCOVERY)
    for service in servicesDiscovery["services"]:
        if service["serviceGun"] == "com.hp.cdm.service.calibration.version.2" :
            assert "2.4.0" in service["version"] 
            for link in service["links"]:
                if "hrefTemplate" in link :
                    print(link["hrefTemplate"])
                    print("dynamic resources should not be discoverable!")
                    assert(0)
                else:
                    if link["href"] == "/cdm/calibration/v2/capabilities"  :
                        print(link["href"] + " - is supported and discoverable")
                    if link["href"] == "/cdm/calibration/v2/statuses"  :
                        print(link["href"] + " - is supported and discoverable")
                    if link["href"] == "/cdm/calibration/v2/calibrate"  :
                        print(link["href"] + " - is supported and discoverable")
                    if link["href"] == "/cdm/calibration/v2/calibrationCapabilities"  :
                        print(link["href"] + " - is supported and discoverable")
                    if link["href"] == "/cdm/calibration/v2/calibrationGroups"  :
                        print(link["href"] + " - is supported and discoverable")
                    if link["href"] == "/cdm/calibration/v2/configuration"  :
                        print(link["href"] + " - is supported and discoverable")
                    if "/alerts" in link["href"]  and "service.alert" not in service["serviceGun"]:
                        print("service alert resource should not be discoverable!")
                        assert(0)

                    if link["href"] == "/cdm/calibration/v2/statuses/0"  :
                        print(link["href"] + " - supports pubsub")
                    if link["href"] == "/cdm/calibration/v2/statuses"  :
                        print(link["href"] + " - supports pubsub")
                    if link["href"] == "/cdm/calibration/v2/calibrate"  :
                        print(link["href"] + " - supports pubsub")


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test CDM
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-180010
    +timeout:120
    +asset: CDM
    +delivery_team:PDLJobPQ
    +feature_team:PQsolns
    +test_framework: TUF
    +name: test_calibration_resource_capabilities
    +test :
        +title: test_calibration_resource_capabilities
        +guid: e0b40ca4-ee70-4277-847e-e3febfa19d22
        +dut:
            +type: Simulator
            +configuration: WebServices=CDM & CloudSolution=Telemetry
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_calibration_resource_capabilities(cdm):
    cdmUtil = CdmTestUtils()
    cdmUtil.set_cdm(cdm)
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    print( "-----------------------------------------------------" )

    #Check resource availability
    check = resource_availability_check(cdm, "com.hp.cdm.service.calibration.version.2", "/cdm/calibration/v2", "capabilities")
    print(check)
    expectedResponseStatus = 405
    if check == False:
        expectedResponseStatus = 404 #if the resource is not available, then the expected response status should be 404

    #test unsupported methods of capabilities
    timeout = 4.0
    claimScope = cdm.ScopeAlias.PUBLIC
    #trying PUT
    ENDPOINT = "cdm/calibration/v2/capabilities"
    res = {"version": "2.3.0"}
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/capabilities","PUT")
    print(claimScopes)
    if len(claimScopes) > 0: 
        claimScope = cdmUtil.mapClaimScopeToCdm(cdm, claimScopes[0])
    headers = {}
    resp = cdm.put_raw(ENDPOINT, res, headers=headers, scope_alias=claimScope, timeout=timeout)
    print( resp )
    assert resp.status_code == expectedResponseStatus
    print( "------------------------------------------------" )
    claimScope = cdm.ScopeAlias.PUBLIC
    #trying PATCH
    ENDPOINT = "cdm/calibration/v2/capabilities"
    res = {"version": "2.3.0"}
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/capabilities","PATCH")
    print(claimScopes)
    if len(claimScopes) > 0: 
        claimScope = cdmUtil.mapClaimScopeToCdm(cdm, claimScopes[0])
    headers = {}
    resp = cdm.patch_raw(ENDPOINT, res, headers=headers,  scope_alias=claimScope, timeout=timeout)
    print( resp )
    assert resp.status_code == expectedResponseStatus
    print( "------------------------------------------------" )
    claimScope = cdm.ScopeAlias.PUBLIC
    #trying POST
    ENDPOINT = "cdm/calibration/v2/capabilities"
    res = {"version": "2.3.0"}
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/capabilities","POST")
    print(claimScopes)
    if len(claimScopes) > 0: 
        claimScope = cdmUtil.mapClaimScopeToCdm(cdm, claimScopes[0])
    headers = {}
    resp = cdm.post_raw(ENDPOINT, res, headers=headers, scope_alias=claimScope, timeout=timeout)
    print( resp )
    assert resp.status_code == expectedResponseStatus
    print( "------------------------------------------------" )
    claimScope = cdm.ScopeAlias.PUBLIC
    #trying DELETE
    ENDPOINT = "cdm/calibration/v2/capabilities"
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/capabilities","DELETE")
    print(claimScopes)
    if len(claimScopes) > 0: 
        claimScope = cdmUtil.mapClaimScopeToCdm(cdm, claimScopes[0])
    headers = {}
    resp = cdm.delete_raw(ENDPOINT, headers=headers, scope_alias=claimScope, timeout=timeout)
    print( resp )
    assert resp.status_code == expectedResponseStatus
    print( "------------------------------------------------" )


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test CDM
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-180010
    +timeout:120
    +asset: CDM
    +delivery_team:PDLJobPQ
    +feature_team:PQsolns
    +test_framework: TUF
    +name: test_calibration_resource_status
    +test :
        +title: test_calibration_resource_status
        +guid: 1b1ceae6-a346-48ad-92ab-227957452b78
        +dut:
            +type: Simulator
            +configuration: WebServices=CDM & CloudSolution=Telemetry
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_calibration_resource_status(cdm):
    cdmUtil = CdmTestUtils()
    cdmUtil.set_cdm(cdm)
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    print( "-----------------------------------------------------" )

    #test unsupported methods of status
    timeout = 4.0
    claimScope = cdm.ScopeAlias.PUBLIC
    #trying PUT
    ENDPOINT = "cdm/calibration/v2/statuses/0"
    res = {"version": "2.3.0"}
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/statuses/{calibrationId}","PUT")
    print(claimScopes)
    if len(claimScopes) > 0: 
        claimScope = cdmUtil.mapClaimScopeToCdm(cdm, claimScopes[0])
    headers = {}
    resp = cdm.put_raw(ENDPOINT, res, headers=headers, scope_alias=claimScope, timeout=timeout)
    print( resp )
    assert resp.status_code == 405
    print( "------------------------------------------------" )
    claimScope = cdm.ScopeAlias.PUBLIC
    #trying PATCH
    ENDPOINT = "cdm/calibration/v2/statuses/0"
    res = {"version": "2.3.0"}
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/statuses/{calibrationId}","PATCH")
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
    ENDPOINT = "cdm/calibration/v2/statuses/0"
    res = {"version": "2.3.0"}
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/statuses/{calibrationId}","POST")
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
    ENDPOINT = "cdm/calibration/v2/statuses/0"
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/statuses/{calibrationId}","DELETE")
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
    +reqid: DUNE-180010
    +timeout:120
    +asset: CDM
    +delivery_team:PDLJobPQ
    +feature_team:PQsolns
    +test_framework: TUF
    +name: test_calibration_resource_statuses
    +test :
        +title: test_calibration_resource_statuses
        +guid: c91460f3-72ad-47b1-815d-1cb6c36fecad
        +dut:
            +type: Simulator
            +configuration: WebServices=CDM & CloudSolution=Telemetry
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_calibration_resource_statuses(cdm):
    cdmUtil = CdmTestUtils()
    cdmUtil.set_cdm(cdm)
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    print( "-----------------------------------------------------" )

    #test unsupported methods of statuses
    timeout = 4.0
    claimScope = cdm.ScopeAlias.PUBLIC
    #trying PUT
    ENDPOINT = "cdm/calibration/v2/statuses"
    res = {"version": "2.3.0"}
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/statuses","PUT")
    print(claimScopes)
    if len(claimScopes) > 0: 
        claimScope = cdmUtil.mapClaimScopeToCdm(cdm, claimScopes[0])
    headers = {}
    resp = cdm.put_raw(ENDPOINT, res, headers=headers, scope_alias=claimScope, timeout=timeout)
    print( resp )
    assert resp.status_code == 405
    print( "------------------------------------------------" )
    claimScope = cdm.ScopeAlias.PUBLIC
    #trying PATCH
    ENDPOINT = "cdm/calibration/v2/statuses"
    res = {"version": "2.3.0"}
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/statuses","PATCH")
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
    ENDPOINT = "cdm/calibration/v2/statuses"
    res = {"version": "2.3.0"}
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/statuses","POST")
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
    ENDPOINT = "cdm/calibration/v2/statuses"
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/statuses","DELETE")
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
    +reqid: DUNE-180010
    +timeout:120
    +asset: CDM
    +delivery_team:PDLJobPQ
    +feature_team:PQsolns
    +test_framework: TUF
    +name: test_calibration_resource_calibrate
    +test :
        +title: test_calibration_resource_calibrate
        +guid: 121cf33b-133f-4221-aa6e-3b7c2ac45ce9
        +dut:
            +type: Simulator
            +configuration: WebServices=CDM & CloudSolution=Telemetry
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_calibration_resource_calibrate(cdm):
    cdmUtil = CdmTestUtils()
    cdmUtil.set_cdm(cdm)
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    print( "-----------------------------------------------------" )

    #test unsupported methods of calibrate
    timeout = 4.0
    claimScope = cdm.ScopeAlias.PUBLIC
    #trying PUT
    ENDPOINT = "cdm/calibration/v2/calibrate"
    res = {"version": "2.3.0"}
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/calibrate","PUT")
    print(claimScopes)
    if len(claimScopes) > 0: 
        claimScope = cdmUtil.mapClaimScopeToCdm(cdm, claimScopes[0])
    headers = {}
    resp = cdm.put_raw(ENDPOINT, res, headers=headers, scope_alias=claimScope, timeout=timeout)
    print( resp )
    assert resp.status_code == 405
    print( "------------------------------------------------" )
    claimScope = cdm.ScopeAlias.PUBLIC
    #trying POST
    ENDPOINT = "cdm/calibration/v2/calibrate"
    res = {"version": "2.3.0"}
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/calibrate","POST")
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
    ENDPOINT = "cdm/calibration/v2/calibrate"
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/calibrate","DELETE")
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
    +reqid: DUNE-180010
    +timeout:120
    +asset: CDM
    +delivery_team:PDLJobPQ
    +feature_team:PQsolns
    +test_framework: TUF
    +name: test_calibration_resource_calibrationCapabilities
    +test :
        +title: test_calibration_resource_calibrationCapabilities
        +guid: 4895ab17-f674-460a-a67b-439c950088e5
        +dut:
            +type: Simulator
            +configuration: WebServices=CDM & CloudSolution=Telemetry
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_calibration_resource_calibrationCapabilities(cdm):
    cdmUtil = CdmTestUtils()
    cdmUtil.set_cdm(cdm)
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    print( "-----------------------------------------------------" )

    #test unsupported methods of calibrationCapabilities
    timeout = 4.0
    claimScope = cdm.ScopeAlias.PUBLIC
    #trying PUT
    ENDPOINT = "cdm/calibration/v2/calibrationCapabilities"
    res = {"version": "2.3.0"}
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/calibrationCapabilities","PUT")
    print(claimScopes)
    if len(claimScopes) > 0: 
        claimScope = cdmUtil.mapClaimScopeToCdm(cdm, claimScopes[0])
    headers = {}
    resp = cdm.put_raw(ENDPOINT, res, headers=headers, scope_alias=claimScope, timeout=timeout)
    print( resp )
    assert resp.status_code == 405
    print( "------------------------------------------------" )
    claimScope = cdm.ScopeAlias.PUBLIC
    #trying PATCH
    ENDPOINT = "cdm/calibration/v2/calibrationCapabilities"
    res = {"version": "2.3.0"}
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/calibrationCapabilities","PATCH")
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
    ENDPOINT = "cdm/calibration/v2/calibrationCapabilities"
    res = {"version": "2.3.0"}
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/calibrationCapabilities","POST")
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
    ENDPOINT = "cdm/calibration/v2/calibrationCapabilities"
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/calibrationCapabilities","DELETE")
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
    +reqid: DUNE-180010
    +timeout:120
    +asset: CDM
    +delivery_team:PDLJobPQ
    +feature_team:PQsolns
    +test_framework: TUF
    +name: test_calibration_resource_calibrationGroups
    +test :
        +title: test_calibration_resource_calibrationGroups
        +guid: bd17051e-08fd-4d32-9bf1-68de4d8436a1
        +dut:
            +type: Simulator
            +configuration: WebServices=CDM & CloudSolution=Telemetry
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_calibration_resource_calibrationGroups(cdm):
    cdmUtil = CdmTestUtils()
    cdmUtil.set_cdm(cdm)
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    print( "-----------------------------------------------------" )

    #Check resource availability
    check = resource_availability_check(cdm, "com.hp.cdm.service.calibration.version.2", "/cdm/calibration/v2", "calibrationGroups")
    print(check)
    expectedResponseStatus = 405
    if check == False:
        expectedResponseStatus = 404 #if the resource is not available, then the expected response status should be 404

    #test unsupported methods of calibrationGroups
    timeout = 4.0
    claimScope = cdm.ScopeAlias.PUBLIC
    #trying PUT
    ENDPOINT = "cdm/calibration/v2/calibrationGroups"
    res = {"version": "2.3.0"}
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/calibrationGroups","PUT")
    print(claimScopes)
    if len(claimScopes) > 0: 
        claimScope = cdmUtil.mapClaimScopeToCdm(cdm, claimScopes[0])
    headers = {}
    resp = cdm.put_raw(ENDPOINT, res, headers=headers, scope_alias=claimScope, timeout=timeout)
    print( resp )
    assert resp.status_code == expectedResponseStatus
    print( "------------------------------------------------" )
    claimScope = cdm.ScopeAlias.PUBLIC
    #trying PATCH
    ENDPOINT = "cdm/calibration/v2/calibrationGroups"
    res = {"version": "2.3.0"}
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/calibrationGroups","PATCH")
    print(claimScopes)
    if len(claimScopes) > 0: 
        claimScope = cdmUtil.mapClaimScopeToCdm(cdm, claimScopes[0])
    headers = {}
    resp = cdm.patch_raw(ENDPOINT, res, headers=headers,  scope_alias=claimScope, timeout=timeout)
    print( resp )
    assert resp.status_code == expectedResponseStatus
    print( "------------------------------------------------" )
    claimScope = cdm.ScopeAlias.PUBLIC
    #trying POST
    ENDPOINT = "cdm/calibration/v2/calibrationGroups"
    res = {"version": "2.3.0"}
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/calibrationGroups","POST")
    print(claimScopes)
    if len(claimScopes) > 0: 
        claimScope = cdmUtil.mapClaimScopeToCdm(cdm, claimScopes[0])
    headers = {}
    resp = cdm.post_raw(ENDPOINT, res, headers=headers, scope_alias=claimScope, timeout=timeout)
    print( resp )
    assert resp.status_code == expectedResponseStatus
    print( "------------------------------------------------" )
    claimScope = cdm.ScopeAlias.PUBLIC
    #trying DELETE
    ENDPOINT = "cdm/calibration/v2/calibrationGroups"
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/calibrationGroups","DELETE")
    print(claimScopes)
    if len(claimScopes) > 0: 
        claimScope = cdmUtil.mapClaimScopeToCdm(cdm, claimScopes[0])
    headers = {}
    resp = cdm.delete_raw(ENDPOINT, headers=headers, scope_alias=claimScope, timeout=timeout)
    print( resp )
    assert resp.status_code == expectedResponseStatus
    print( "------------------------------------------------" )


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test CDM
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-180010
    +timeout:120
    +asset: CDM
    +delivery_team:PDLJobPQ
    +feature_team:PQsolns
    +test_framework: TUF
    +name: test_calibration_resource_calibrationsAction
    +test :
        +title: test_calibration_resource_calibrationsAction
        +guid: 46bf5493-d3d1-4efa-baf2-e7d71088b9b8
        +dut:
            +type: Simulator
            +configuration: WebServices=CDM & CloudSolution=Telemetry
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_calibration_resource_calibrationsAction(cdm):
    cdmUtil = CdmTestUtils()
    cdmUtil.set_cdm(cdm)
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    print( "-----------------------------------------------------" )

    #test unsupported methods of calibrationsAction
    timeout = 4.0
    claimScope = cdm.ScopeAlias.PUBLIC
    #trying GET
    ENDPOINT = "cdm/calibration/v2/calibrationsAction"
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/calibrationsAction","GET")
    print(claimScopes)
    if len(claimScopes) > 0: 
        claimScope = cdmUtil.mapClaimScopeToCdm(cdm, claimScopes[0])
    headers = {}
    resp = cdm.get_raw(ENDPOINT, headers=headers, scope_alias=claimScope, timeout=timeout)
    print( resp )
    assert resp.status_code == 405
    print( "------------------------------------------------" )
    claimScope = cdm.ScopeAlias.PUBLIC
    #trying PUT
    ENDPOINT = "cdm/calibration/v2/calibrationsAction"
    res = {"version": "2.3.0"}
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/calibrationsAction","PUT")
    print(claimScopes)
    if len(claimScopes) > 0: 
        claimScope = cdmUtil.mapClaimScopeToCdm(cdm, claimScopes[0])
    headers = {}
    resp = cdm.put_raw(ENDPOINT, res, headers=headers, scope_alias=claimScope, timeout=timeout)
    print( resp )
    assert resp.status_code == 405
    print( "------------------------------------------------" )
    claimScope = cdm.ScopeAlias.PUBLIC
    #trying POST
    ENDPOINT = "cdm/calibration/v2/calibrationsAction"
    res = {"version": "2.3.0"}
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/calibrationsAction","POST")
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
    ENDPOINT = "cdm/calibration/v2/calibrationsAction"
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/calibrationsAction","DELETE")
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
    +reqid: DUNE-180010
    +timeout:120
    +asset: CDM
    +delivery_team:PDLJobPQ
    +feature_team:PQsolns
    +test_framework: TUF
    +name: test_calibration_resource_alerts
    +test :
        +title: test_calibration_resource_alerts
        +guid: 45ade09f-5a6c-4677-a143-8ea18182bbd2
        +dut:
            +type: Simulator
            +configuration: WebServices=CDM & CloudSolution=Telemetry
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_calibration_resource_alerts(cdm):
    cdmUtil = CdmTestUtils()
    cdmUtil.set_cdm(cdm)
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    print( "-----------------------------------------------------" )

    #test unsupported methods of alerts
    timeout = 4.0
    claimScope = cdm.ScopeAlias.PUBLIC
    #trying PUT
    ENDPOINT = "cdm/calibration/v2/alerts"
    res = {"version": "2.3.0"}
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/alerts","PUT")
    print(claimScopes)
    if len(claimScopes) > 0: 
        claimScope = cdmUtil.mapClaimScopeToCdm(cdm, claimScopes[0])
    headers = {}
    resp = cdm.put_raw(ENDPOINT, res, headers=headers, scope_alias=claimScope, timeout=timeout)
    print( resp )
    assert resp.status_code == 405
    print( "------------------------------------------------" )
    claimScope = cdm.ScopeAlias.PUBLIC
    #trying PATCH
    ENDPOINT = "cdm/calibration/v2/alerts"
    res = {"version": "2.3.0"}
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/alerts","PATCH")
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
    ENDPOINT = "cdm/calibration/v2/alerts"
    res = {"version": "2.3.0"}
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/alerts","POST")
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
    ENDPOINT = "cdm/calibration/v2/alerts"
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/alerts","DELETE")
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
    +reqid: DUNE-180010
    +timeout:120
    +asset: CDM
    +delivery_team:PDLJobPQ
    +feature_team:PQsolns
    +test_framework: TUF
    +name: test_calibration_resource_alert
    +test :
        +title: test_calibration_resource_alert
        +guid: ce50b81e-94a9-4737-b277-8ebf7779d555
        +dut:
            +type: Simulator
            +configuration: WebServices=CDM & CloudSolution=Telemetry
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_calibration_resource_alert(cdm):
    cdmUtil = CdmTestUtils()
    cdmUtil.set_cdm(cdm)
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    print( "-----------------------------------------------------" )

    #test unsupported methods of alert
    timeout = 4.0
    claimScope = cdm.ScopeAlias.PUBLIC
    #trying PUT
    ENDPOINT = "cdm/calibration/v2/alerts/0"
    res = {"version": "2.3.0"}
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/alerts/{id}","PUT")
    print(claimScopes)
    if len(claimScopes) > 0: 
        claimScope = cdmUtil.mapClaimScopeToCdm(cdm, claimScopes[0])
    headers = {}
    resp = cdm.put_raw(ENDPOINT, res, headers=headers, scope_alias=claimScope, timeout=timeout)
    print( resp )
    assert resp.status_code == 405
    print( "------------------------------------------------" )
    claimScope = cdm.ScopeAlias.PUBLIC
    #trying PATCH
    ENDPOINT = "cdm/calibration/v2/alerts/0"
    res = {"version": "2.3.0"}
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/alerts/{id}","PATCH")
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
    ENDPOINT = "cdm/calibration/v2/alerts/0"
    res = {"version": "2.3.0"}
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/alerts/{id}","POST")
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
    ENDPOINT = "cdm/calibration/v2/alerts/0"
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/alerts/{id}","DELETE")
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
    +reqid: DUNE-180010
    +timeout:120
    +asset: CDM
    +delivery_team:PDLJobPQ
    +feature_team:PQsolns
    +test_framework: TUF
    +name: test_calibration_resource_alertAction
    +test :
        +title: test_calibration_resource_alertAction
        +guid: 3fec06ca-1789-4a17-9260-9a2f3257d45d
        +dut:
            +type: Simulator
            +configuration: WebServices=CDM & CloudSolution=Telemetry
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_calibration_resource_alertAction(cdm):
    cdmUtil = CdmTestUtils()
    cdmUtil.set_cdm(cdm)
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    print( "-----------------------------------------------------" )

    #test unsupported methods of alertAction
    timeout = 4.0
    claimScope = cdm.ScopeAlias.PUBLIC
    #trying GET
    ENDPOINT = "cdm/calibration/v2/alerts/0/action"
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/alerts/{id}/action","GET")
    print(claimScopes)
    if len(claimScopes) > 0: 
        claimScope = cdmUtil.mapClaimScopeToCdm(cdm, claimScopes[0])
    headers = {}
    resp = cdm.get_raw(ENDPOINT, headers=headers, scope_alias=claimScope, timeout=timeout)
    print( resp )
    assert resp.status_code == 405
    print( "------------------------------------------------" )
    claimScope = cdm.ScopeAlias.PUBLIC
    #trying PATCH
    ENDPOINT = "cdm/calibration/v2/alerts/0/action"
    res = {"version": "2.3.0"}
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/alerts/{id}/action","PATCH")
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
    ENDPOINT = "cdm/calibration/v2/alerts/0/action"
    res = {"version": "2.3.0"}
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/alerts/{id}/action","POST")
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
    ENDPOINT = "cdm/calibration/v2/alerts/0/action"
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/alerts/{id}/action","DELETE")
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
    +reqid: DUNE-180010
    +timeout:120
    +asset: CDM
    +delivery_team:PDLJobPQ
    +feature_team:PQsolns
    +test_framework: TUF
    +name: test_calibration_resource_configuration
    +test :
        +title: test_calibration_resource_configuration
        +guid: b7876912-8678-435b-9e43-6dfb867243cb
        +dut:
            +type: Simulator
            +configuration: WebServices=CDM & CloudSolution=Telemetry
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_calibration_resource_configuration(cdm):
    cdmUtil = CdmTestUtils()
    cdmUtil.set_cdm(cdm)
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    print( "-----------------------------------------------------" )

    #check resource availability
    check = resource_availability_check(cdm, "com.hp.cdm.service.calibration.version.2", "/cdm/calibration/v2", "configuration")
    print(check)
    expectedResponseStatus = 405
    if check == False:
        expectedResponseStatus = 404 #if the resource is not available, then the expected response status should be 404

    #test unsupported methods of configuration
    timeout = 4.0
    claimScope = cdm.ScopeAlias.PUBLIC
    #trying PUT
    ENDPOINT = "cdm/calibration/v2/configuration"
    res = {"version": "2.3.0"}
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/configuration","PUT")
    print(claimScopes)
    if len(claimScopes) > 0: 
        claimScope = cdmUtil.mapClaimScopeToCdm(cdm, claimScopes[0])
    headers = {}
    resp = cdm.put_raw(ENDPOINT, res, headers=headers, scope_alias=claimScope, timeout=timeout)
    print( resp )
    assert resp.status_code == expectedResponseStatus
    print( "------------------------------------------------" )
    claimScope = cdm.ScopeAlias.PUBLIC
    #trying POST
    ENDPOINT = "cdm/calibration/v2/configuration"
    res = {"version": "2.3.0"}
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/configuration","POST")
    print(claimScopes)
    if len(claimScopes) > 0: 
        claimScope = cdmUtil.mapClaimScopeToCdm(cdm, claimScopes[0])
    headers = {}
    resp = cdm.post_raw(ENDPOINT, res, headers=headers, scope_alias=claimScope, timeout=timeout)
    print( resp )
    assert resp.status_code == expectedResponseStatus
    print( "------------------------------------------------" )
    claimScope = cdm.ScopeAlias.PUBLIC
    #trying DELETE
    ENDPOINT = "cdm/calibration/v2/configuration"
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/configuration","DELETE")
    print(claimScopes)
    if len(claimScopes) > 0: 
        claimScope = cdmUtil.mapClaimScopeToCdm(cdm, claimScopes[0])
    headers = {}
    resp = cdm.delete_raw(ENDPOINT, headers=headers, scope_alias=claimScope, timeout=timeout)
    print( resp )
    assert resp.status_code == expectedResponseStatus
    print( "------------------------------------------------" )


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test CDM
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-180010
    +timeout:120
    +asset: CDM
    +delivery_team:PDLJobPQ
    +feature_team:PQsolns
    +test_framework: TUF
    +name: test_calibration_resource_resetAllCalibrationData
    +test :
        +title: test_calibration_resource_resetAllCalibrationData
        +guid: cbaf16de-6a6b-4485-8d37-82e6326748e6
        +dut:
            +type: Simulator
            +configuration: WebServices=CDM & CloudSolution=Telemetry
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_calibration_resource_resetAllCalibrationData(cdm):
    cdmUtil = CdmTestUtils()
    cdmUtil.set_cdm(cdm)
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    print( "-----------------------------------------------------" )

    #Check resource availability
    check = resource_availability_check(cdm, "com.hp.cdm.service.calibration.version.2", "/cdm/calibration/v2", "resetAllCalibrationData")
    print(check)
    expectedResponseStatus = 405
    if check == False:
        expectedResponseStatus = 404 #if the resource is not available, then the expected response status should be 404

    #test unsupported methods of resetAllCalibrationData
    timeout = 4.0
    claimScope = cdm.ScopeAlias.PUBLIC
    #trying PUT
    ENDPOINT = "cdm/calibration/v2/resetAllCalibrationData"
    res = {"version": "2.3.0"}
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/resetAllCalibrationData","PUT")
    print(claimScopes)
    if len(claimScopes) > 0: 
        claimScope = cdmUtil.mapClaimScopeToCdm(cdm, claimScopes[0])
    headers = {}
    resp = cdm.put_raw(ENDPOINT, res, headers=headers, scope_alias=claimScope, timeout=timeout)
    print( resp )
    assert resp.status_code == expectedResponseStatus
    print( "------------------------------------------------" )
    claimScope = cdm.ScopeAlias.PUBLIC
    #trying POST
    ENDPOINT = "cdm/calibration/v2/resetAllCalibrationData"
    res = {"version": "2.3.0"}
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/resetAllCalibrationData","POST")
    print(claimScopes)
    if len(claimScopes) > 0: 
        claimScope = cdmUtil.mapClaimScopeToCdm(cdm, claimScopes[0])
    headers = {}
    resp = cdm.post_raw(ENDPOINT, res, headers=headers, scope_alias=claimScope, timeout=timeout)
    print( resp )
    assert resp.status_code == expectedResponseStatus
    print( "------------------------------------------------" )
    claimScope = cdm.ScopeAlias.PUBLIC
    #trying DELETE
    ENDPOINT = "cdm/calibration/v2/resetAllCalibrationData"
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/resetAllCalibrationData","DELETE")
    print(claimScopes)
    if len(claimScopes) > 0: 
        claimScope = cdmUtil.mapClaimScopeToCdm(cdm, claimScopes[0])
    headers = {}
    resp = cdm.delete_raw(ENDPOINT, headers=headers, scope_alias=claimScope, timeout=timeout)
    print( resp )
    assert resp.status_code == expectedResponseStatus
    print( "------------------------------------------------" )

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test CDM
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-180010
    +timeout:120
    +asset: CDM
    +delivery_team:PDLJobPQ
    +feature_team:PQsolns
    +test_framework: TUF
    +name: test__calibration_v2_capabilities_get
    +test :
        +title: test__calibration_v2_capabilities_get
        +guid: 142c85ec-a518-475b-a2da-d8211bd861f7
        +dut:
            +type: Simulator
            +configuration: WebServices=CDM & CloudSolution=Telemetry
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test__calibration_v2_capabilities_get(cdm, udw):
    cdmUtil = CdmTestUtils()
    cdmUtil.set_cdm(cdm)
    responses = [200,401,403,500,502,503]
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/capabilities","GET")
    print(claimScopes)
    if len(claimScopes) > 0: 
        claimScope = cdmUtil.mapClaimScopeToCdm(cdm, claimScopes[0])
    if "/alerts" in "cdm/calibration/v2/capabilities" and "service.alert" not in "com.hp.cdm.service.calibration.version.2" and claimScope == cdm.ScopeAlias.PUBLIC:
        print("service alert resource should not be available with public claim scope!")
        assert(0)
    headers = {}
    timeout = 4.0
    ENDPOINT="cdm/calibration/v2/capabilities"
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
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test CDM
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-180010
    +timeout:120
    +asset: CDM
    +delivery_team:PDLJobPQ
    +feature_team:PQsolns
    +test_framework: TUF
    +name: test_calibration_v2_status_get
    +test :
        +title: test_calibration_v2_status_get
        +guid: 7115da33-4b97-4521-8e3a-88f78eefabe4
        +dut:
            +type: Simulator
            +configuration: WebServices=CDM & CloudSolution=Telemetry
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_calibration_v2_status_get(cdm, udw):
    cdmUtil = CdmTestUtils()
    cdmUtil.set_cdm(cdm)
    responses = [200,304,401,403,404,500,502,503]
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/statuses/{calibrationId}","GET")
    print(claimScopes)
    if len(claimScopes) > 0: 
        claimScope = cdmUtil.mapClaimScopeToCdm(cdm, claimScopes[0])
    if "/alerts" in "cdm/calibration/v2/statuses/0" and "service.alert" not in "com.hp.cdm.service.calibration.version.2" and claimScope == cdm.ScopeAlias.PUBLIC:
        print("service alert resource should not be available with public claim scope!")
        assert(0)
    headers = {}
    timeout = 4.0
    ENDPOINT="cdm/calibration/v2/statuses/0"
    resp = cdm.get_raw(ENDPOINT, headers=headers, scope_alias=claimScope, timeout=timeout)
    print(resp.status_code)
    assert resp.status_code == 404
    
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
    +reqid: DUNE-180010
    +timeout:120
    +asset: CDM
    +delivery_team:PDLJobPQ
    +feature_team:PQsolns
    +test_framework: TUF
    +name: test_statuses_get
    +test :
        +title: test_statuses_get
        +guid: 4d377605-0a18-46fb-a419-5c7f76881cc7
        +dut:
            +type: Simulator
            +configuration: WebServices=CDM & CloudSolution=Telemetry
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_statuses_get(cdm, udw):
    cdmUtil = CdmTestUtils()
    cdmUtil.set_cdm(cdm)
    responses = [200,304,401,403,500,502,503]
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/statuses","GET")
    print(claimScopes)
    if len(claimScopes) > 0: 
        claimScope = cdmUtil.mapClaimScopeToCdm(cdm, claimScopes[0])
    if "/alerts" in "cdm/calibration/v2/statuses" and "service.alert" not in "com.hp.cdm.service.calibration.version.2" and claimScope == cdm.ScopeAlias.PUBLIC:
        print("service alert resource should not be available with public claim scope!")
        assert(0)
    headers = {}
    timeout = 4.0
    ENDPOINT="cdm/calibration/v2/statuses"
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
    +reqid: DUNE-180010
    +timeout:120
    +asset: CDM
    +delivery_team:PDLJobPQ
    +feature_team:PQsolns
    +test_framework: TUF
    +name: test_calibrate_get
    +test :
        +title: test_calibrate_get
        +guid: 7aa566d0-449d-4c34-9fc3-751d9deb5cee
        +dut:
            +type: Simulator
            +configuration: WebServices=CDM & CloudSolution=Telemetry
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_calibrate_get(cdm, udw):
    cdmUtil = CdmTestUtils()
    cdmUtil.set_cdm(cdm)
    responses = [200,304,401,403,500,502,503]
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/calibrate","GET")
    print(claimScopes)
    if len(claimScopes) > 0: 
        claimScope = cdmUtil.mapClaimScopeToCdm(cdm, claimScopes[0])
    if "/alerts" in "cdm/calibration/v2/calibrate" and "service.alert" not in "com.hp.cdm.service.calibration.version.2" and claimScope == cdm.ScopeAlias.PUBLIC:
        print("service alert resource should not be available with public claim scope!")
        assert(0)
    headers = {}
    timeout = 4.0
    ENDPOINT="cdm/calibration/v2/calibrate"
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
    +reqid: DUNE-180010
    +timeout:120
    +asset: CDM
    +delivery_team:PDLJobPQ
    +feature_team:PQsolns
    +test_framework: TUF
    +name: test_calibrate_patch
    +test :
        +title: test_calibrate_patch
        +guid: 18e404e8-6a4b-466c-90d4-5182201d4291
        +dut:
            +type: Simulator
            +configuration: WebServices=CDM & CloudSolution=Telemetry
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_calibrate_patch(cdm, udw):
    cdmUtil = CdmTestUtils()
    cdmUtil.set_cdm(cdm)
    responses = [202,400,401,403,404,409,500,502,503]
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/calibrate","PATCH")
    print(claimScopes)
    if len(claimScopes) > 0: 
        claimScope = cdmUtil.mapClaimScopeToCdm(cdm, claimScopes[0])
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/calibrate","GET")
    print(claimScopes)
    if len(claimScopes) > 0: 
        getClaimScope = cdmUtil.mapClaimScopeToCdm(cdm, claimScopes[0])
    headers = {}
    timeout = 4.0
    ENDPOINT="cdm/calibration/v2/calibrate"
    print("----if resource supports data change, get etag -----")
    r0 = cdmUtil.getResource(ENDPOINT, getClaimScope, headers)
    if r0.status_code == 200 : 
        oldEtag = cdmUtil.getETag(r0.headers["ETag"])
        powerCycleCount = oldEtag//1000000 
        seqNum = oldEtag - powerCycleCount * 1000000
        print("power cycle count : {}".format(powerCycleCount))
        print("seq num : {}".format(seqNum))
    print("--------- change the resource with patch ---------")
    #test patch with empty data 
    resource = ""
    r = cdm.patch_raw(ENDPOINT, resource, headers=headers, scope_alias=claimScope, timeout=timeout)
    print(r.status_code)
    assert (r.status_code == 400  or  r.status_code == 404)
    
    #test patch with empty json 
    resource = {
    }
    r = cdm.patch_raw(ENDPOINT, resource, headers=headers, scope_alias=claimScope, timeout=timeout)
    print(r.status_code)
    assert r.status_code == 400
    
    #test patch with data with only version field 
    resource = {
    "version": "2.3.0",
    }
    r = cdm.patch_raw(ENDPOINT, resource, headers=headers, scope_alias=claimScope, timeout=timeout)
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
        #try patch  with public claim scope
        r = cdm.patch_raw(ENDPOINT, resource, headers=headers, scope_alias=cdm.ScopeAlias.PUBLIC, timeout=timeout)
        print(r.status_code)
        assert r.status_code == 403
    print( "--------------------------------------------------------" )

    if claimScope == cdm.ScopeAlias.PUBLIC :
        if 401 in responses or 403 in responses:
            print("Incorrect response codes (401, 403) with PUBLIC claimScope")
            assert(0)
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test CDM
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-180010
    +timeout:120
    +asset: CDM
    +delivery_team:PDLJobPQ
    +feature_team:PQsolns
    +test_framework: TUF
    +name: test_calibrationCapabilities_get
    +test :
        +title: test_calibrationCapabilities_get
        +guid: a6e3d471-46eb-47fd-9296-6da1965a21c3
        +dut:
            +type: Simulator
            +configuration: WebServices=CDM & CloudSolution=Telemetry
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_calibrationCapabilities_get(cdm, udw):
    cdmUtil = CdmTestUtils()
    cdmUtil.set_cdm(cdm)
    responses = [200,401,403,500,502,503]
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/calibrationCapabilities","GET")
    print(claimScopes)
    if len(claimScopes) > 0: 
        claimScope = cdmUtil.mapClaimScopeToCdm(cdm, claimScopes[0])
    if "/alerts" in "cdm/calibration/v2/calibrationCapabilities" and "service.alert" not in "com.hp.cdm.service.calibration.version.2" and claimScope == cdm.ScopeAlias.PUBLIC:
        print("service alert resource should not be available with public claim scope!")
        assert(0)
    headers = {}
    timeout = 4.0
    ENDPOINT="cdm/calibration/v2/calibrationCapabilities"
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
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test CDM
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-180010
    +timeout:120
    +asset: CDM
    +delivery_team:PDLJobPQ
    +feature_team:PQsolns
    +test_framework: TUF
    +name: test_calibrationGroups_get
    +test :
        +title: test_calibrationGroups_get
        +guid: 8cf6d771-31e7-4ff5-998a-6eb2f8d8385e
        +dut:
            +type: Simulator
            +configuration: WebServices=CDM & CloudSolution=Telemetry
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_calibrationGroups_get(cdm, udw):
    #Check resource availability
    check = resource_availability_check(cdm, "com.hp.cdm.service.calibration.version.2", "/cdm/calibration/v2", "calibrationGroups")
    print(check)
    if check == False:
        print("Resource not available")
        return

    cdmUtil = CdmTestUtils()
    cdmUtil.set_cdm(cdm)
    responses = [200,401,403,404,500,502,503]
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/calibrationGroups","GET")
    print(claimScopes)
    if len(claimScopes) > 0: 
        claimScope = cdmUtil.mapClaimScopeToCdm(cdm, claimScopes[0])
    if "/alerts" in "cdm/calibration/v2/calibrationGroups" and "service.alert" not in "com.hp.cdm.service.calibration.version.2" and claimScope == cdm.ScopeAlias.PUBLIC:
        print("service alert resource should not be available with public claim scope!")
        assert(0)
    headers = {}
    timeout = 4.0
    ENDPOINT="cdm/calibration/v2/calibrationGroups"
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
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test CDM
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-180010
    +timeout:120
    +asset: CDM
    +delivery_team:PDLJobPQ
    +feature_team:PQsolns
    +test_framework: TUF
    +name: test_calibrationsAction_patch
    +test :
        +title: test_calibrationsAction_patch
        +guid: af65df51-8bd9-41ec-a171-8dcf7b8415ee
        +dut:
            +type: Simulator
            +configuration: WebServices=CDM & CloudSolution=Telemetry
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_calibrationsAction_patch(cdm, udw):
    cdmUtil = CdmTestUtils()
    cdmUtil.set_cdm(cdm)
    responses = [200,204,400,401,403,500,502,503]
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/calibrationsAction","PATCH")
    print(claimScopes)
    if len(claimScopes) > 0: 
        claimScope = cdmUtil.mapClaimScopeToCdm(cdm, claimScopes[0])
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/calibrationsAction","GET")
    print(claimScopes)
    if len(claimScopes) > 0: 
        getClaimScope = cdmUtil.mapClaimScopeToCdm(cdm, claimScopes[0])
    headers = {}
    timeout = 4.0
    ENDPOINT="cdm/calibration/v2/calibrationsAction"
    print("--------- change the resource with patch ---------")
    #test patch with empty data 
    resource = ""
    r = cdm.patch_raw(ENDPOINT, resource, headers=headers, scope_alias=claimScope, timeout=timeout)
    print(r.status_code)
    assert (r.status_code == 400  or  r.status_code == 404)
    
    #test patch with empty json 
    resource = {
    }
    r = cdm.patch_raw(ENDPOINT, resource, headers=headers, scope_alias=claimScope, timeout=timeout)
    print(r.status_code)
    assert r.status_code == 400
    
    #test patch with data with only version field 
    resource = {
    "version": "2.3.0",
    }
    r = cdm.patch_raw(ENDPOINT, resource, headers=headers, scope_alias=claimScope, timeout=timeout)
    print(r.status_code)
    assert r.status_code == 400
    
    
    if claimScope != cdm.ScopeAlias.PUBLIC :
        #try patch  with public claim scope
        r = cdm.patch_raw(ENDPOINT, resource, headers=headers, scope_alias=cdm.ScopeAlias.PUBLIC, timeout=timeout)
        print(r.status_code)
        assert r.status_code == 403
    print( "--------------------------------------------------------" )

    if claimScope == cdm.ScopeAlias.PUBLIC :
        if 401 in responses or 403 in responses:
            print("Incorrect response codes (401, 403) with PUBLIC claimScope")
            assert(0)
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test CDM
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-180010
    +timeout:120
    +asset: CDM
    +delivery_team:PDLJobPQ
    +feature_team:PQsolns
    +test_framework: TUF
    +name: test__calibration_v2_alerts_get
    +test :
        +title: test__calibration_v2_alerts_get
        +guid: b2495956-fbe9-4b3c-aa49-1c956d6b99d8
        +dut:
            +type: Simulator
            +configuration: WebServices=CDM & CloudSolution=Telemetry
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test__calibration_v2_alerts_get(cdm, udw):
    cdmUtil = CdmTestUtils()
    cdmUtil.set_cdm(cdm)
    responses = [200,401,403,500,502,503]
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/alerts","GET")
    print(claimScopes)
    if len(claimScopes) > 0: 
        claimScope = cdmUtil.mapClaimScopeToCdm(cdm, claimScopes[0])
    if "/alerts" in "cdm/calibration/v2/alerts" and "service.alert" not in "com.hp.cdm.service.calibration.version.2" and claimScope == cdm.ScopeAlias.PUBLIC:
        print("service alert resource should not be available with public claim scope!")
        assert(0)
    headers = {}
    timeout = 4.0
    ENDPOINT="cdm/calibration/v2/alerts"
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
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test CDM
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-180010
    +timeout:120
    +asset: CDM
    +delivery_team:PDLJobPQ
    +feature_team:PQsolns
    +test_framework: TUF
    +name: test__calibration_v2_alert_get
    +test :
        +title: test__calibration_v2_alert_get
        +guid: a809f7bb-3e61-460f-97d9-0d0c0bb2b780
        +dut:
            +type: Simulator
            +configuration: WebServices=CDM & CloudSolution=Telemetry
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test__calibration_v2_alert_get(cdm, udw):
    cdmUtil = CdmTestUtils()
    cdmUtil.set_cdm(cdm)
    responses = [200,304,401,403,404,500,502,503]
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/alerts/{id}","GET")
    print(claimScopes)
    if len(claimScopes) > 0: 
        claimScope = cdmUtil.mapClaimScopeToCdm(cdm, claimScopes[0])
    if "/alerts" in "cdm/calibration/v2/alerts/0" and "service.alert" not in "com.hp.cdm.service.calibration.version.2" and claimScope == cdm.ScopeAlias.PUBLIC:
        print("service alert resource should not be available with public claim scope!")
        assert(0)
    headers = {}
    timeout = 4.0
    ENDPOINT="cdm/calibration/v2/alerts/0"
    resp = cdm.get_raw(ENDPOINT, headers=headers, scope_alias=claimScope, timeout=timeout)
    print(resp.status_code)
    assert resp.status_code == 404
    
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
    +reqid: DUNE-180010
    +timeout:120
    +asset: CDM
    +delivery_team:PDLJobPQ
    +feature_team:PQsolns
    +test_framework: TUF
    +name: test__calibration_v2_alertAction_put
    +test :
        +title: test__calibration_v2_alertAction_put
        +guid: af687cf6-b011-487e-acb9-9856957a89ba
        +dut:
            +type: Simulator
            +configuration: WebServices=CDM & CloudSolution=Telemetry
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test__calibration_v2_alertAction_put(cdm, udw):
    cdmUtil = CdmTestUtils()
    cdmUtil.set_cdm(cdm)
    responses = [204,400,401,403,404,500,502,503]
    claimScope = cdm.ScopeAlias.PUBLIC
    getClaimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/alerts/{id}/action","PUT")
    print(claimScopes)
    if len(claimScopes) > 0: 
        claimScope = cdmUtil.mapClaimScopeToCdm(cdm, claimScopes[0])
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/alerts/{id}/action","GET")
    print(claimScopes)
    if len(claimScopes) > 0: 
        getClaimScope = cdmUtil.mapClaimScopeToCdm(cdm, claimScopes[0])
    headers = {}
    timeout = 4.0
    ENDPOINT = "cdm/calibration/v2/alerts/0/action"
    
    if claimScope == cdm.ScopeAlias.PUBLIC :
        if 401 in responses or 403 in responses:
            print("incorrect response codes 401, 403")
            assert(0)
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test CDM
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-180010
    +timeout:120
    +asset: CDM
    +delivery_team:PDLJobPQ
    +feature_team:PQsolns
    +test_framework: TUF
    +name: test_calibration_v2_configuration_get
    +test :
        +title: test_calibration_v2_configuration_get
        +guid: ab13b9db-b268-429b-8bf8-2b973f7fa5d6
        +dut:
            +type: Simulator
            +configuration: WebServices=CDM & CloudSolution=Telemetry
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_calibration_v2_configuration_get(cdm, udw):

    #Check resource availability
    check = resource_availability_check(cdm, "com.hp.cdm.service.calibration.version.2", "/cdm/calibration/v2", "configuration")
    print(check)
    if check == False:
        print("Resource not available")
        return

    cdmUtil = CdmTestUtils()
    cdmUtil.set_cdm(cdm)
    responses = [200,304,401,403,404,500,502,503]
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/configuration","GET")
    print(claimScopes)
    if len(claimScopes) > 0: 
        claimScope = cdmUtil.mapClaimScopeToCdm(cdm, claimScopes[0])
    if "/alerts" in "cdm/calibration/v2/configuration" and "service.alert" not in "com.hp.cdm.service.calibration.version.2" and claimScope == cdm.ScopeAlias.PUBLIC:
        print("service alert resource should not be available with public claim scope!")
        assert(0)
    headers = {}
    timeout = 4.0
    ENDPOINT="cdm/calibration/v2/configuration"
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
    +reqid: DUNE-180010
    +timeout:120
    +asset: CDM
    +delivery_team:PDLJobPQ
    +feature_team:PQsolns
    +test_framework: TUF
    +name: test_calibration_v2_configuration_patch
    +test :
        +title: test_calibration_v2_configuration_patch
        +guid: ea7e2a82-568c-4ab4-8c9f-7580761c0e5e
        +dut:
            +type: Simulator
            +configuration: WebServices=CDM & CloudSolution=Telemetry
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_calibration_v2_configuration_patch(cdm, udw):

    #Check resource availability
    check = resource_availability_check(cdm, "com.hp.cdm.service.calibration.version.2", "/cdm/calibration/v2", "configuration")
    print(check)
    if check == False:
        print("Resource not available")
        return

    cdmUtil = CdmTestUtils()
    cdmUtil.set_cdm(cdm)
    responses = [204,400,401,403,404,500,502,503]
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/configuration","PATCH")
    print(claimScopes)
    if len(claimScopes) > 0: 
        claimScope = cdmUtil.mapClaimScopeToCdm(cdm, claimScopes[0])
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/configuration","GET")
    print(claimScopes)
    if len(claimScopes) > 0: 
        getClaimScope = cdmUtil.mapClaimScopeToCdm(cdm, claimScopes[0])
    headers = {}
    timeout = 4.0
    ENDPOINT="cdm/calibration/v2/configuration"
    print("----if resource supports data change, get etag -----")
    r0 = cdmUtil.getResource(ENDPOINT, getClaimScope, headers)
    if r0.status_code == 200 : 
        oldEtag = cdmUtil.getETag(r0.headers["ETag"])
        powerCycleCount = oldEtag//1000000 
        seqNum = oldEtag - powerCycleCount * 1000000
        print("power cycle count : {}".format(powerCycleCount))
        print("seq num : {}".format(seqNum))
    print("--------- change the resource with patch ---------")
    #test patch with empty data 
    resource = ""
    r = cdm.patch_raw(ENDPOINT, resource, headers=headers, scope_alias=claimScope, timeout=timeout)
    print(r.status_code)
    assert (r.status_code == 400  or  r.status_code == 404)
    
    #test patch with empty json 
    resource = {
    }
    r = cdm.patch_raw(ENDPOINT, resource, headers=headers, scope_alias=claimScope, timeout=timeout)
    print(r.status_code)
    assert r.status_code == 400
    
    #test patch with data with only version field 
    resource = {
    "version": "2.3.0",
    }
    r = cdm.patch_raw(ENDPOINT, resource, headers=headers, scope_alias=claimScope, timeout=timeout)
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
        #try patch  with public claim scope
        r = cdm.patch_raw(ENDPOINT, resource, headers=headers, scope_alias=cdm.ScopeAlias.PUBLIC, timeout=timeout)
        print(r.status_code)
        assert r.status_code == 403
    print( "--------------------------------------------------------" )

    if claimScope == cdm.ScopeAlias.PUBLIC :
        if 401 in responses or 403 in responses:
            print("Incorrect response codes (401, 403) with PUBLIC claimScope")
            assert(0)
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test CDM
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-180010
    +timeout:120
    +asset: CDM
    +delivery_team:PDLJobPQ
    +feature_team:PQsolns
    +test_framework: TUF
    +name: test_resetAllCalibrationData_get
    +test :
        +title: test_resetAllCalibrationData_get
        +guid: 9db3dc37-b3c4-4134-adc5-0432a8011040
        +dut:
            +type: Simulator
            +configuration: WebServices=CDM & CloudSolution=Telemetry
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_resetAllCalibrationData_get(cdm, udw):

    #Check resource availability
    check = resource_availability_check(cdm, "com.hp.cdm.service.calibration.version.2", "/cdm/calibration/v2", "resetAllCalibrationData")
    print(check)
    if check == False:
        print("Resource not available")
        return

    cdmUtil = CdmTestUtils()
    cdmUtil.set_cdm(cdm)
    responses = [200,304,401,403,404,500,502,503]
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/resetAllCalibrationData","GET")
    print(claimScopes)
    if len(claimScopes) > 0: 
        claimScope = cdmUtil.mapClaimScopeToCdm(cdm, claimScopes[0])
    if "/alerts" in "cdm/calibration/v2/resetAllCalibrationData" and "service.alert" not in "com.hp.cdm.service.calibration.version.2" and claimScope == cdm.ScopeAlias.PUBLIC:
        print("service alert resource should not be available with public claim scope!")
        assert(0)
    headers = {}
    timeout = 4.0
    ENDPOINT="cdm/calibration/v2/resetAllCalibrationData"
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
    +reqid: DUNE-180010
    +timeout:120
    +asset: CDM
    +delivery_team:PDLJobPQ
    +feature_team:PQsolns
    +test_framework: TUF
    +name: test_resetAllCalibrationData_patch
    +test :
        +title: test_resetAllCalibrationData_patch
        +guid: d3991577-4840-43b9-abf3-af7f6b964df3
        +dut:
            +type: Simulator
            +configuration: WebServices=CDM & CloudSolution=Telemetry
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_resetAllCalibrationData_patch(cdm, udw):

    #Check resource availability
    check = resource_availability_check(cdm, "com.hp.cdm.service.calibration.version.2", "/cdm/calibration/v2", "resetAllCalibrationData")
    print(check)
    if check == False:
        print("Resource not available")
        return

    cdmUtil = CdmTestUtils()
    cdmUtil.set_cdm(cdm)
    responses = [202,400,401,403,404,500,502,503]
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/resetAllCalibrationData","PATCH")
    print(claimScopes)
    if len(claimScopes) > 0: 
        claimScope = cdmUtil.mapClaimScopeToCdm(cdm, claimScopes[0])
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/resetAllCalibrationData","GET")
    print(claimScopes)
    if len(claimScopes) > 0: 
        getClaimScope = cdmUtil.mapClaimScopeToCdm(cdm, claimScopes[0])
    headers = {}
    timeout = 4.0
    ENDPOINT="cdm/calibration/v2/resetAllCalibrationData"
    print("----if resource supports data change, get etag -----")
    r0 = cdmUtil.getResource(ENDPOINT, getClaimScope, headers)
    if r0.status_code == 200 : 
        oldEtag = cdmUtil.getETag(r0.headers["ETag"])
        powerCycleCount = oldEtag//1000000 
        seqNum = oldEtag - powerCycleCount * 1000000
        print("power cycle count : {}".format(powerCycleCount))
        print("seq num : {}".format(seqNum))
    print("--------- change the resource with patch ---------")
    #test patch with empty data 
    resource = ""
    r = cdm.patch_raw(ENDPOINT, resource, headers=headers, scope_alias=claimScope, timeout=timeout)
    print(r.status_code)
    assert (r.status_code == 400  or  r.status_code == 404)
    
    #test patch with empty json 
    resource = {
    }
    r = cdm.patch_raw(ENDPOINT, resource, headers=headers, scope_alias=claimScope, timeout=timeout)
    print(r.status_code)
    assert r.status_code == 400
    
    #test patch with data with only version field 
    resource = {
    "version": "2.3.0",
    }
    r = cdm.patch_raw(ENDPOINT, resource, headers=headers, scope_alias=claimScope, timeout=timeout)
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
        #try patch  with public claim scope
        r = cdm.patch_raw(ENDPOINT, resource, headers=headers, scope_alias=cdm.ScopeAlias.PUBLIC, timeout=timeout)
        print(r.status_code)
        assert r.status_code == 403
    print( "--------------------------------------------------------" )

    if claimScope == cdm.ScopeAlias.PUBLIC :
        if 401 in responses or 403 in responses:
            print("Incorrect response codes (401, 403) with PUBLIC claimScope")
            assert(0)
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test CDM
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-180010
    +timeout:120
    +asset: CDM
    +delivery_team:PDLJobPQ
    +feature_team:PQsolns
    +test_framework: TUF
    +name: test_calibration_pubsub_resources
    +test :
        +title: test_calibration_pubsub_resources
        +guid: 1c17f886-9396-442c-a1db-f65a4987e6d3
        +dut:
            +type: Simulator
            +configuration: WebServices=CDM & CloudSolution=Telemetry
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_calibration_pubsub_resources(cdm):
    cdmUtil = CdmTestUtils()
    cdmUtil.set_cdm(cdm)
    print( "--------------------------------------------------------" )
    ENDPOINT_PUBSUB = "cdm/pubsub/v2/subscriptions"
    ENDPOINT_PUBSUB_ONDEMAND = "cdm/pubsub/v2/desires"
    pubsubClientId = "calibration_test"
    cdmUtil.deleteSubscriptions(pubsubClientId)
    pubsubClientInstanceId = "capabilities"
    pubsubClientInstanceId = "status"
    print("----- Check for PubSub " + "com.hp.cdm.service.calibration.version.2.status" +"-----")
    resource = {
        "version": "2.3.0",
        "clientId" : "test",
        "clientInstanceId" : "instanceId_test1",
        "resources" : [
            { "gun" : "com.hp.cdm.service.calibration.version.2.resource.status"}
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
    pubsubClientInstanceId = "statuses"
    print("----- Check for PubSub " + "com.hp.cdm.service.calibration.version.2.statuses" +"-----")
    resource = {
        "version": "2.3.0",
        "clientId" : "test",
        "clientInstanceId" : "instanceId_test1",
        "resources" : [
            { "gun" : "com.hp.cdm.service.calibration.version.2.resource.statuses"}
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
    pubsubClientInstanceId = "calibrate"
    print("----- Check for PubSub " + "com.hp.cdm.service.calibration.version.2.calibrate" +"-----")
    resource = {
        "version": "2.3.0",
        "clientId" : "test",
        "clientInstanceId" : "instanceId_test1",
        "resources" : [
            { "gun" : "com.hp.cdm.service.calibration.version.2.resource.calibrate"}
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
    pubsubClientInstanceId = "calibrationCapabilities"
    pubsubClientInstanceId = "calibrationGroups"
    pubsubClientInstanceId = "calibrationsAction"
    pubsubClientInstanceId = "alerts"
    pubsubClientInstanceId = "alert"
    pubsubClientInstanceId = "alertAction"
    pubsubClientInstanceId = "configuration"
    pubsubClientInstanceId = "resetAllCalibrationData"
    cdmUtil.deleteSubscriptions(pubsubClientId)
    print( "----------------------------------------------------" )
    
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test CDM
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-180010
    +timeout:120
    +asset: CDM
    +delivery_team:PDLJobPQ
    +feature_team:PQsolns
    +test_framework: TUF
    +name: test_calibration_non_pubsub_resources
    +test :
        +title: test_calibration_non_pubsub_resources
        +guid: 0ccb2513-0f4f-437d-932e-87e077922420
        +dut:
            +type: Simulator
            +configuration: WebServices=CDM & CloudSolution=Telemetry
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_calibration_non_pubsub_resources(cdm):
    cdmUtil = CdmTestUtils()
    cdmUtil.set_cdm(cdm)
    print( "-----------------------------------------------------------" )
    ENDPOINT_PUBSUB = "cdm/pubsub/v2/subscriptions"
    ENDPOINT_PUBSUB_ONDEMAND = "cdm/pubsub/v2/desires"
    pubsubClientId = "calibration_test"
    cdmUtil.deleteSubscriptions(pubsubClientId)
    pubsubClientInstanceId = "capabilities"
    print("----- PubSub not supported for this resource " + "com.hp.cdm.service.calibration.version.2.capabilities" +"-----")
    print("----- Check ondemand desire --------")
    expected_status = 204
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/capabilities","GET")
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
        "gun" : "com.hp.cdm.service.calibration.version.2.resource.capabilities",
        "path" : "/calibration/v2//capabilities",
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
    
    pubsubClientInstanceId = "status"
    pubsubClientInstanceId = "statuses"
    pubsubClientInstanceId = "calibrate"
    pubsubClientInstanceId = "calibrationCapabilities"
    print("----- PubSub not supported for this resource " + "com.hp.cdm.service.calibration.version.2.calibrationCapabilities" +"-----")
    print("----- Check ondemand desire --------")
    expected_status = 204
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/calibrationCapabilities","GET")
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
        "gun" : "com.hp.cdm.service.calibration.version.2.resource.calibrationCapabilities",
        "path" : "/calibration/v2//calibrationCapabilities",
        "method" : "get",
        "ackToken" : "onDemandAck",
        }
        ]
    }
    resource["desires"][0]["onDemand"]["clientId"] = pubsubClientId
    resource["desires"][0]["onDemand"]["clientInstanceId"] = pubsubClientInstanceId
    resource["desires"][0]["ackToken"] = "onDemandAck_" + "calibrationCapabilities"
    print(resource)
    headers = {}
    timeout = 4.0
    r = cdm.patch_raw(ENDPOINT_PUBSUB_ONDEMAND, resource, headers=headers, scope_alias=cdm.ScopeAlias.HP_CLOUD_SERVICE, timeout=timeout)
    print(r.status_code)
    assert (r.status_code == expected_status)
    print( "-----------------------------------------" )
    
    pubsubClientInstanceId = "calibrationGroups"
    print("----- PubSub not supported for this resource " + "com.hp.cdm.service.calibration.version.2.calibrationGroups" +"-----")
    print("----- Check ondemand desire --------")
    expected_status = 204
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/calibrationGroups","GET")
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
        "gun" : "com.hp.cdm.service.calibration.version.2.resource.calibrationGroups",
        "path" : "/calibration/v2//calibrationGroups",
        "method" : "get",
        "ackToken" : "onDemandAck",
        }
        ]
    }
    resource["desires"][0]["onDemand"]["clientId"] = pubsubClientId
    resource["desires"][0]["onDemand"]["clientInstanceId"] = pubsubClientInstanceId
    resource["desires"][0]["ackToken"] = "onDemandAck_" + "calibrationGroups"
    print(resource)
    headers = {}
    timeout = 4.0
    r = cdm.patch_raw(ENDPOINT_PUBSUB_ONDEMAND, resource, headers=headers, scope_alias=cdm.ScopeAlias.HP_CLOUD_SERVICE, timeout=timeout)
    print(r.status_code)
    #Check resource availability
    check = resource_availability_check(cdm, "com.hp.cdm.service.calibration.version.2", "/cdm/calibration/v2", "calibrationGroups")
    print(check)
    if check != False:
        assert (r.status_code == expected_status)
    else:
        print("Resource not available")
    print( "-----------------------------------------" )
    
    pubsubClientInstanceId = "calibrationsAction"
    print("----- PubSub not supported for this resource " + "com.hp.cdm.service.calibration.version.2.calibrationsAction" +"-----")
    print("----- Check ondemand desire --------")
    expected_status = 204
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/calibrationsAction","GET")
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
        "gun" : "com.hp.cdm.service.calibration.version.2.resource.calibrationsAction",
        "path" : "/calibration/v2//calibrationsAction",
        "method" : "get",
        "ackToken" : "onDemandAck",
        }
        ]
    }
    resource["desires"][0]["onDemand"]["clientId"] = pubsubClientId
    resource["desires"][0]["onDemand"]["clientInstanceId"] = pubsubClientInstanceId
    resource["desires"][0]["ackToken"] = "onDemandAck_" + "calibrationsAction"
    print(resource)
    headers = {}
    timeout = 4.0
    r = cdm.patch_raw(ENDPOINT_PUBSUB_ONDEMAND, resource, headers=headers, scope_alias=cdm.ScopeAlias.HP_CLOUD_SERVICE, timeout=timeout)
    print(r.status_code)
    #Check resource availability
    check = resource_availability_check(cdm, "com.hp.cdm.service.calibration.version.2", "/cdm/calibration/v2", "calibrationsAction")
    print(check)
    if check != False:
        assert (r.status_code == expected_status)
    else:
        print("Resource not available")
    print( "-----------------------------------------" )
    
    pubsubClientInstanceId = "alerts"
    print("----- PubSub not supported for this resource " + "com.hp.cdm.service.calibration.version.2.alerts" +"-----")
    print("----- Check ondemand desire --------")
    expected_status = 204
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/alerts","GET")
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
        "gun" : "com.hp.cdm.service.calibration.version.2.resource.alerts",
        "path" : "/calibration/v2//alerts",
        "method" : "get",
        "ackToken" : "onDemandAck",
        }
        ]
    }
    resource["desires"][0]["onDemand"]["clientId"] = pubsubClientId
    resource["desires"][0]["onDemand"]["clientInstanceId"] = pubsubClientInstanceId
    resource["desires"][0]["ackToken"] = "onDemandAck_" + "alerts"
    print(resource)
    headers = {}
    timeout = 4.0
    r = cdm.patch_raw(ENDPOINT_PUBSUB_ONDEMAND, resource, headers=headers, scope_alias=cdm.ScopeAlias.HP_CLOUD_SERVICE, timeout=timeout)
    print(r.status_code)
    assert (r.status_code == expected_status)
    print( "-----------------------------------------" )
    
    pubsubClientInstanceId = "alert"
    print("----- PubSub not supported for this resource " + "com.hp.cdm.service.calibration.version.2.alert" +"-----")
    print("----- Check ondemand desire --------")
    expected_status = 204
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/alerts/{id}","GET")
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
        "gun" : "com.hp.cdm.service.calibration.version.2.resource.alert",
        "path" : "/calibration/v2//alerts/{id}",
        "method" : "get",
        "ackToken" : "onDemandAck",
        }
        ]
    }
    resource["desires"][0]["onDemand"]["clientId"] = pubsubClientId
    resource["desires"][0]["onDemand"]["clientInstanceId"] = pubsubClientInstanceId
    resource["desires"][0]["ackToken"] = "onDemandAck_" + "alert"
    print(resource)
    headers = {}
    timeout = 4.0
    r = cdm.patch_raw(ENDPOINT_PUBSUB_ONDEMAND, resource, headers=headers, scope_alias=cdm.ScopeAlias.HP_CLOUD_SERVICE, timeout=timeout)
    print(r.status_code)
    assert (r.status_code == expected_status)
    print( "-----------------------------------------" )
    
    pubsubClientInstanceId = "alertAction"
    print("----- PubSub not supported for this resource " + "com.hp.cdm.service.calibration.version.2.alertAction" +"-----")
    print("----- Check ondemand desire --------")
    expected_status = 204
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/alerts/{id}/action","GET")
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
        "gun" : "com.hp.cdm.service.calibration.version.2.resource.alertAction",
        "path" : "/calibration/v2//alerts/{id}/action",
        "method" : "get",
        "ackToken" : "onDemandAck",
        }
        ]
    }
    resource["desires"][0]["onDemand"]["clientId"] = pubsubClientId
    resource["desires"][0]["onDemand"]["clientInstanceId"] = pubsubClientInstanceId
    resource["desires"][0]["ackToken"] = "onDemandAck_" + "alertAction"
    print(resource)
    headers = {}
    timeout = 4.0
    r = cdm.patch_raw(ENDPOINT_PUBSUB_ONDEMAND, resource, headers=headers, scope_alias=cdm.ScopeAlias.HP_CLOUD_SERVICE, timeout=timeout)
    print(r.status_code)
    #Check resource availability
    check = resource_availability_check(cdm, "com.hp.cdm.service.calibration.version.2", "/cdm/calibration/v2", "alertAction")
    print(check)
    if check != False:
        assert (r.status_code == expected_status)
    else:
        print("Resource not available")
    print( "-----------------------------------------" )
    
    pubsubClientInstanceId = "configuration"
    print("----- PubSub not supported for this resource " + "com.hp.cdm.service.calibration.version.2.configuration" +"-----")
    print("----- Check ondemand desire --------")
    expected_status = 204
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/configuration","GET")
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
        "gun" : "com.hp.cdm.service.calibration.version.2.resource.configuration",
        "path" : "/calibration/v2//configuration",
        "method" : "get",
        "ackToken" : "onDemandAck",
        }
        ]
    }
    resource["desires"][0]["onDemand"]["clientId"] = pubsubClientId
    resource["desires"][0]["onDemand"]["clientInstanceId"] = pubsubClientInstanceId
    resource["desires"][0]["ackToken"] = "onDemandAck_" + "configuration"
    print(resource)
    headers = {}
    timeout = 4.0
    r = cdm.patch_raw(ENDPOINT_PUBSUB_ONDEMAND, resource, headers=headers, scope_alias=cdm.ScopeAlias.HP_CLOUD_SERVICE, timeout=timeout)
    print(r.status_code)
    #Check resource availability
    check = resource_availability_check(cdm, "com.hp.cdm.service.calibration.version.2", "/cdm/calibration/v2", "configuration")
    print(check)
    if check != False:
        assert (r.status_code == expected_status)
    else:
        print("Resource not available")
    print( "-----------------------------------------" )
    
    pubsubClientInstanceId = "resetAllCalibrationData"
    print("----- PubSub not supported for this resource " + "com.hp.cdm.service.calibration.version.2.resetAllCalibrationData" +"-----")
    print("----- Check ondemand desire --------")
    expected_status = 204
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.2","cdm/calibration/v2/resetAllCalibrationData","GET")
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
        "gun" : "com.hp.cdm.service.calibration.version.2.resource.resetAllCalibrationData",
        "path" : "/calibration/v2//resetAllCalibrationData",
        "method" : "get",
        "ackToken" : "onDemandAck",
        }
        ]
    }
    resource["desires"][0]["onDemand"]["clientId"] = pubsubClientId
    resource["desires"][0]["onDemand"]["clientInstanceId"] = pubsubClientInstanceId
    resource["desires"][0]["ackToken"] = "onDemandAck_" + "resetAllCalibrationData"
    print(resource)
    headers = {}
    timeout = 4.0
    r = cdm.patch_raw(ENDPOINT_PUBSUB_ONDEMAND, resource, headers=headers, scope_alias=cdm.ScopeAlias.HP_CLOUD_SERVICE, timeout=timeout)
    print(r.status_code)

    #Check resource availability
    check = resource_availability_check(cdm, "com.hp.cdm.service.calibration.version.2", "/cdm/calibration/v2", "resetAllCalibrationData")
    print(check)
    if check != False:
        assert (r.status_code == expected_status)
    else:
        print("Resource not available")

    print( "-----------------------------------------" )
    
    cdmUtil.deleteSubscriptions(pubsubClientId)
    print( "--------------------------------------------------" )
    

def resource_availability_check(cdm, service_gun, service_path, resource) -> bool:
    """ check if the resource is available in the services discovery """
    resource_supported = False
    servicesDiscovery = cdm.get(cdm.SERVICES_DISCOVERY)
    for service in servicesDiscovery["services"]:
        if service["serviceGun"] == service_gun :
            assert "2.4.0" in service["version"]
            for link in service["links"]:
                print (link["href"])
                if link["href"] == service_path + "/" + resource  :
                    print(link["href"] + " - is supported and discoverable")
                    resource_supported = True
                    return resource_supported
    # if the resource is not found in the services discovery, check if get is supported
    headers = {}
    timeout = 4.0
    if resource_supported == False:
        response = cdm.get_raw(service_path + "/" + resource, headers=headers, timeout=timeout)
        print(response.status_code)
        if response.status_code == 404:
            print(resource + " resource not supported")
    return resource_supported