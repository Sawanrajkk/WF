"""
///////////////////////////////////////////////////////////
/** @file: test_calibration_v1.py
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
    +reqid: DUNE-180009
    +timeout:120
    +asset: CDM
    +delivery_team:PDLJobPQ
    +feature_team:PQsolns
    +test_framework: TUF
    +name: test_calibration_v1_service
    +test :
        +title: test_calibration_v1_service
        +guid: b5cfdb14-9eaf-4671-a33b-aae998e12f42
        +dut:
            +type: Simulator
            +configuration: WebServices=CDM & CloudSolution=Telemetry
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_calibration_v1_service(cdm):
    servicesDiscovery = cdm.get(cdm.SERVICES_DISCOVERY)
    for service in servicesDiscovery["services"]:
        if service["serviceGun"] == "com.hp.cdm.service.calibration.version.1" :
            assert "1.5.0" in service["version"] 
            for link in service["links"]:
                if "hrefTemplate" in link :
                    print(link["hrefTemplate"])
                    print("dynamic resources should not be discoverable!")
                    assert(0)
                else:
                    if link["href"] == "/cdm/calibration/v1/capabilities"  :
                        print(link["href"] + " - is supported and discoverable")
                    if link["href"] == "/cdm/calibration/v1/configuration"  :
                        print(link["href"] + " - is supported and discoverable")
                    if link["href"] == "/cdm/calibration/v1/calibrations"  :
                        print(link["href"] + " - is supported and discoverable")
                    if link["href"] == "/cdm/calibration/v1/calibrationCapabilities"  :
                        print(link["href"] + " - is supported and discoverable")
                    if "/alerts/" in link["href"]  and "service.alert" not in service["serviceGun"]:
                        print("service alert resource should not be discoverable!")
                        assert(0)

                    if link["href"] == "/cdm/calibration/v1/capabilities"  :
                        print(link["href"] + " - supports pubsub")
                    if link["href"] == "/cdm/calibration/v1/calibrations"  :
                        print(link["href"] + " - supports pubsub")
                    if link["href"] == "/cdm/calibration/v1/calibrations/0"  :
                        print(link["href"] + " - supports pubsub")


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test CDM
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-180009
    +timeout:120
    +asset: CDM
    +delivery_team:PDLJobPQ
    +feature_team:PQsolns
    +test_framework: TUF
    +name: test_calibration_v1_resource_capabilities
    +test :
        +title: test_calibration_v1_resource_capabilities
        +guid: c91091a6-9bbd-4805-b127-30b2d9154519
        +dut:
            +type: Simulator
            +configuration: WebServices=CDM & CloudSolution=Telemetry
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_calibration_v1_resource_capabilities(cdm):
    cdmUtil = CdmTestUtils()
    cdmUtil.set_cdm(cdm)
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    print( "-----------------------------------------------------" )

    #check resource availability
    check = resource_availability_check(cdm, "com.hp.cdm.service.calibration.version.1", "/cdm/calibration/v1", "capabilities")
    print(check)
    expectedResponseStatus = 405
    if check == False:
        expectedResponseStatus = 404 #if the resource is not available, then the expected response status should be 404

    #test unsupported methods of capabilities
    timeout = 4.0
    claimScope = cdm.ScopeAlias.PUBLIC
    #trying PUT
    ENDPOINT = "cdm/calibration/v1/capabilities"
    res = {"version": "2.3.0"}
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.1","cdm/calibration/v1/capabilities","PUT")
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
    ENDPOINT = "cdm/calibration/v1/capabilities"
    res = {"version": "2.3.0"}
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.1","cdm/calibration/v1/capabilities","PATCH")
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
    ENDPOINT = "cdm/calibration/v1/capabilities"
    res = {"version": "2.3.0"}
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.1","cdm/calibration/v1/capabilities","POST")
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
    ENDPOINT = "cdm/calibration/v1/capabilities"
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.1","cdm/calibration/v1/capabilities","DELETE")
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
    +reqid: DUNE-180009
    +timeout:120
    +asset: CDM
    +delivery_team:PDLJobPQ
    +feature_team:PQsolns
    +test_framework: TUF
    +name: test_calibration_v1_resource_configuration
    +test :
        +title: test_calibration_v1_resource_configuration
        +guid: 0ec7f7ef-e383-43f0-b54e-27736c69c143
        +dut:
            +type: Simulator
            +configuration: WebServices=CDM & CloudSolution=Telemetry & PrintEngineType=Canon
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_calibration_v1_resource_configuration(cdm):
    cdmUtil = CdmTestUtils()
    cdmUtil.set_cdm(cdm)
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    print( "-----------------------------------------------------" )

    #check resource availability
    check = resource_availability_check(cdm, "com.hp.cdm.service.calibration.version.1", "/cdm/calibration/v1", "configuration")
    print(check)
    expectedResponseStatus = 405
    if check == False:
        expectedResponseStatus = 404 #if the resource is not available, then the expected response status should be 404

    #test unsupported methods of configuration
    timeout = 4.0
    claimScope = cdm.ScopeAlias.PUBLIC
    #trying PUT
    ENDPOINT = "cdm/calibration/v1/configuration"
    res = {"version": "2.3.0"}
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.1","cdm/calibration/v1/configuration","PUT")
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
    ENDPOINT = "cdm/calibration/v1/configuration"
    res = {"version": "2.3.0"}
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.1","cdm/calibration/v1/configuration","POST")
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
    ENDPOINT = "cdm/calibration/v1/configuration"
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.1","cdm/calibration/v1/configuration","DELETE")
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
    +reqid: DUNE-180009
    +timeout:120
    +asset: CDM
    +delivery_team:PDLJobPQ
    +feature_team:PQsolns
    +test_framework: TUF
    +name: test_calibration_resource_calibrations
    +test :
        +title: test_calibration_resource_calibrations
        +guid: 39db8bbc-f153-4801-b33f-56be6235b006
        +dut:
            +type: Simulator
            +configuration: WebServices=CDM & CloudSolution=Telemetry
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_calibration_resource_calibrations(cdm):
    cdmUtil = CdmTestUtils()
    cdmUtil.set_cdm(cdm)
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    print( "-----------------------------------------------------" )

    #check resource availability
    check = resource_availability_check(cdm, "com.hp.cdm.service.calibration.version.1", "/cdm/calibration/v1", "calibrations")
    print(check)
    expectedResponseStatus = 405
    if check == False:
        expectedResponseStatus = 404 #if the resource is not available, then the expected response status should be 404

    #test unsupported methods of calibrations
    timeout = 4.0
    claimScope = cdm.ScopeAlias.PUBLIC
    #trying PUT
    ENDPOINT = "cdm/calibration/v1/calibrations"
    res = {"version": "2.3.0"}
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.1","cdm/calibration/v1/calibrations","PUT")
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
    ENDPOINT = "cdm/calibration/v1/calibrations"
    res = {"version": "2.3.0"}
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.1","cdm/calibration/v1/calibrations","PATCH")
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
    ENDPOINT = "cdm/calibration/v1/calibrations"
    res = {"version": "2.3.0"}
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.1","cdm/calibration/v1/calibrations","POST")
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
    ENDPOINT = "cdm/calibration/v1/calibrations"
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.1","cdm/calibration/v1/calibrations","DELETE")
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
    +reqid: DUNE-180009
    +timeout:120
    +asset: CDM
    +delivery_team:PDLJobPQ
    +feature_team:PQsolns
    +test_framework: TUF
    +name: test_calibration_resource_calibration
    +test :
        +title: test_calibration_resource_calibration
        +guid: 49b41a96-d338-47d6-bc15-c1332f6062e9
        +dut:
            +type: Simulator
            +configuration: WebServices=CDM & CloudSolution=Telemetry
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_calibration_resource_calibration(cdm):
    cdmUtil = CdmTestUtils()
    cdmUtil.set_cdm(cdm)
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    print( "-----------------------------------------------------" )

    #check resource availability
    check = resource_availability_check(cdm, "com.hp.cdm.service.calibration.version.1", "/cdm/calibration/v1", "calibrations")
    print(check)
    expectedResponseStatus = 405
    if check == False:
        expectedResponseStatus = 404 #if the resource is not available, then the expected response status should be 404

    #test unsupported methods of calibration
    timeout = 4.0
    claimScope = cdm.ScopeAlias.PUBLIC
    #trying PUT
    ENDPOINT = "cdm/calibration/v1/calibrations/0"
    res = {"version": "2.3.0"}
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.1","cdm/calibration/v1/calibrations/{calibrationType}","PUT")
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
    ENDPOINT = "cdm/calibration/v1/calibrations/0"
    res = {"version": "2.3.0"}
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.1","cdm/calibration/v1/calibrations/{calibrationType}","POST")
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
    ENDPOINT = "cdm/calibration/v1/calibrations/0"
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.1","cdm/calibration/v1/calibrations/{calibrationType}","DELETE")
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
    +reqid: DUNE-180009
    +timeout:120
    +asset: CDM
    +delivery_team:PDLJobPQ
    +feature_team:PQsolns
    +test_framework: TUF
    +name: test_calibration_v1_resource_calibrationCapabilities
    +test :
        +title: test_calibration_v1_resource_calibrationCapabilities
        +guid: 9992b9a9-4eec-4267-8283-81a3e1715ca2
        +dut:
            +type: Simulator
            +configuration: WebServices=CDM & CloudSolution=Telemetry
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_calibration_v1_resource_calibrationCapabilities(cdm):
    cdmUtil = CdmTestUtils()
    cdmUtil.set_cdm(cdm)
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    print( "-----------------------------------------------------" )

    #check resource availability
    check = resource_availability_check(cdm, "com.hp.cdm.service.calibration.version.1", "/cdm/calibration/v1", "calibrationCapabilities")
    print(check)
    expectedResponseStatus = 405
    if check == False:
        expectedResponseStatus = 404 #if the resource is not available, then the expected response status should be 404

    #test unsupported methods of calibrationCapabilities
    timeout = 4.0
    claimScope = cdm.ScopeAlias.PUBLIC
    #trying PUT
    ENDPOINT = "cdm/calibration/v1/calibrationCapabilities"
    res = {"version": "2.3.0"}
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.1","cdm/calibration/v1/calibrationCapabilities","PUT")
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
    ENDPOINT = "cdm/calibration/v1/calibrationCapabilities"
    res = {"version": "2.3.0"}
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.1","cdm/calibration/v1/calibrationCapabilities","PATCH")
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
    ENDPOINT = "cdm/calibration/v1/calibrationCapabilities"
    res = {"version": "2.3.0"}
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.1","cdm/calibration/v1/calibrationCapabilities","POST")
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
    ENDPOINT = "cdm/calibration/v1/calibrationCapabilities"
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.1","cdm/calibration/v1/calibrationCapabilities","DELETE")
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
    +reqid: DUNE-180009
    +timeout:120
    +asset: CDM
    +delivery_team:PDLJobPQ
    +feature_team:PQsolns
    +test_framework: TUF
    +name: test_calibration_resource_calibrationCapability
    +test :
        +title: test_calibration_resource_calibrationCapability
        +guid: c318485c-2ce0-42d0-9695-3e256098ea86
        +dut:
            +type: Simulator
            +configuration: WebServices=CDM & CloudSolution=Telemetry
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_calibration_resource_calibrationCapability(cdm):
    cdmUtil = CdmTestUtils()
    cdmUtil.set_cdm(cdm)
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    print( "-----------------------------------------------------" )

   #check resource availability
    check = resource_availability_check(cdm, "com.hp.cdm.service.calibration.version.1", "/cdm/calibration/v1", "calibrationCapabilities")
    print(check)
    expectedResponseStatus = 405
    if check == False:
        expectedResponseStatus = 404 #if the resource is not available, then the expected response status should be 404

    #test unsupported methods of calibrationCapability
    timeout = 4.0
    claimScope = cdm.ScopeAlias.PUBLIC
    #trying PUT
    ENDPOINT = "cdm/calibration/v1/calibrationCapabilities/0"
    res = {"version": "2.3.0"}
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.1","cdm/calibration/v1/calibrationCapabilities/{calibrationType}","PUT")
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
    ENDPOINT = "cdm/calibration/v1/calibrationCapabilities/0"
    res = {"version": "2.3.0"}
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.1","cdm/calibration/v1/calibrationCapabilities/{calibrationType}","PATCH")
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
    ENDPOINT = "cdm/calibration/v1/calibrationCapabilities/0"
    res = {"version": "2.3.0"}
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.1","cdm/calibration/v1/calibrationCapabilities/{calibrationType}","POST")
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
    ENDPOINT = "cdm/calibration/v1/calibrationCapabilities/0"
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.1","cdm/calibration/v1/calibrationCapabilities/{calibrationType}","DELETE")
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
    +reqid: DUNE-180009
    +timeout:120
    +asset: CDM
    +delivery_team:PDLJobPQ
    +feature_team:PQsolns
    +test_framework: TUF
    +name: test_calibration_v1_resource_calibrationsAction
    +test :
        +title: test_calibration_v1_resource_calibrationsAction
        +guid: 240cf2b7-bf1d-4409-a801-40b881f4c69f
        +dut:
            +type: Simulator
            +configuration: WebServices=CDM & CloudSolution=Telemetry
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_calibration_v1_resource_calibrationsAction(cdm):
    cdmUtil = CdmTestUtils()
    cdmUtil.set_cdm(cdm)
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    print( "-----------------------------------------------------" )

   #check resource availability
    check = resource_availability_check(cdm, "com.hp.cdm.service.calibration.version.1", "/cdm/calibration/v1", "calibrationsAction")
    print(check)
    if check == False:
        print("Resource not available")
        return

    #test unsupported methods of calibrationsAction
    timeout = 4.0
    claimScope = cdm.ScopeAlias.PUBLIC
    #trying GET
    ENDPOINT = "cdm/calibration/v1/calibrationsAction"
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.1","cdm/calibration/v1/calibrationsAction","GET")
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
    ENDPOINT = "cdm/calibration/v1/calibrationsAction"
    res = {"version": "2.3.0"}
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.1","cdm/calibration/v1/calibrationsAction","PUT")
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
    ENDPOINT = "cdm/calibration/v1/calibrationsAction"
    res = {"version": "2.3.0"}
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.1","cdm/calibration/v1/calibrationsAction","POST")
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
    ENDPOINT = "cdm/calibration/v1/calibrationsAction"
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.1","cdm/calibration/v1/calibrationsAction","DELETE")
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
    +reqid: DUNE-180009
    +timeout:120
    +asset: CDM
    +delivery_team:PDLJobPQ
    +feature_team:PQsolns
    +test_framework: TUF
    +name: test_calibration_v1_resource_alerts
    +test :
        +title: test_calibration_v1_resource_alerts
        +guid: f8b5b804-6ff1-4d1d-84f4-4e27723535da
        +dut:
            +type: Simulator
            +configuration: WebServices=CDM & CloudSolution=Telemetry
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_calibration_v1_resource_alerts(cdm):
    cdmUtil = CdmTestUtils()
    cdmUtil.set_cdm(cdm)
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    print( "-----------------------------------------------------" )

   #check resource availability
    check = resource_availability_check(cdm, "com.hp.cdm.service.calibration.version.1", "/cdm/calibration/v1", "alerts")
    print(check)
    if check == False:
        print("Resource not available")
        return

    #test unsupported methods of alerts
    timeout = 4.0
    claimScope = cdm.ScopeAlias.PUBLIC
    #trying PUT
    ENDPOINT = "cdm/calibration/v1/alerts"
    res = {"version": "2.3.0"}
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.1","cdm/calibration/v1/alerts","PUT")
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
    ENDPOINT = "cdm/calibration/v1/alerts"
    res = {"version": "2.3.0"}
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.1","cdm/calibration/v1/alerts","PATCH")
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
    ENDPOINT = "cdm/calibration/v1/alerts"
    res = {"version": "2.3.0"}
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.1","cdm/calibration/v1/alerts","POST")
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
    ENDPOINT = "cdm/calibration/v1/alerts"
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.1","cdm/calibration/v1/alerts","DELETE")
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
    +reqid: DUNE-180009
    +timeout:120
    +asset: CDM
    +delivery_team:PDLJobPQ
    +feature_team:PQsolns
    +test_framework: TUF
    +name: test_calibration_v1_resource_alert
    +test :
        +title: test_calibration_v1_resource_alert
        +guid: 1a0c7bb8-8a31-4757-bfa6-54bc4dfa3e00
        +dut:
            +type: Simulator
            +configuration: WebServices=CDM & CloudSolution=Telemetry
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_calibration_v1_resource_alert(cdm):
    cdmUtil = CdmTestUtils()
    cdmUtil.set_cdm(cdm)
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    print( "-----------------------------------------------------" )

    #check resource availability
    check = resource_availability_check(cdm, "com.hp.cdm.service.calibration.version.1", "/cdm/calibration/v1", "alerts")
    print(check)
    if check == False:
        print("Resource not available")
        return

    #test unsupported methods of alert
    timeout = 4.0
    claimScope = cdm.ScopeAlias.PUBLIC
    #trying PUT
    ENDPOINT = "cdm/calibration/v1/alerts/0"
    res = {"version": "2.3.0"}
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.1","cdm/calibration/v1/alerts/{id}","PUT")
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
    ENDPOINT = "cdm/calibration/v1/alerts/0"
    res = {"version": "2.3.0"}
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.1","cdm/calibration/v1/alerts/{id}","PATCH")
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
    ENDPOINT = "cdm/calibration/v1/alerts/0"
    res = {"version": "2.3.0"}
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.1","cdm/calibration/v1/alerts/{id}","POST")
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
    ENDPOINT = "cdm/calibration/v1/alerts/0"
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.1","cdm/calibration/v1/alerts/{id}","DELETE")
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
    +reqid: DUNE-180009
    +timeout:120
    +asset: CDM
    +delivery_team:PDLJobPQ
    +feature_team:PQsolns
    +test_framework: TUF
    +name: test_calibration_v1_resource_alertAction
    +test :
        +title: test_calibration_v1_resource_alertAction
        +guid: 2c8a6283-9645-4a51-9802-23afa5be31ea
        +dut:
            +type: Simulator
            +configuration: WebServices=CDM & CloudSolution=Telemetry
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_calibration_v1_resource_alertAction(cdm):
    cdmUtil = CdmTestUtils()
    cdmUtil.set_cdm(cdm)
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    print( "-----------------------------------------------------" )

    #check resource availability
    check = resource_availability_check(cdm, "com.hp.cdm.service.calibration.version.1", "/cdm/calibration/v1", "alerts")
    print(check)
    if check == False:
        print("Resource not available")
        return

    #test unsupported methods of alertAction
    timeout = 4.0
    claimScope = cdm.ScopeAlias.PUBLIC
    #trying GET
    ENDPOINT = "cdm/calibration/v1/alerts/0/action"
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.1","cdm/calibration/v1/alerts/{id}/action","GET")
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
    ENDPOINT = "cdm/calibration/v1/alerts/0/action"
    res = {"version": "2.3.0"}
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.1","cdm/calibration/v1/alerts/{id}/action","PATCH")
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
    ENDPOINT = "cdm/calibration/v1/alerts/0/action"
    res = {"version": "2.3.0"}
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.1","cdm/calibration/v1/alerts/{id}/action","POST")
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
    ENDPOINT = "cdm/calibration/v1/alerts/0/action"
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.1","cdm/calibration/v1/alerts/{id}/action","DELETE")
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
    +reqid: DUNE-180009
    +timeout:120
    +asset: CDM
    +delivery_team:PDLJobPQ
    +feature_team:PQsolns
    +test_framework: TUF
    +name: test_calibration_capabilities_get
    +test :
        +title: test_calibration_capabilities_get
        +guid: cf30288f-b863-47f9-b2da-103d50fc7e41
        +dut:
            +type: Simulator
            +configuration: WebServices=CDM & CloudSolution=Telemetry
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_calibration_capabilities_get(cdm, udw):
    #check resource availability
    check = resource_availability_check(cdm, "com.hp.cdm.service.calibration.version.1", "/cdm/calibration/v1", "capabilities")
    print(check)
    if check == False:
        print("Resource not available")
        return

    cdmUtil = CdmTestUtils()
    cdmUtil.set_cdm(cdm)
    # claimScope = cdm.ScopeAlias.PUBLIC
    # claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    # claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.1","cdm/calibration/v1/capabilities","GET")
    # print(claimScopes)
    # if len(claimScopes) > 0: 
    #     claimScope = cdmUtil.mapClaimScopeToCdm(cdm, claimScopes[0])
    claimScope = cdm.ScopeAlias.PUBLIC # as of now, there is a bug with cdmUtil.getClaimScopes so setting PUBLIC since it is not getting the match correctly
    if "/alerts/" in "cdm/calibration/v1/capabilities" and "service.alert" not in "com.hp.cdm.service.calibration.version.1" and claimScope == cdm.ScopeAlias.PUBLIC:
        print("service alert resource should not be available with public claim scope!")
        assert(0)
    headers = {}
    timeout = 4.0
    ENDPOINT="cdm/calibration/v1/capabilities"
    resp = cdm.get_raw(ENDPOINT, headers=headers, scope_alias=claimScope, timeout=timeout)
    print(resp.status_code)
    assert resp.status_code == 200

    if claimScope != cdm.ScopeAlias.PUBLIC :
        #try get  with public claim scope
        r = cdm.get_raw(ENDPOINT, headers=headers, scope_alias=cdm.ScopeAlias.PUBLIC, timeout=timeout)
        print(r.status_code)
        assert r.status_code == 403
    print( "--------------------------------------------------------" )

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
    +reqid: DUNE-180009
    +timeout:120
    +asset: CDM
    +delivery_team:PDLJobPQ
    +feature_team:PQsolns
    +test_framework: TUF
    +name: test_calibration_configuration_get
    +test :
        +title: test_calibration_configuration_get
        +guid: 533b37df-89d6-463c-8cc7-0ccec887566c
        +dut:
            +type: Simulator
            +configuration: WebServices=CDM & CloudSolution=Telemetry & PrintEngineType=Canon
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_calibration_configuration_get(cdm, udw):

    #Check resource availability
    check = resource_availability_check(cdm, "com.hp.cdm.service.calibration.version.1", "/cdm/calibration/v1", "configuration")
    print(check)
    if check == False:
        print("Resource not available")
        return

    cdmUtil = CdmTestUtils()
    cdmUtil.set_cdm(cdm)
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.1","cdm/calibration/v1/configuration","GET")
    print(claimScopes)
    if len(claimScopes) > 0: 
        claimScope = cdmUtil.mapClaimScopeToCdm(cdm, claimScopes[0])
    if "/alerts/" in "cdm/calibration/v1/configuration" and "service.alert" not in "com.hp.cdm.service.calibration.version.1" and claimScope == cdm.ScopeAlias.PUBLIC:
        print("service alert resource should not be available with public claim scope!")
        assert(0)
    headers = {}
    timeout = 4.0
    ENDPOINT="cdm/calibration/v1/configuration"
    resp = cdm.get_raw(ENDPOINT, headers=headers, scope_alias=claimScope, timeout=timeout)
    print(resp.status_code)
    assert resp.status_code == 200

    if claimScope != cdm.ScopeAlias.PUBLIC :
        #try get  with public claim scope
        r = cdm.get_raw(ENDPOINT, headers=headers, scope_alias=cdm.ScopeAlias.PUBLIC, timeout=timeout)
        print(r.status_code)
        assert r.status_code == 403
    print( "--------------------------------------------------------" )

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test CDM
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-180009
    +timeout:120
    +asset: CDM
    +delivery_team:PDLJobPQ
    +feature_team:PQsolns
    +test_framework: TUF
    +name: test_calibration_configuration_patch
    +test :
        +title: test_calibration_configuration_patch
        +guid: 721b9c4e-4658-479f-8dfc-d87221d37a9c
        +dut:
            +type: Simulator
            +configuration: WebServices=CDM & CloudSolution=Telemetry & PrintEngineType=Canon
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_calibration_configuration_patch(cdm, udw):

    #Check resource availability
    check = resource_availability_check(cdm, "com.hp.cdm.service.calibration.version.1", "/cdm/calibration/v1", "configuration")
    print(check)
    if check == False:
        print("Resource not available")
        return

    cdmUtil = CdmTestUtils()
    cdmUtil.set_cdm(cdm)
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.1","cdm/calibration/v1/configuration","PATCH")
    print(claimScopes)
    if len(claimScopes) > 0: 
        claimScope = cdmUtil.mapClaimScopeToCdm(cdm, claimScopes[0])
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.1","cdm/calibration/v1/configuration","GET")
    print(claimScopes)
    if len(claimScopes) > 0: 
        getClaimScope = cdmUtil.mapClaimScopeToCdm(cdm, claimScopes[0])
    headers = {}
    timeout = 4.0
    ENDPOINT="cdm/calibration/v1/configuration"
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

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test CDM
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-180009
    +timeout:120
    +asset: CDM
    +delivery_team:PDLJobPQ
    +feature_team:PQsolns
    +test_framework: TUF
    +name: test_calibrations_get
    +test :
        +title: test_calibrations_get
        +guid: 22974d0a-9c70-4c55-b926-faf2a259eea4
        +dut:
            +type: Simulator
            +configuration: WebServices=CDM & CloudSolution=Telemetry
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_calibrations_get(cdm, udw):

    #Check resource availability
    check = resource_availability_check(cdm, "com.hp.cdm.service.calibration.version.1", "/cdm/calibration/v1", "calibrations")
    print(check)
    if check == False:
        print("Resource not available")
        return

    cdmUtil = CdmTestUtils()
    cdmUtil.set_cdm(cdm)
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.1","cdm/calibration/v1/calibrations","GET")
    print(claimScopes)
    if len(claimScopes) > 0: 
        claimScope = cdmUtil.mapClaimScopeToCdm(cdm, claimScopes[0])
    if "/alerts/" in "cdm/calibration/v1/calibrations" and "service.alert" not in "com.hp.cdm.service.calibration.version.1" and claimScope == cdm.ScopeAlias.PUBLIC:
        print("service alert resource should not be available with public claim scope!")
        assert(0)
    headers = {}
    timeout = 4.0
    ENDPOINT="cdm/calibration/v1/calibrations"
    resp = cdm.get_raw(ENDPOINT, headers=headers, scope_alias=claimScope, timeout=timeout)
    print(resp.status_code)
    assert resp.status_code == 200
    
    if claimScope != cdm.ScopeAlias.PUBLIC :
        #try get  with public claim scope
        r = cdm.get_raw(ENDPOINT, headers=headers, scope_alias=cdm.ScopeAlias.PUBLIC, timeout=timeout)
        print(r.status_code)
        assert r.status_code == 403
    print( "--------------------------------------------------------" )

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
    +reqid: DUNE-180009
    +timeout:120
    +asset: CDM
    +delivery_team:PDLJobPQ
    +feature_team:PQsolns
    +test_framework: TUF
    +name: test_calibration_get
    +test :
        +title: test_calibration_get
        +guid: 41f6bea8-9575-4375-a3da-cdab34402ef1
        +dut:
            +type: Simulator
            +configuration: WebServices=CDM & CloudSolution=Telemetry
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_calibration_get(cdm, udw):

    #Check resource availability
    check = resource_availability_check(cdm, "com.hp.cdm.service.calibration.version.1", "/cdm/calibration/v1", "calibrations")
    print(check)
    if check == False:
        print("Resource not available")
        return

    cdmUtil = CdmTestUtils()
    cdmUtil.set_cdm(cdm)
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.1","cdm/calibration/v1/calibrations/{calibrationType}","GET")
    print(claimScopes)
    if len(claimScopes) > 0: 
        claimScope = cdmUtil.mapClaimScopeToCdm(cdm, claimScopes[0])
    if "/alerts/" in "cdm/calibration/v1/calibrations/0" and "service.alert" not in "com.hp.cdm.service.calibration.version.1" and claimScope == cdm.ScopeAlias.PUBLIC:
        print("service alert resource should not be available with public claim scope!")
        assert(0)
    headers = {}
    timeout = 4.0
    ENDPOINT="cdm/calibration/v1/calibrations/0"
    resp = cdm.get_raw(ENDPOINT, headers=headers, scope_alias=claimScope, timeout=timeout)
    print(resp.status_code)
    assert resp.status_code == 404
    
    if claimScope != cdm.ScopeAlias.PUBLIC :
        #try get  with public claim scope
        r = cdm.get_raw(ENDPOINT, headers=headers, scope_alias=cdm.ScopeAlias.PUBLIC, timeout=timeout)
        print(r.status_code)
        assert r.status_code == 403
    print( "--------------------------------------------------------" )

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
    +reqid: DUNE-180009
    +timeout:120
    +asset: CDM
    +delivery_team:PDLJobPQ
    +feature_team:PQsolns
    +test_framework: TUF
    +name: test_calibration_patch
    +test :
        +title: test_calibration_patch
        +guid: 07d36837-a5e3-4481-9b06-9b7f7c4272d3
        +dut:
            +type: Simulator
            +configuration: WebServices=CDM & CloudSolution=Telemetry
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_calibration_patch(cdm, udw):

    #Check resource availability
    check = resource_availability_check(cdm, "com.hp.cdm.service.calibration.version.1", "/cdm/calibration/v1", "calibrations")
    print(check)
    if check == False:
        print("Resource not available")
        return

    cdmUtil = CdmTestUtils()
    cdmUtil.set_cdm(cdm)
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.1","cdm/calibration/v1/calibrations/{calibrationType}","PATCH")
    print(claimScopes)
    if len(claimScopes) > 0: 
        claimScope = cdmUtil.mapClaimScopeToCdm(cdm, claimScopes[0])
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.1","cdm/calibration/v1/calibrations/{calibrationType}","GET")
    print(claimScopes)
    if len(claimScopes) > 0: 
        getClaimScope = cdmUtil.mapClaimScopeToCdm(cdm, claimScopes[0])
    headers = {}
    timeout = 4.0
    ENDPOINT="cdm/calibration/v1/calibrations/0"
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
    assert r.status_code == 404
    
    #test patch with data with only version field 
    resource = {
    "version": "2.3.0",
    }
    r = cdm.patch_raw(ENDPOINT, resource, headers=headers, scope_alias=claimScope, timeout=timeout)
    print(r.status_code)
    assert r.status_code == 404
    
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

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test CDM
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-180009
    +timeout:120
    +asset: CDM
    +delivery_team:PDLJobPQ
    +feature_team:PQsolns
    +test_framework: TUF
    +name: test_calibration_v1_calibrationCapabilities_get
    +test :
        +title: test_calibration_v1_calibrationCapabilities_get
        +guid: c26e694c-9a09-4069-8bef-39b21b0c43f1
        +dut:
            +type: Simulator
            +configuration: WebServices=CDM & CloudSolution=Telemetry
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_calibration_v1_calibrationCapabilities_get(cdm, udw):

    #Check resource availability
    check = resource_availability_check(cdm, "com.hp.cdm.service.calibration.version.1", "/cdm/calibration/v1", "calibrationCapabilities")
    print(check)
    if check == False:
        print("Resource not available")
        return

    cdmUtil = CdmTestUtils()
    cdmUtil.set_cdm(cdm)
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.1","cdm/calibration/v1/calibrationCapabilities","GET")
    print(claimScopes)
    if len(claimScopes) > 0: 
        claimScope = cdmUtil.mapClaimScopeToCdm(cdm, claimScopes[0])
    if "/alerts/" in "cdm/calibration/v1/calibrationCapabilities" and "service.alert" not in "com.hp.cdm.service.calibration.version.1" and claimScope == cdm.ScopeAlias.PUBLIC:
        print("service alert resource should not be available with public claim scope!")
        assert(0)
    headers = {}
    timeout = 4.0
    ENDPOINT="cdm/calibration/v1/calibrationCapabilities"
    resp = cdm.get_raw(ENDPOINT, headers=headers, scope_alias=claimScope, timeout=timeout)
    print(resp.status_code)
    assert resp.status_code == 200
    
    if claimScope != cdm.ScopeAlias.PUBLIC :
        #try get  with public claim scope
        r = cdm.get_raw(ENDPOINT, headers=headers, scope_alias=cdm.ScopeAlias.PUBLIC, timeout=timeout)
        print(r.status_code)
        assert r.status_code == 403
    print( "--------------------------------------------------------" )

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test CDM
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-180009
    +timeout:120
    +asset: CDM
    +delivery_team:PDLJobPQ
    +feature_team:PQsolns
    +test_framework: TUF
    +name: test_calibrationCapability_get
    +test :
        +title: test_calibrationCapability_get
        +guid: df1bd986-a161-4d50-945a-d39cc84094c6
        +dut:
            +type: Simulator
            +configuration: WebServices=CDM & CloudSolution=Telemetry
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_calibrationCapability_get(cdm, udw):

    #Check resource availability
    check = resource_availability_check(cdm, "com.hp.cdm.service.calibration.version.1", "/cdm/calibration/v1", "calibrationCapabilities")
    print(check)
    if check == False:
        print("Resource not available")
        return

    cdmUtil = CdmTestUtils()
    cdmUtil.set_cdm(cdm)
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.1","cdm/calibration/v1/calibrationCapabilities/{calibrationType}","GET")
    print(claimScopes)
    if len(claimScopes) > 0: 
        claimScope = cdmUtil.mapClaimScopeToCdm(cdm, claimScopes[0])
    if "/alerts/" in "cdm/calibration/v1/calibrationCapabilities/0" and "service.alert" not in "com.hp.cdm.service.calibration.version.1" and claimScope == cdm.ScopeAlias.PUBLIC:
        print("service alert resource should not be available with public claim scope!")
        assert(0)
    headers = {}
    timeout = 4.0
    ENDPOINT="cdm/calibration/v1/calibrationCapabilities/0"
    resp = cdm.get_raw(ENDPOINT, headers=headers, scope_alias=claimScope, timeout=timeout)
    print(resp.status_code)
    assert resp.status_code == 404
    
    if claimScope != cdm.ScopeAlias.PUBLIC :
        #try get  with public claim scope
        r = cdm.get_raw(ENDPOINT, headers=headers, scope_alias=cdm.ScopeAlias.PUBLIC, timeout=timeout)
        print(r.status_code)
        assert r.status_code == 403
    print( "--------------------------------------------------------" )

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test CDM
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-180009
    +timeout:120
    +asset: CDM
    +delivery_team:PDLJobPQ
    +feature_team:PQsolns
    +test_framework: TUF
    +name: test_calibration_v1_calibrationsAction_patch
    +test :
        +title: test_calibration_v1_calibrationsAction_patch
        +guid: 664e8d6b-d6bb-4b7c-8430-3b826bfcf4cb
        +dut:
            +type: Simulator
            +configuration: WebServices=CDM & CloudSolution=Telemetry
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_calibration_v1_calibrationsAction_patch(cdm, udw):

    #Check resource availability
    check = resource_availability_check(cdm, "com.hp.cdm.service.calibration.version.1", "/cdm/calibration/v1", "calibrationsAction")
    print(check)
    if check == False:
        print("Resource not available")
        return

    cdmUtil = CdmTestUtils()
    cdmUtil.set_cdm(cdm)
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.1","cdm/calibration/v1/calibrationsAction","PATCH")
    print(claimScopes)
    if len(claimScopes) > 0: 
        claimScope = cdmUtil.mapClaimScopeToCdm(cdm, claimScopes[0])
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.1","cdm/calibration/v1/calibrationsAction","GET")
    print(claimScopes)
    if len(claimScopes) > 0: 
        getClaimScope = cdmUtil.mapClaimScopeToCdm(cdm, claimScopes[0])
    headers = {}
    timeout = 4.0
    ENDPOINT="cdm/calibration/v1/calibrationsAction"
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

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test CDM
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-180009
    +timeout:120
    +asset: CDM
    +delivery_team:PDLJobPQ
    +feature_team:PQsolns
    +test_framework: TUF
    +name: test_calibration_alerts_get
    +test :
        +title: test_calibration_alerts_get
        +guid: 28697c53-2407-474e-88f5-6fc736d6d93d
        +dut:
            +type: Simulator
            +configuration: WebServices=CDM & CloudSolution=Telemetry
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_calibration_alerts_get(cdm, udw):

    #Check resource availability
    check = resource_availability_check(cdm, "com.hp.cdm.service.calibration.version.1", "/cdm/calibration/v1", "alerts")
    print(check)
    if check == False:
        print("Resource not available")
        return

    cdmUtil = CdmTestUtils()
    cdmUtil.set_cdm(cdm)
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.1","cdm/calibration/v1/alerts","GET")
    print(claimScopes)
    if len(claimScopes) > 0: 
        claimScope = cdmUtil.mapClaimScopeToCdm(cdm, claimScopes[0])
    if "/alerts/" in "cdm/calibration/v1/alerts" and "service.alert" not in "com.hp.cdm.service.calibration.version.1" and claimScope == cdm.ScopeAlias.PUBLIC:
        print("service alert resource should not be available with public claim scope!")
        assert(0)
    headers = {}
    timeout = 4.0
    ENDPOINT="cdm/calibration/v1/alerts"
    resp = cdm.get_raw(ENDPOINT, headers=headers, scope_alias=claimScope, timeout=timeout)
    print(resp.status_code)
    assert resp.status_code == 200
    
    if claimScope != cdm.ScopeAlias.PUBLIC :
        #try get  with public claim scope
        r = cdm.get_raw(ENDPOINT, headers=headers, scope_alias=cdm.ScopeAlias.PUBLIC, timeout=timeout)
        print(r.status_code)
        assert r.status_code == 403
    print( "--------------------------------------------------------" )

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test CDM
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-180009
    +timeout:120
    +asset: CDM
    +delivery_team:PDLJobPQ
    +feature_team:PQsolns
    +test_framework: TUF
    +name: test_calibration_alert_get
    +test :
        +title: test_calibration_alert_get
        +guid: ed753a97-69cb-4a4b-a296-36e2e6cb88a1
        +dut:
            +type: Simulator
            +configuration: WebServices=CDM & CloudSolution=Telemetry
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_calibration_alert_get(cdm, udw):

    #Check resource availability
    check = resource_availability_check(cdm, "com.hp.cdm.service.calibration.version.1", "/cdm/calibration/v1", "alerts")
    print(check)
    if check == False:
        print("Resource not available")
        return

    cdmUtil = CdmTestUtils()
    cdmUtil.set_cdm(cdm)
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.1","cdm/calibration/v1/alerts/{id}","GET")
    print(claimScopes)
    if len(claimScopes) > 0: 
        claimScope = cdmUtil.mapClaimScopeToCdm(cdm, claimScopes[0])
    if "/alerts/" in "cdm/calibration/v1/alerts/0" and "service.alert" not in "com.hp.cdm.service.calibration.version.1" and claimScope == cdm.ScopeAlias.PUBLIC:
        print("service alert resource should not be available with public claim scope!")
        assert(0)
    headers = {}
    timeout = 4.0
    ENDPOINT="cdm/calibration/v1/alerts/0"
    resp = cdm.get_raw(ENDPOINT, headers=headers, scope_alias=claimScope, timeout=timeout)
    print(resp.status_code)
    assert resp.status_code == 404
    
    if claimScope != cdm.ScopeAlias.PUBLIC :
        #try get  with public claim scope
        r = cdm.get_raw(ENDPOINT, headers=headers, scope_alias=cdm.ScopeAlias.PUBLIC, timeout=timeout)
        print(r.status_code)
        assert r.status_code == 403
    print( "--------------------------------------------------------" )

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
    +reqid: DUNE-180009
    +timeout:120
    +asset: CDM
    +delivery_team:PDLJobPQ
    +feature_team:PQsolns
    +test_framework: TUF
    +name: test_calibration_alertAction_put
    +test :
        +title: test_calibration_alertAction_put
        +guid: 6a5047f6-e4ae-4b20-9208-8912237b74af
        +dut:
            +type: Simulator
            +configuration: WebServices=CDM & CloudSolution=Telemetry
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_calibration_alertAction_put(cdm, udw):
    cdmUtil = CdmTestUtils()
    cdmUtil.set_cdm(cdm)
    claimScope = cdm.ScopeAlias.PUBLIC
    getClaimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.1","cdm/calibration/v1/alerts/{id}/action","PUT")
    print(claimScopes)
    if len(claimScopes) > 0: 
        claimScope = cdmUtil.mapClaimScopeToCdm(cdm, claimScopes[0])
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.1","cdm/calibration/v1/alerts/{id}/action","GET")
    print(claimScopes)
    if len(claimScopes) > 0: 
        getClaimScope = cdmUtil.mapClaimScopeToCdm(cdm, claimScopes[0])
    headers = {}
    timeout = 4.0
    ENDPOINT = "cdm/calibration/v1/alerts/0/action"
    
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test CDM
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-180009
    +timeout:120
    +asset: CDM
    +delivery_team:PDLJobPQ
    +feature_team:PQsolns
    +test_framework: TUF
    +name: test_calibration_v1_pubsub_resources
    +test :
        +title: test_calibration_v1_pubsub_resources
        +guid: 5ed6392d-538f-4d63-b2a6-b4acba6be5c9
        +dut:
            +type: Simulator
            +configuration: WebServices=CDM & CloudSolution=Telemetry
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_calibration_v1_pubsub_resources(cdm):
    cdmUtil = CdmTestUtils()
    cdmUtil.set_cdm(cdm)
    print( "--------------------------------------------------------" )
    ENDPOINT_PUBSUB = "cdm/pubsub/v2/subscriptions"
    ENDPOINT_PUBSUB_ONDEMAND = "cdm/pubsub/v2/desires"
    pubsubClientId = "calibration_test"
    cdmUtil.deleteSubscriptions(pubsubClientId)
    pubsubClientInstanceId = "capabilities"
    print("----- Check for PubSub " + "com.hp.cdm.service.calibration.version.1.capabilities" +"-----")
    #Check resource availability
    check = resource_availability_check(cdm, "com.hp.cdm.service.calibration.version.1", "/cdm/calibration/v1", "capabilities")
    print(check)
    if check == False:
        print("Resource not available")
        return

    resource = {
        "version": "2.3.0",
        "clientId" : "test",
        "clientInstanceId" : "instanceId_test1",
        "resources" : [
            { "gun" : "com.hp.cdm.service.calibration.version.1.resource.capabilities"}
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
    pubsubClientInstanceId = "configuration"
    pubsubClientInstanceId = "calibrations"
    print("----- Check for PubSub " + "com.hp.cdm.service.calibration.version.1.calibrations" +"-----")
    #Check resource availability
    check = resource_availability_check(cdm, "com.hp.cdm.service.calibration.version.1", "/cdm/calibration/v1", "calibrations")
    print(check)
    if check == False:
        print("Resource not available")
        return

    resource = {
        "version": "2.3.0",
        "clientId" : "test",
        "clientInstanceId" : "instanceId_test1",
        "resources" : [
            { "gun" : "com.hp.cdm.service.calibration.version.1.resource.calibrations"}
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
    pubsubClientInstanceId = "calibration"
    print("----- Check for PubSub " + "com.hp.cdm.service.calibration.version.1.calibration" +"-----")
    #Check resource availability
    check = resource_availability_check(cdm, "com.hp.cdm.service.calibration.version.1", "/cdm/calibration/v1", "calibration")
    print(check)
    if check == False:
        print("Resource not available")
        return

    resource = {
        "version": "2.3.0",
        "clientId" : "test",
        "clientInstanceId" : "instanceId_test1",
        "resources" : [
            { "gun" : "com.hp.cdm.service.calibration.version.1.resource.calibration"}
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
    pubsubClientInstanceId = "calibrationCapability"
    pubsubClientInstanceId = "calibrationsAction"
    pubsubClientInstanceId = "alerts"
    pubsubClientInstanceId = "alert"
    pubsubClientInstanceId = "alertAction"
    cdmUtil.deleteSubscriptions(pubsubClientId)
    print( "----------------------------------------------------" )
    
"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test CDM
    +test_tier: 1
    +is_manual: False
    +test_classification:System
    +reqid: DUNE-180009
    +timeout:120
    +asset: CDM
    +delivery_team:PDLJobPQ
    +feature_team:PQsolns
    +test_framework: TUF
    +name: test_calibration_v1_non_pubsub_resources
    +test :
        +title: test_calibration_v1_non_pubsub_resources
        +guid: f0809684-2687-475f-9fea-3babddfe54f6
        +dut:
            +type: Simulator
            +configuration: WebServices=CDM & CloudSolution=Telemetry
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_calibration_v1_non_pubsub_resources(cdm):
    cdmUtil = CdmTestUtils()
    cdmUtil.set_cdm(cdm)
    print( "-----------------------------------------------------------" )
    ENDPOINT_PUBSUB = "cdm/pubsub/v2/subscriptions"
    ENDPOINT_PUBSUB_ONDEMAND = "cdm/pubsub/v2/desires"
    pubsubClientId = "calibration_test"
    cdmUtil.deleteSubscriptions(pubsubClientId)
    pubsubClientInstanceId = "capabilities"
    pubsubClientInstanceId = "configuration"
    print("----- PubSub not supported for this resource " + "com.hp.cdm.service.calibration.version.1.configuration" +"-----")
    print("----- Check ondemand desire --------")
    expected_status = 204
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.1","cdm/calibration/v1/configuration","GET")
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
        "gun" : "com.hp.cdm.service.calibration.version.1.resource.configuration",
        "path" : "/calibration/v1//configuration",
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
    check = resource_availability_check(cdm, "com.hp.cdm.service.calibration.version.1", "/cdm/calibration/v1", "configuration")
    print(check)
    if check != False:
        assert (r.status_code == expected_status)
    else:
        print("Resource not available")

    print( "-----------------------------------------" )
    
    pubsubClientInstanceId = "calibrations"
    pubsubClientInstanceId = "calibration"
    pubsubClientInstanceId = "calibrationCapabilities"
    print("----- PubSub not supported for this resource " + "com.hp.cdm.service.calibration.version.1.calibrationCapabilities" +"-----")
    print("----- Check ondemand desire --------")
    expected_status = 204
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.1","cdm/calibration/v1/calibrationCapabilities","GET")
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
        "gun" : "com.hp.cdm.service.calibration.version.1.resource.calibrationCapabilities",
        "path" : "/calibration/v1//calibrationCapabilities",
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
    #Check resource availability
    check = resource_availability_check(cdm, "com.hp.cdm.service.calibration.version.1", "/cdm/calibration/v1", "calibrationCapabilities")
    print(check)
    if check != False:
        assert (r.status_code == expected_status)
    else:
        print("Resource not available")

    print( "-----------------------------------------" )
    
    pubsubClientInstanceId = "calibrationCapability"
    print("----- PubSub not supported for this resource " + "com.hp.cdm.service.calibration.version.1.calibrationCapability" +"-----")
    print("----- Check ondemand desire --------")
    expected_status = 204
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.1","cdm/calibration/v1/calibrationCapabilities/{calibrationType}","GET")
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
        "gun" : "com.hp.cdm.service.calibration.version.1.resource.calibrationCapability",
        "path" : "/calibration/v1//calibrationCapabilities/{calibrationType}",
        "method" : "get",
        "ackToken" : "onDemandAck",
        }
        ]
    }
    resource["desires"][0]["onDemand"]["clientId"] = pubsubClientId
    resource["desires"][0]["onDemand"]["clientInstanceId"] = pubsubClientInstanceId
    resource["desires"][0]["ackToken"] = "onDemandAck_" + "calibrationCapability"
    print(resource)
    headers = {}
    timeout = 4.0
    r = cdm.patch_raw(ENDPOINT_PUBSUB_ONDEMAND, resource, headers=headers, scope_alias=cdm.ScopeAlias.HP_CLOUD_SERVICE, timeout=timeout)
    print(r.status_code)
    #Check resource availability
    check = resource_availability_check(cdm, "com.hp.cdm.service.calibration.version.1", "/cdm/calibration/v1", "calibrationCapabilities")
    print(check)
    if check != False:
        assert (r.status_code == expected_status)
    else:
        print("Resource not available")

    print( "-----------------------------------------" )
    
    pubsubClientInstanceId = "calibrationsAction"
    print("----- PubSub not supported for this resource " + "com.hp.cdm.service.calibration.version.1.calibrationsAction" +"-----")
    print("----- Check ondemand desire --------")
    expected_status = 204
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.1","cdm/calibration/v1/calibrationsAction","GET")
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
        "gun" : "com.hp.cdm.service.calibration.version.1.resource.calibrationsAction",
        "path" : "/calibration/v1//calibrationsAction",
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
    check = resource_availability_check(cdm, "com.hp.cdm.service.calibration.version.1", "/cdm/calibration/v1", "calibrationsAction")
    print(check)
    if check != False:
        assert (r.status_code == expected_status)
    else:
        print("Resource not available")

    print( "-----------------------------------------" )
    
    pubsubClientInstanceId = "alerts"
    print("----- PubSub not supported for this resource " + "com.hp.cdm.service.calibration.version.1.alerts" +"-----")
    print("----- Check ondemand desire --------")
    expected_status = 204
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.1","cdm/calibration/v1/alerts","GET")
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
        "gun" : "com.hp.cdm.service.calibration.version.1.resource.alerts",
        "path" : "/calibration/v1//alerts",
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
    #Check resource availability
    check = resource_availability_check(cdm, "com.hp.cdm.service.calibration.version.1", "/cdm/calibration/v1", "alerts")
    print(check)
    if check != False:
        assert (r.status_code == expected_status)
    else:
        print("Resource not available")

    print( "-----------------------------------------" )
    
    pubsubClientInstanceId = "alert"
    print("----- PubSub not supported for this resource " + "com.hp.cdm.service.calibration.version.1.alert" +"-----")
    print("----- Check ondemand desire --------")
    expected_status = 204
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.1","cdm/calibration/v1/alerts/{id}","GET")
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
        "gun" : "com.hp.cdm.service.calibration.version.1.resource.alert",
        "path" : "/calibration/v1//alerts/{id}",
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
    #Check resource availability
    check = resource_availability_check(cdm, "com.hp.cdm.service.calibration.version.1", "/cdm/calibration/v1", "alerts")
    print(check)
    if check != False:
        assert (r.status_code == expected_status)
    else:
        print("Resource not available")

    print( "-----------------------------------------" )
    
    pubsubClientInstanceId = "alertAction"
    print("----- PubSub not supported for this resource " + "com.hp.cdm.service.calibration.version.1.alertAction" +"-----")
    print("----- Check ondemand desire --------")
    expected_status = 204
    claimScope = cdm.ScopeAlias.PUBLIC
    claimScopeData = cdm.get(cdm.V1_CLAIM_SCOPE_DATA)
    claimScopes = cdmUtil.getClaimScopes(claimScopeData, "com.hp.cdm.service.calibration.version.1","cdm/calibration/v1/alerts/{id}/action","GET")
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
        "gun" : "com.hp.cdm.service.calibration.version.1.resource.alertAction",
        "path" : "/calibration/v1//alerts/{id}/action",
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
    check = resource_availability_check(cdm, "com.hp.cdm.service.calibration.version.1", "/cdm/calibration/v1", "alerts")
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
            assert "1.5.0" in service["version"]
            for link in service["links"]:
                print ("link[href]:" + link["href"])
                if link["href"] == service_path + "/" + resource  :
                    print(link["href"] + " - is supported and discoverable")
                    resource_supported = True
                    return resource_supported
                else:
                    print(resource + " resource not discoverable")
    # if the resource is not found in the services discovery, check if get is supported
    headers = {}
    timeout = 4.0
    if resource_supported == False:
        response = cdm.get_raw(service_path + "/" + resource, headers=headers, timeout=timeout)
        print(response.status_code)
        if response.status_code == 404:
            print(resource + " resource not supported")
    return resource_supported