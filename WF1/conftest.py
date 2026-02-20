"""
Common dunetuf tests conftest.py file
"""

import os
import re
import sys
import json
import pytest
import logging
import requests
import subprocess

from contextlib import contextmanager

# TODO: merge functionalities of UDW & add unit tests
from dunetuf.cdm import CDM
from dunetuf.configuration import Configuration
from dunetuf.control.device_status import DuneDeviceStatus
from dunetuf.copy.copy import Copy
from dunetuf.counters import Counters
from dunetuf.device.reset import DeviceResetManager
from dunetuf.dial import DialController
from dunetuf.emulation.print import PrintEmulation
from dunetuf.emulation.scan import ScanEmulation
from dunetuf.engine.maia.AlertsMaia import AlertsMaia
from dunetuf.engine.maia.Power import Power
from dunetuf.engine.maia.SensorsMaia import SensorsMaia
from dunetuf.engine.maia.TclMaiaClient import TclMaiaClient
from dunetuf.engine.sirius.TclSiriusClient import TclSiriusClient
from dunetuf.engine.sirius.SiriusEngine import SiriusEngine
from dunetuf.event.EventFactory import EventFactory
from dunetuf.ews import get_ews_instance
from dunetuf.image.image import IMAGE
from dunetuf.job.job_configuration.job_configuration import JobConfiguration
from dunetuf.job.job_queue.job_queue import JobQueue
from dunetuf.job.job_history.job_history import JobHistory
from dunetuf.job.job import Job
from dunetuf.job.sendjob import DunePrintJob
from dunetuf.keypad import KeypadController
from dunetuf.localization.LocalizationHelper import LocalizationHelper
from dunetuf.metadata import set_metadata, set_platform, set_buildinfo, set_ip, set_qmltest_port, set_screen_capture, set_emulation_ip
from dunetuf.metadata import (
    set_metadata, set_platform, set_buildinfo,
    get_product_metadata, get_metadata
)
from dunetuf.network.net import Network, ConnectTimeoutException
from dunetuf.onboard.onboard import Onboard
from dunetuf.plugins.logcollector import collect_logs
from dunetuf.print.capabilities import Capabilities
from dunetuf.print.file import PrintFileGenerator
from dunetuf.print.media import MediaHandler
from dunetuf.print.output import OutputSaver, OutputVerifier
from dunetuf.print.print import PrintJob
from dunetuf.print.tray import TrayHandler
from dunetuf.print.bin import BinHandler
from dunetuf.qmltest.QmlTestServer import QmlTestServer
from dunetuf.scp import SCP
from dunetuf.reports import ReportContentValidation
from dunetuf.reports.NetworkConfigurationReportValidation import NetworkConfigurationReportValidation
from dunetuf.reports.ConnectivityStatusReportValidation import ConnectivityStatusReportValidation
from dunetuf.reports.NetworkSecurityReportValidation import NetworkSecurityReportValidation
from dunetuf.reports.ConfigurationReportValidation import ConfigurationReportValidation
from dunetuf.reports.WebAccessTestReportValidation import WebAccessTestReportValidation
from dunetuf.reports.WifiNetworkTestResultReportValidation import WifiNetworkTestResultReportValidation
from dunetuf.reports.WifiDirectReportValidation import WifiDirectReportValidation
from dunetuf.reports.WifiQuickStartGuideReportValidation import WifiQuickStartGuideReportValidation
from dunetuf.reports.FaxReportValidation import FaxReportValidation
from dunetuf.send.disk.disk import Disk
from dunetuf.send.folder.folder import Folder
from dunetuf.send.usb.usb import Usb
from dunetuf.servers.syslogngServer import SyslogngSever
from dunetuf.snmp import SNMP
from dunetuf.ssh import SSH
from dunetuf.cdm import CDM
from dunetuf.udw import UDWError, UDWConnectionTimeout
from dunetuf.udw import TclSocketClient
from dunetuf.ui.spice import Spice
from dunetuf.usb.device import UsbDevice
from dunetuf.utility.args import PytestArgs
from dunetuf.utility.pytestinspect import PytestInspect
from dunetuf.servers.cicadaserver import CicadaServer
from dunetuf.servers.pinpairingserver import IotPinPairing
from dunetuf.calibrations.Calibrations import Calibrations
from dunetuf.engine.maia.calibrations.MaiaCalibration import MaiaCalibration
from dunetuf.oobe.OOBEFactory import OOBEFactory
from dunetuf.web.Web import Web
from dunetuf.security.UiPermissionsTestInitialize import UiPermissionsTestInitialize
from dunetuf.security.UserGroupPermissionsFramework.NetworkUIUserGroupPermissions import NetworkUIUserGroupPermissions
from dunetuf.engine.maia.MediaMaia import MediaMaia
from dunetuf.engine.maia.MaiaEngine import MaiaEngine
from dunetuf.print.mapper import PrintMapper
from dunetuf.econfig import EConfiguration
from dunetuf.ioref.Ioref import Ioref
from dunetuf.yeti.yeti import Yeti
from dunetuf.plugins.print import DeviceManager
from dunetuf.network.IPConfig.Dhcpv4Keywords import Dhcpv4Keywords
from dunetuf.network.IPConfig.DhcpPrinterValidation import DhcpPrinterValidation
from dunetuf.servers.pubsubserver import PubSubServer
from dunetuf.engine.maia.HeaterMaia import HeaterMaia
from dunetuf.engine.maia.phMaia import phMaia
from dunetuf.engine.maia.MediaInfoMaia import MediaInfoMaia
from dunetuf.engine.engine import Engine
from tests.security.py_fixtures.security_py_fixtures import *
from dunetuf.control.targetdevice import TargetPlatform, TargetConnectivity, device_instance
from dunetuf.udw.udw import Underware

def pytest_addoption(parser):
    parser.addoption("--target", required=True, help="Target IP address")
    parser.addoption(
        "--power-on-timeout", default=60, type=float, help="Device power ON timeout (s)"
    )
    parser.addoption("--qmltest-port", default=8080, type=int, help="QMLTest port")
    parser.addoption("--interface", default="eth", help="Target IP address printer interface")
    parser.addoption(
        "--debug-level", default="a", type=str, help="Debug level (e.g. abcd)"
    )
    parser.addoption(
        "--metadata-file", default="", type=str,
        help="Filename of device metadata"
    )
    parser.addoption(
        "--family", default="Dune", type=str,
        help="Target device type (Dune, Ares)"
    )
    parser.addoption(
        "--platform", default="Sim", type=str,
        help="Platform of device (Sim, Eng, Emu)"
    )
    parser.addoption(
        "--sku", default="", help="Product sku name"
    )
    parser.addoption(
        "--build-info", default='{}', type=str,
        help="Build info for the execution"
    )
    parser.addoption(
        "--screencapture", default=False, action="store_true",
        help="Save screencaptures to /src/test/output/tuf_screencaptures/"
    )

    parser.addoption(
        "--fixture-cdm-timeout", default=5.0, type=float,
        help="Timeout value for CDM fixture"
    )

    parser.addoption(
        "--avoid-precondition-mechless",
        action="store_true",
        help="Avoid precondition mechless"
    )

    parser.addoption(
        "--rps-info", default=None, type=str,
        help="Rps Info for the product as a json string"
    )

    parser.addoption(
        "--finisher-name", default=None, type=str,
        help="Finisher name supported for the product sku (if any)"
    )

    parser.addoption(
        "--connectivity", default="proxyusb", type=str,
        help="Connectivity type for Ares products (proxyusb, ethernet, wireless), communicates with the printer based on the connectivity type"
    )

def pytest_configure(config):
    
    if config.option.family.lower() == "ares":
        os.environ['DEVICE_FAMILY'] = "ares" 
        device_instance().target_platform = TargetPlatform.ARES
        logging.info('TargetPlatform set to Ares')
    if config.option.connectivity:
        os.environ['DEVICE_CONNECTIVITY'] = config.option.connectivity.lower()
        device_instance().target_connectivity = TargetConnectivity[config.option.connectivity.upper()]
        logging.info('TargetConnectivity set to %s', config.option.connectivity)

    try:
        # Option only available if logcollector module is loaded
        cap = config.getoption("--capture-logs-to")
        if cap:
            os.environ["CAPTURE_LOGS_TO"] = cap
    except ValueError:
        pass

    if hasattr(config.option, "timeout"):
        timeout_value = getattr(config.option, 'timeout', None)
        if timeout_value is not None:
            config.option.timeout = timeout_value
        else:
            if hasattr(config.option, 'file_or_dir') and config.option.file_or_dir:
                test_path = config.option.file_or_dir   
                if isinstance(test_path, list) and test_path:
                    test_name = test_path[0].split("::", 1)[-1]
                    config.option.timeout = get_timeout_value_from_test_metadata(test_name)
            else:
                config.option.timeout = 120

def get_timeout_value_from_test_metadata(test_name):
    """
    Fetch the timeout value from the test metadata for a specific test.
    This function attempts to load the TestCatalog from the gui.test_catalog module
    and retrieve the timeout value for the specified test. If the test catalog
    cannot be loaded or the test is not found, it returns a default timeout value.
    Args:
        test_name (str): The name of the test to retrieve timeout metadata for.
    Returns:
        int: The timeout value in seconds. Returns 120 seconds (default) if:
            - Test is not found in the catalog
            - TestCatalog cannot be imported (common in local dev environments)
            - Timeout value is invalid or missing
            - Any unexpected error occurs during lookup
    Note:
        ImportError exceptions are common and expected in environments where:
        - Running tests locally without full dune installation
        - CI/CD environments that don't have gui.test_catalog available
        - Development setups with incomplete module paths
        This is normal behavior and the function gracefully falls back to defaults.
    """
    default_timeout = 120
    
    try:
        # Add dune paths if they exist
        repo_root = os.environ.get(
            'REPO_ROOT'
        )
        if not repo_root:
            raise EnvironmentError("REPO_ROOT environment variable is not set.")
        
        dune_path = os.path.join(repo_root, 'src', 'tools', 'testing')
        if os.path.exists(dune_path) and dune_path not in sys.path:
            sys.path.append(dune_path)
        
        from gui.test_catalog import TestCatalog
        
        test_catalog = TestCatalog(os.path.dirname(os.path.realpath(__file__)))
        
        # Direct lookup instead of iteration
        for test in test_catalog.values():
            if test.name == test_name and test.timeout:
                timeout_value = int(test.timeout)
                return timeout_value if timeout_value > 0 else default_timeout   
        return default_timeout
        
    except ImportError:
        logging.error("Failed to import TestCatalog. Ensure the path is correct.")
        return default_timeout
    except (ValueError, AttributeError) as e:
        logging.error("Error parsing timeout value from test metadata: %s", e)
        return default_timeout
    except Exception as e:
        logging.error("Unexpected error fetching timeout value: %s", e)
        return default_timeout

def _add_test_string_checkpoint(udw_instance, level, message):
    """
        private function to encapsulate the logic to decide if we have to add
        test string chkpoint to an app
    """
    current_component = None
    try:
        if hasattr(udw_instance, "mainApp") and \
           hasattr(udw_instance.mainApp, "Debug"):
            current_component = "mainApp"
            try:
                udw_instance.mainApp.Debug.TestStringCheckpoint(level, message)
            except (UDWConnectionTimeout, ConnectTimeoutException):
                logging.warning(
                    "Encountered timeout while attempting to log SYSTEM_TEST_END trace " +
                    "statement: Failed component: %s.", current_component
                )
        if hasattr(udw_instance, "mainUiApp") and \
           hasattr(udw_instance.mainUiApp, "Debug"):
            current_component = "mainUiApp"
            try:
                udw_instance.mainUiApp.Debug.TestStringCheckpoint(level, message)
            except (UDWConnectionTimeout, ConnectTimeoutException):
                logging.warning(
                    "Encountered timeout while attempting to log SYSTEM_TEST_END trace " +
                    "statement: Failed component: %s.", current_component
                )
        if hasattr(udw_instance, "connectivityApp") and \
           hasattr(udw_instance.connectivityApp, "Debug"):
            current_component = "connectivityApp"
            try:
                udw_instance.connectivityApp.Debug.TestStringCheckpoint(level, message)
            except (UDWConnectionTimeout, ConnectTimeoutException):
                logging.warning(
                    "Encountered timeout while attempting to log SYSTEM_TEST_END trace " +
                    "statement: Failed component: %s.", current_component
                )
        if hasattr(udw_instance, "firmwareUpdateApp") and \
           hasattr(udw_instance.firmwareUpdateApp, "Debug"):
            current_component = "firmwareUpdateApp"
            try:
                udw_instance.firmwareUpdateApp.Debug.TestStringCheckpoint(level, message)
            except (UDWConnectionTimeout, ConnectTimeoutException):
                logging.warning(
                    "Encountered timeout while attempting to log SYSTEM_TEST_END trace " +
                    "statement: Failed component: %s.", current_component
                )
    except UDWError:
        logging.exception(
            "Encountered exception while attempting to log SYSTEM_TEST_END trace " +
            "statement: Failed component: %s.", current_component
        )

@pytest.fixture(scope="session", autouse=True)
def readiness(request):
    """
    Autouse fixture. Wait for device being ready as a precondition for the test.
    """
    try:
        # This is for the RPE (E2 API simulator).
        if "rpe" in request.config.option.target:
            return

        if request.config.option.family == TargetPlatform.DUNE:
            # Make sure system is fully powered on before doing anything else
            device_status = DuneDeviceStatus(request.config.option.target)
            response = device_status.pre_test_ready(request.config.option.power_on_timeout)
            if not all(list(response.values())):
                raise TimeoutError("Device power ON timed out")

            device_status.set_max_sleep()
            device_status.set_max_inactivity_timeout()

        try:
            udw_instance = Underware(request.config.option.target)

            if hasattr(udw_instance, "mainApp") and \
                hasattr(udw_instance.mainApp, "AdminStandard"):
                        if hasattr(udw_instance.mainApp.AdminStandard, "getAdminState"):
                            admin_state = udw_instance.mainApp.AdminStandard.getAdminState()
                            logging.info('**readiness (mainApp)** [before PIN set] Admin state: %s', admin_state)
                        else:
                            logging.warning('**readiness (mainApp)** getAdminState udw unavailable')

                        setPwdRetVal = udw_instance.mainApp.AdminStandard.setDefaultDevicePassword("12345678")
                        logging.info('**readiness (mainApp)** Device default PIN set: %s', setPwdRetVal)

                        if hasattr(udw_instance.mainApp.AdminStandard, "setIgnoreManufacturingPin"):
                            # clear the "ignore manufacturing pin" flag if set by previous test
                            setIgnoreMfgPinRetVal = udw_instance.mainApp.AdminStandard.setIgnoreManufacturingPin(False)
                            logging.info('**readiness (mainApp)** setIgnoreManufacturingPin to False returned: %s', setIgnoreMfgPinRetVal)
                        else:
                            logging.warning('**readiness (mainApp)** setIgnoreManufacturingPin udw unavailable')

                        if hasattr(udw_instance.mainApp.AdminStandard, "getAdminState"):
                            admin_state = udw_instance.mainApp.AdminStandard.getAdminState()
                            logging.info('**readiness (mainApp)** [before PIN set] Admin state: %s', admin_state)
                        else:
                            logging.warning('**readiness (mainApp)** getAdminState udw unavailable')
        except Exception as ex:
            # In some cases the mainApp is not initialized, so we need to catch the exception.
            # e.g. testcase test_recovery_basic_idle
            logging.warning("Failed to execute readiness udw commands to set default Admin PIN: %s", ex)
        try:
            if (not request.config.option.avoid_precondition_mechless and
              request.config.option.platform == "Eng"):
                logging.info("**readiness** Checking mechless mode and setting it")
                # check if TUF_DEVICE_MEATDATA is there else fetch it from get_product_metadata
                if not get_metadata():
                    logging.info("**readiness** Metadata not found in environment")
                    cdm = CDM(request.config.option.target,
                              udw=Underware(request.config.option.target))
                    configuration = Configuration(cdm)
                    product_metadata = get_product_metadata(cdm, configuration)
                engine = Engine(udw=udw_instance)
                rps_info = None
                if request.config.option.rps_info:
                    rps_info = json.loads(request.config.option.rps_info)
                    if not os.path.exists(rps_info.get('cred_file')):
                        logging.error("RPS cred file not found")
                        rps_info = None
                # lets check if device is in mechless mode and set it if not
                if engine.get_mechless_mode():
                    logging.info("**readiness** Mechless mode already set")
                else:
                    logging.info("**readiness** Setting mechless mode")
                    if engine.set_mechless_mode(True,rps_info):
                       logging.info("**readiness** Mechless mode set")
            else:
                logging.info("**readiness** Avoiding mechless mode")
        except Exception as ex:
            logging.error("Failed to check or set mechless mode: %s", ex)

    except Exception as exc:
        # Try to collect printer logs in case of early failure
        if request.config.option.capture_logs_to:
            collect_logs(request.config.option.target, request.config.option.capture_logs_to)

        raise exc

    # Remove all history logs to avoid collecting previous test's history logs
    try:
        ip = request.config.option.target
        _ssh = SSH(ip)
        history_logs_directory = '/mnt/machinedata/log/history'
        rm_result = _ssh.run("rm -rf {}".format(history_logs_directory))
    except Exception as ex:
        print('Error removing /mnt/machinedata/log/history from target. Error {}'.format(ex))

   # Make sure control panel is in home screen before test start.
    try:
        spice = Spice(request.config.option.target, request.config.option.qmltest_port, request.config.option.screencapture)
        spice.goto_homescreen()
    except:
        logging.warning("Failed to go to home screen.")


class TUFStore(object):

    def __init__(self, request):
        self.request = request

    @contextmanager
    def open(self, filename, access):
        base_dir = self.request.config.option.capture_logs_to

        assert base_dir

        module_namespace = PytestInspect.test_module_file_namespace(self.request)
        test_dir = os.sep.join(module_namespace.split('.'))

        dir_name = base_dir + os.sep + test_dir
        if not os.path.isdir(dir_name):
            os.makedirs(dir_name, exist_ok=True)

        # Don't allow a test to write outside its directory
        filename = filename.split(os.sep)[-1]

        test_name = dir_name + os.sep + filename

        with open(test_name, access) as test_file:
            yield test_file


@pytest.fixture(autouse=True)
def store(request):
    yield TUFStore(request)

@pytest.fixture(scope="session", autouse=True)
def set_ip_address(request):
    set_ip(request.config.option.target)

@pytest.fixture(scope="session", autouse=True)
def set_emulation_ip_address(request):
    if 'engineSimulatorIP' in sys.argv:
        engine_simulator_ip = sys.argv[sys.argv.index('engineSimulatorIP') + 1]
        set_emulation_ip(engine_simulator_ip)

@pytest.fixture(scope="session", autouse=True)
def set_qmltest_port_number(request):
    set_qmltest_port(request.config.option.qmltest_port)

@pytest.fixture(scope="session", autouse=True)
def set_screencapture(request):
    set_screen_capture(request.config.option.screencapture)

@pytest.fixture(scope="session", autouse=True)
def buildinfo(request):
    set_buildinfo(json.loads(request.config.option.build_info))
    yield None


@pytest.fixture(scope="session", autouse=True)
def devicemetadata(request):
    sku_name = request.config.option.sku
    ip = request.config.option.target
    metadata_dict = {}
    if sku_name:
        metadata_path = os.path.join(os.sep, "core", "product", "metadata")
        destination_file = os.path.join(metadata_path,
                            '{}.json'.format(re.sub('[^A-Za-z0-9\\-]+', '_', sku_name)))
        _ssh = SSH(ip)
        output = str()
        try:
            output = _ssh.run("cat {}".format(destination_file))
        except IOError as ex:
            print('Error in fetching information from target. Error {}'.format(ex))
        if output:
            raw_metadata = json.loads(output)
            metadata_dict ={"Data" : raw_metadata}
    else:
        try:
            metadata_dict = json.load(open(request.config.option.metadata_file))
        except FileNotFoundError:
            metadata_dict = {}
    set_metadata(metadata_dict)
    yield None


@pytest.fixture(scope="session", autouse=True)
def deviceplatform(request):
    set_platform(request.config.option.platform)
    yield None


@pytest.fixture
def qml(request):
    """QmlTestServer fixture."""
    yield QmlTestServer(
        request.config.option.target, request.config.option.qmltest_port, request.config.option.screencapture
    )


@pytest.fixture
def dial(request):
    """Dial fixture."""
    yield DialController(request.config.option.target)


@pytest.fixture
def spice(request):
    """Spice fixture."""
    spice = Spice(request.config.option.target, request.config.option.qmltest_port, request.config.option.screencapture)
    spice.wait_ready()
    yield spice


@pytest.fixture
def keypad(udw2):
    """Keypad fixture."""
    yield KeypadController(udw2)


@pytest.fixture(scope="session")
def args(request):
    """Dune pytest command-line argument access"""
    yield PytestArgs(request.config.option)


@pytest.fixture(scope="session", autouse=True)
def udw(request):
    """Dune Underware Fixture."""

    udw_instance = Underware(request.config.option.target)
    test_name = "{}::{}".format(request.node.name,
                                os.environ.get('PYTEST_CURRENT_TEST')
                                # Current test is last in ':' separated list
                                .split(':')[-1]
                                .split(' ')[0]     # remove non list arguments
                                # strip any pytest-added list arguments
                                .split('[', maxsplit=1)[0]
                                .replace(' ', '_'))  # replace any whitespaces with underscore

    _add_test_string_checkpoint(udw_instance, "a",
                                              "SYSTEM_TEST_BEGIN___{}".format(test_name))

    yield udw_instance

    _add_test_string_checkpoint(udw_instance, "a",
                                              "SYSTEM_TEST_END___{}".format(test_name))


# This fixture uses "session" scope because it is indirectly used by the readiness fixture which also has session scope
@pytest.fixture(scope="session", autouse=True)
def cdm(request):
    """Dune CDM Fixture."""
    CDM.DEFAULT_TIMEOUT = request.config.option.fixture_cdm_timeout
    yield CDM(request.config.option.target)


@pytest.fixture
def snmp(request):
    """Dune SNMP Fixture."""
    yield SNMP(request.config.option.target)


@pytest.fixture
def ews(request):
    """Dune EWS Fixture."""
    yield get_ews_instance(request.config.option.target)


@pytest.fixture
def ssh(request):
    """Dune SSH Fixture."""
    yield SSH(request.config.option.target)


@pytest.fixture(scope="session", autouse=True)
def net(request):
    """Dune Network Fixture."""
    yield Network(request.config.option.target)


@pytest.fixture
def scp(request):
    """Dune SCP Fixture."""
    yield SCP(request.config.option.target)


@pytest.fixture
def reports(scp):
    yield ReportContentValidation(scp)

@pytest.fixture
def faxReportValidation():
    yield FaxReportValidation()

@pytest.fixture
def networkConfigurationReportValidation():
    yield NetworkConfigurationReportValidation()

@pytest.fixture
def connectivityStatusReportValidation():
    yield ConnectivityStatusReportValidation()

@pytest.fixture
def networkSecurityReportValidation():
    yield NetworkSecurityReportValidation()

@pytest.fixture
def configurationReportValidation():
    yield ConfigurationReportValidation()

@pytest.fixture
def webAccessTestReportValidation():
    yield WebAccessTestReportValidation()

@pytest.fixture
def wifiNetworkTestResultReportValidation():
    yield WifiNetworkTestResultReportValidation()

@pytest.fixture
def wifiDirectReportValidation():
    yield WifiDirectReportValidation()

@pytest.fixture
def wifiQuickStartGuideReportValidation():
    yield WifiQuickStartGuideReportValidation()

@pytest.fixture
def dhcpv4_client():
    """Dune DHCPv4 client Fixture."""
    yield Dhcpv4Keywords()


@pytest.fixture
def dhcp_printer_validation(request):
    '''Dune DHCPv4 Printer validation'''
    yield DhcpPrinterValidation(request.config.option.target)


@pytest.fixture
def tcl(request):
    """Dune TclSocketClient Fixture."""
    yield TclSocketClient(request.config.option.target, 9104)


@pytest.fixture
def tclMaia(request):
    """Dune TclMaia Fixture."""
    yield TclMaiaClient(request.config.option.target, 19104)


@pytest.fixture
def alertsMaia(tclMaia):
    """Dune Maia Alerts Fixture."""
    yield AlertsMaia(tclMaia)


@pytest.fixture
def power(tclMaia, ssh):
    """Dune Power for Maia Fixture."""
    yield Power(tclMaia, ssh)


@pytest.fixture
def sensorsMaia(tclMaia):
    """Dune Maia Sensors Fixture."""
    yield SensorsMaia(tclMaia)


@pytest.fixture
def tclSirius(udw):
    """Dune TclSirius Fixture."""
    #--------- Set Up -----------
    sirius_tlc_instance = TclSiriusClient(udw)
    sirius_tlc_instance.connect()

    #--------- Execute Test ----------
    yield sirius_tlc_instance

    #--------- Test Tear Down --------
    sirius_tlc_instance.disconnect()


@pytest.fixture
def siriusEngine(tclSirius, cdm):
    yield SiriusEngine(tclSirius, cdm)


@pytest.fixture
def configuration(cdm):
    yield Configuration(cdm)


@pytest.fixture
def job(cdm, udw):
    """Dune  Job Fixture."""
    yield Job(cdm, udw)


@pytest.fixture
def disk(cdm, udw):
    """Dune  Disk Fixture."""
    yield Disk(cdm, udw)


@pytest.fixture
def copy(cdm, udw):
    """Dune  Copy Fixture."""
    yield Copy(cdm, udw)


@pytest.fixture
def usb(cdm, udw, net):
    """Dune  Usb Fixture."""
    yield Usb(cdm, udw, net)


@pytest.fixture
def usbdevice(cdm, udw):
    """Dune UsbDevice Fixture."""
    yield UsbDevice(cdm, udw)

@pytest.fixture
def folder(cdm, udw):
    """Dune  folder Fixture."""
    yield Folder(cdm, udw)

@pytest.fixture
def device(net):
    yield DuneDeviceStatus(net.ip_address, "")


@pytest.fixture
def print_emulation(cdm, udw, tcl):
    engineSimulatorIP = sys.argv[sys.argv.index('engineSimulatorIP') + 1]
    # Check for missing information
    if engineSimulatorIP == 'None':
        logging.debug('Instantiating PrintEmulation: no engineSimulatorIP specified, was -eip not set to emulator/simulator emulation IP?')
    engineSimulatorIP = None if engineSimulatorIP == 'None' else engineSimulatorIP

    logging.info('Instantiating PrintEmulation with %s', engineSimulatorIP)
    yield PrintEmulation(cdm, udw, tcl, engineSimulatorIP)

@pytest.fixture
def scan_emulation(cdm, udw, tcl):
    scanSimulatorIP = sys.argv[sys.argv.index('scanSimulatorIP') + 1]
    scanSimulatorIP = None if scanSimulatorIP == 'None' else scanSimulatorIP

    logging.info('Instantiating ScanEmulation with %s', scanSimulatorIP)
    yield ScanEmulation(cdm, udw, tcl, scanSimulatorIP)


@pytest.fixture
def reset_manager(cdm, udw, device):
    yield DeviceResetManager(cdm, udw, device)


@pytest.fixture
def duneprintjob(net):
    yield DunePrintJob(net.ip_address, 9100)


@pytest.fixture
def capabilities(net):
    """Device capabilities through IPP and other means."""
    yield Capabilities(net)


@pytest.fixture
def printjob(job, duneprintjob, testname, capabilities):
    yield PrintJob(job, duneprintjob, testname, capabilities)


@pytest.fixture
def outputsaver(udw, ssh, scp, request, testname, configuration):
    yield OutputSaver(udw, ssh, scp, request, testname, configuration)


@pytest.fixture
def outputverifier(outputsaver):
    yield OutputVerifier(outputsaver)


@pytest.fixture
def econfig(configuration, print_emulation):
    yield EConfiguration(configuration, print_emulation)

@pytest.fixture
def tray(udw, cdm):
    yield TrayHandler(udw, cdm)

@pytest.fixture
def bin(udw, cdm):
    yield BinHandler(udw, cdm)

@pytest.fixture
def media(udw, cdm):
    yield MediaHandler(udw, cdm)


@pytest.fixture
def counters(cdm, udw):
    yield Counters(cdm, udw)


@pytest.fixture
def printfile(request, testname):
    yield PrintFileGenerator(request, testname)


@pytest.fixture
def calibrations(tcl, udw):
    yield Calibrations(tcl, udw)

@pytest.fixture
def maiaCalibration(tclMaia):
    yield MaiaCalibration(tclMaia)

@pytest.fixture
def mediaMaia(tclMaia):
    yield MediaMaia(tclMaia)
@pytest.fixture
def maiaEngine(tcl,tclMaia,scp, net, cdm , device, ssh):
    yield MaiaEngine(tcl,tclMaia,scp, net, cdm, device, ssh)

@pytest.fixture(scope="session", autouse=True)
def set_debug_levels(request):
    """Automatic fixture to setup debug level."""

    # This is for the RPE (E2 API simulator).
    # TODO: should configure logging for Ares as well.
    if ("rpe" in request.config.option.target) or (request.config.option.family.lower() == "ares"):
        return

    udw = Underware(request.config.option.target)
    debug_level = request.config.option.debug_level.lower()

    levels = {
        "a": "a" in debug_level,
        "b": "b" in debug_level,
        "c": "c" in debug_level,
        "d": "d" in debug_level,
    }

    for level, enabled in levels.items():
        for app_name, app in udw.apps.items():
            if hasattr(udw.connectivityApp, "Debug"):
                udw.connectivityApp.Debug.TestStringCheckpoint(
                    "a", "set_debug_levels:{}:{}={}".format(app_name, level, enabled)
                )

            if hasattr(app, "Debug"):
                app.Debug.setFilterLevelAcrossAllDomains(level, enabled)


@pytest.fixture(scope="session", autouse=True)
def check_security_disable_wifi(request):
    """ required for wifi testing via usb to ethernet """

    if(request.config.option.interface  == "usb"):
        cmd = os.system("rm /code/output/usb.sh")
        f = open("/code/output/usb.sh", "x")
        data = "telnet " + str(request.config.option.target) + " 9104 <<E0F "
        f.write(data)
        f.write("\n")
        f.write("WebServerSecurity PUB_EnableCSRFCheck false")
        f.write("\n")
        f.write("EOF")
        f.close()
        os.system("chmod +x /code/output/usb.sh")
        subprocess.call(['sh', '/code/output/usb.sh'])


@pytest.fixture
def testname():
    """Return the current test name, remove setup/teardown suffixes."""
    current_test_parts = os.environ.get('PYTEST_CURRENT_TEST', 'file::class::method').split('::')
    current_test = "::".join(current_test_parts[1:])
    current_test = current_test.replace('(', '#').replace('[', '#')
    current_test = current_test.split('#')[0].strip()
    return current_test


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Overriding hook provided by pytest-html to include ews snapshot and logs in tests that uses ews fixture.
    This is ignored for tests that doesn't use ews fixture.
    """
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])
    try:
        feature_request = item.funcargs['request']
        # IMPORTANT: The call on the next line, getfixturevalue('ews'), will cause the EWS fixture to get
        # created and initialized, if it is not already.  This means that even if a test does not
        # use the fixture, it will get created and any code inside the fixture's __init__() method
        # will get executed.  In July 2025, we temporary tried to make this more efficient by not
        # calling getfixturevalue('ews'), but this caused a few tests to fail.  It could have been
        # due to timing or some other side effects.  The call to getfixturevalue('ews') has been in
        # place since 2021 and hasn't caused any known issues... so we'll leave it alone for now.
        browser = feature_request.getfixturevalue('ews')
        if report.when == "call" and browser.driver is not None:
            xfail = hasattr(report, "wasxfail")
            if (report.skipped and xfail) or (report.failed and not xfail):
                # Adds the snapshot to extras so that the report shows up the snapshot of the EWS page.
                extra.append(pytest_html.extras.image(browser.driver.get_screenshot_as_base64()))
                report.extra = extra
                logpath = feature_request.config.option.capture_logs_to
                logpath = logpath if logpath else os.path.join('/code/output/')
                # We are not allowed to call testname() defined above
                current_test_parts = os.environ.get('PYTEST_CURRENT_TEST', 'file::class::method').split('::')
                current_test = "::".join(current_test_parts[1:])
                current_test = current_test.replace('(', '#').replace('[', '#')
                current_test = current_test.split('#')[0].strip()
                browser.helper.get_browser_console_log(logpath, current_test)
                browser.helper.get_browser_performance_log(logpath, current_test)
            # close_browser() will only do something if the driver is still open
            browser.close_browser()
    except:
        # Do Nothing
        pass


@pytest.fixture
def image():
    yield IMAGE()


@pytest.fixture
def setup_teardown_print_device(job, outputsaver, device, media, tclMaia):
    """Default setup/teardown fixture for Print/Copy tests."""
    logging.info('-- SETUP (Print/Copy Tests) --')
    # ---- Setup emulator For Maia ----
    # This tcl is product dependant and should be implemented by each engine
    # Should initialize all the needed subsystems to allow engine in ready state
    # for instance: load media, accept pens, set as ready all the supplies, skip OOBE
    try:
        tclMaia.execute("setEmulatorReady", recvTimeout=20)
        flush_script = """setMediaLoaded"""
        tclMaia.execute(flush_script)
        result = device.device_ready(150)
        logging.info('Device Status: %s', result)
        assert all(result.values()), "Device not in ready state!"
    except ConnectionRefusedError:
        logging.info('The setEmulatorReady command not supported!')

    job.cancel_active_jobs()
    outputsaver.clear_output()
    # outputsaver.save_print_intents(True)
    outputsaver.save_pdl_intents(True)

    yield

    logging.info('-- TEARDOWN (Print/Copy Tests) --')

    try:
        media.get_alerts()
    except requests.exceptions.HTTPError:
        logging.warning('The CDM endpoint "/cdm/mediaHandling/v1/alerts" is not supported!')

    # outputsaver.save_print_intents(True)
    outputsaver.save_pdl_intents(False)
    outputsaver.clear_output()
    job.cancel_active_jobs()

    try:
        flush_script = """setMediaLoaded"""
        tclMaia.execute(flush_script)
    except ConnectionRefusedError:
        logging.info('The setMediaLoaded command not supported!')


    result = device.device_ready(100)
    logging.info('Device Status: %s', result)
    assert all(result.values()), "Device not in ready state!"


@pytest.fixture
def eventfactory(tcl, udw):
    yield EventFactory(tcl, udw)


@pytest.fixture
def syslogng(cdm):
    '''
    Test set-up and teardown
    '''
    syslogng_server = SyslogngSever()
    logging.info("****Start Syslog-ng Server****")
    # Start the syslg-ng server docker
    syslogng_server.start()
    # Get the source ip address of the syslog-ng server
    source_ip = syslogng_server.get_container_ip_address()
    # Enable syslog, by default enabled flage is true in configure_syslog method
    cdm.network.configure_syslog(server_id=source_ip)

    yield syslogng_server

    logging.info("*****Stop Syslog-ng Server****")
    syslogng_server.stop()
    # Disable syslog by setting enabled falg to false
    cdm.network.configure_syslog(enabled="false")

    logging.info("****Test Ends****")

@pytest.fixture
def syslogngServerOnly(cdm):
    '''
    Test set-up and teardown
    '''
    syslogng_server = SyslogngSever()
    logging.info("****Start Syslog-ng Server****")
    # Start the syslg-ng server docker
    syslogng_server.start()

    yield syslogng_server

    logging.info("*****Stop Syslog-ng Server****")
    syslogng_server.stop()
    # Disable syslog by setting enabled falg to false
    try:
        cdm.network.configure_syslog(enabled="false")
    except:
        logging.info("CDM Disable of syslogging failed. Syslog not supported.")
    logging.info("****Test Ends****")


@pytest.fixture
def onboard(request):
    """Onboard fixture."""
    yield Onboard(request.config.option.target)


@pytest.fixture
def cicada(request):
    cicada = CicadaServer()
    yield cicada
    log_path = request.config.option.capture_logs_to
    log_path = log_path if log_path else os.path.join('/code/output/')
    cicada.stop(log_path)

@pytest.fixture
def iot_pin_pairing():
    """IoT Pin Pairing fixture."""
    pin_pairing = IotPinPairing()
    yield pin_pairing
    pin_pairing.stop()

@pytest.fixture
def ip(net):
    yield net.ip_address

@pytest.fixture
def oobe(request, udw, device):
    yield OOBEFactory(request.config.option.target, udw, device)

@pytest.fixture
def web(request):
    """Web fixture."""
    yield Web()

@pytest.fixture
def ui_permissions_test_setup_teardown(cdm, spice, udw, syslogng, security_rbac_permissions, printer_user_authentication, ui_sign_in):
    """Dune Security Permissions Test Helper Fixture."""
    helper = UiPermissionsTestInitialize(cdm, spice, udw, syslogng)
    helper.testSetup()
    yield helper
    helper.testTeardown()

@pytest.fixture
def ui_network_user_group_permissions_test(cdm, ews, spice, udw, syslogng):
    """Network User Group Permissions Test Fixture"""
    fixture = NetworkUIUserGroupPermissions(cdm, ews, spice, udw, syslogng)
    fixture.setup()
    yield fixture
    fixture.teardown()

@pytest.fixture
def print_mapper(cdm):
    yield PrintMapper(cdm)

@pytest.fixture
def ioref(cdm,spice):
    yield Ioref(cdm,spice)

@pytest.fixture
def yeti(udw):
    yield Yeti(udw)

@pytest.fixture
def device_manager(net, ssh, udw, job):
    yield DeviceManager(net, ssh, udw, job)

@pytest.fixture
def pubsubserver():
    yield PubSubServer()

@pytest.fixture
def ph_maia(configuration, tclMaia, tcl, spice, ssh, net):
    yield phMaia(configuration, tclMaia, tcl, spice, ssh, net)

@pytest.fixture
def heater_maia(tclMaia):
    yield HeaterMaia(tclMaia)

@pytest.fixture
def media_info_maia(configuration):
    yield MediaInfoMaia(configuration)

@pytest.fixture
def job_configuration():
    yield JobConfiguration()

@pytest.fixture
def job_queue():
    yield JobQueue()

@pytest.fixture
def job_history():
    yield JobHistory()

@pytest.fixture
def finisher_name(request):
    """Finisher name fixture."""
    return request.config.option.finisher_name

@pytest.fixture
def enable_network_folder(cdm, udw):
    destination_config = cdm.get(cdm.DESTINATION_CONFIG_CDM_ENDPOINT)
    is_network_folder_enabled = destination_config["folderEnabled"]

    if is_network_folder_enabled == 'false':
        destination_config["folderEnabled"] = 'true'
        cdm.patch(cdm.DESTINATION_CONFIG_CDM_ENDPOINT, destination_config)

    yield Folder(cdm, udw)

    if is_network_folder_enabled == 'false':
        restore_config = cdm.get(cdm.DESTINATION_CONFIG_CDM_ENDPOINT)
        restore_config["folderEnabled"] = 'false'
        cdm.patch(cdm.DESTINATION_CONFIG_CDM_ENDPOINT, restore_config)