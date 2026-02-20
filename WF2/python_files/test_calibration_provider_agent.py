from inspect import Parameter, signature
from pprint import pprint
import schemathesis
import pytest
from schemathesis.hooks import *
from tests.yeti.conftest import *
from tests.conftest import *
from tests.cdm.schema.schemathesis_common import SchemathesisCommon
import dunetuf.cdm
from hypothesis import strategies as st
from hypothesis import HealthCheck, seed
from hypothesis import HealthCheck
from schemathesis import Case
from schemathesis import checks
from typing import Callable, List
from hypothesis import HealthCheck, Verbosity
from hypothesis import settings as hypothesis_settings

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Test CDM calibration service with openapi schemathesis generated tests
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-179308
    +timeout:120
    +asset:CDM
    +delivery_team:PDLJobPQ
    +feature_team:PQsolns
    +test_framework:TUF
    +name:TestCalibrationServiceAPI::test_calibration_cdm_service
    +test:
        +title:TestCalibrationServiceAPI::test_calibration_cdm_service
        +guid:1b100775-e060-4ac9-918b-89fbf608b91f
        +dut:
            +type: Simulator
            +configuration: WebServices=CDM & CDMServiceVersion=CalibrationV1
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

class TestCalibrationServiceAPI:

    openapi_spec = "src/fw/ws/cdm/services/Calibration/pub/com.hp.cdm.service.calibration.version.1.openapi.json"
    serviceGun = "com.hp.cdm.service.calibration.version.1"

    def shortcuts():
        """
        Shortcuts is called by every hook, listed here so we can log things out and understand the system.
        """
        import inspect
        #print(inspect.currentframe().f_back.f_code.co_name)

    @classmethod
    def setup_class(cls):
        """setup any state specific to the execution of the given class (which usually contains tests)."""

        # Setup  class method called once before any test methods in the class are executed.
        # Use this method to perform actions that is common for entire test class
        # Example: Initialize database Connection which is common for entire test class

        print("[setup_class]")

    @pytest.fixture(scope="class", autouse=True)
    def one_time_setup(self, udw):
        return
    
    @pytest.fixture()
    def token(self, udw):
        pytest.udw = udw
        oauth2_token = udw.mainApp.OAuth2Standard.testCreateHpCloudScopeToken()
        return str(oauth2_token)

    #set initial state
    def idle_state(context, case):
        print("[idle_state]")

    call_before_cases = [idle_state]

    def pytest_generate_tests(self, metafunc):
        if ("to_call_before_case" in metafunc.fixturenames):
            metafunc.parametrize("to_call_before_case", TestCalibrationServiceAPI.call_before_cases)

    def get_fixtures_ignore_defaults(func :Callable, request, combined_with):
        sig = signature(func)
        filtered_join = {name : combined_with[name] for name in sig.parameters
                         if name in combined_with}
        kargs_fixture = {name: request.getfixturevalue(name) for name in sig.parameters 
                if name not in combined_with
                and sig.parameters[name].default is Parameter.empty}
        kargs_fixture.update(filtered_join)
        return kargs_fixture

    @pytest.fixture()
    def setup_callbacks(self, request, to_call_before_case):
        pytest.schema_hook_before_call = to_call_before_case
        
        def call_before_wrapper_hook(context, case):
            predefined_fixtures = {"context": context, "case": case}
            fixtures = TestCalibrationServiceAPI.get_fixtures_ignore_defaults(pytest.schema_hook_before_call, request, predefined_fixtures)
            pytest.schema_hook_before_call(**fixtures)
        schemathesis.hooks.GLOBAL_HOOK_DISPATCHER.unregister_all()
        schemathesis.hooks.GLOBAL_HOOK_DISPATCHER.register_hook_with_name(hook = call_before_wrapper_hook, name = "before_call")
        
    ##Custom search example
    #strategy = st.from_regex(r"\A4[0-9]{15}\Z")#.filter(luhn_validator)<- function filter
    #schemathesis.openapi.format("visa_cards", strategy)

    #filtering example
    #operation = schema["/v1/avatarRegistration/registration"]["PUT"]
    #strategy = operation.as_strategy()
    #print(strategy.example())

    @classmethod
    def teardown_class(cls):
        """teardown any state that was previously setup with a call to setup_class. """

        # Teardown class method called once after all test methods in the class have run.
        # Use this method to perform clean-up actions that is common for entire test class
        # Example: Close database connection which is common for entire test class

        print("[teardown_class]")

    spec_path = os.path.join(os.getenv('REPO_ROOT'), openapi_spec)

    print (spec_path)

    #APIs implement rate limiting to prevent misuse of their resources.
    #Schema loaders accept the rate_limit argument that can be used to set
    #the maximum number of requests per second, minute, hour, or day during
    #testing to avoid hitting these limits.

    # 10 requests per second - `10/s`
    # 100 requests per minute - `100/m`
    # 1000 requests per hour - `1000/h`
    # 10000 requests per day - `10000/d`
    #
    #RATE_LIMIT = "50/s"


    schema = schemathesis.from_path(spec_path, rate_limit=SchemathesisCommon.schema_rate_limit)


    @pytest.fixture(scope="class", autouse=True)
    def is_version_available(self, cdm):
        pytest.is_version_available = False
        servicesDiscovery = cdm.get(cdm.SERVICES_DISCOVERY)
        for service in servicesDiscovery["services"]:
            if service["serviceGun"] == self.serviceGun:
                print("Service found: " + self.serviceGun)
                pytest.is_version_available = True
        print("Service not found: " + self.serviceGun)


    @hypothesis_settings(suppress_health_check=[HealthCheck.function_scoped_fixture], 
                deadline=None, #deadline is how long it takes to GENERATE the test suites
                derandomize=True,
                max_examples=100,
                verbosity=Verbosity.quiet,
                database=None)
    @seed(1)
    @schema.parametrize()
    def test_calibration_cdm_service(self,case, request, token, setup_callbacks):
        base_urn = "/cdm/calibration/v1"
        SchemathesisCommon.count = SchemathesisCommon.count + 1
        print("\n-- count = " + str(SchemathesisCommon.count) + "--")
        #print("\n--Request--\n")
        # Use the follwing line to print the complete request
        #pprint(vars(case))
        pprint(case.operation.verbose_name)
        pprint(case.headers)
        excluded_checks = []
        # If the test needs to ignore 5XX errors returned by the CDM Provider, then add option - checks=[check for check in checks.ALL_CHECKS if check!=checks.not_a_server_error]  - to call_and_validate
        r = case.call_and_validate(headers={"Authorization": "Bearer " + token}, verify=False, base_url="https://" + request.config.option.target + base_urn,  checks=[check for check in checks.ALL_CHECKS if check not in excluded_checks])
        #print("\n--Response--\n")
        # Use the follwing line to print the complete response
        #pprint(vars (r))
        pprint(r.status_code)
        #pprint(r.headers)
        # Use the follwing line to print the response json
        #pprint(r.json())
        #print("\n")


    @schema.hook("before_generate_path_parameters")
    def before_generate_path_parameters(context, strategy):
        TestCalibrationServiceAPI.shortcuts()
        return strategy
    @schema.hook("before_generate_headers")
    def before_generate_headers(context, strategy):
        TestCalibrationServiceAPI.shortcuts()
        return strategy
    @schema.hook("before_generate_cookies")
    def before_generate_cookies(context, strategy):
        TestCalibrationServiceAPI.shortcuts()
        return strategy
    @schema.hook("before_generate_query")
    def before_generate_query(context, strategy):
        TestCalibrationServiceAPI.shortcuts()
        return strategy
    @schema.hook("before_generate_body")
    def before_generate_body(context, strategy):
        TestCalibrationServiceAPI.shortcuts()
        return strategy

    @schema.hook("before_add_examples")
    def before_add_examples(
        context: schemathesis.hooks.HookContext,
        examples: List[Case],
    ) -> None:
        pass

