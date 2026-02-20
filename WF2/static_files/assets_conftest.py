import pytest
import logging
import json
import requests
from dunetuf.oobe.oobe import OOBE


PATH_DUMP_JSON = "/tmp/activeFlowStepsDump.json"

@pytest.fixture()
def setup_teardown_ui(spice, device, job):
    """Setup/teardown fixture for UI tests."""
    logging.info('-- SETUP (UI Tests) --')

    spice.goto_homescreen()
    job.wait_for_no_active_jobs()
    
    yield
    
    logging.info('-- TEARDOWN (UI Tests) --')
    
    spice.goto_homescreen() 
    job.wait_for_no_active_jobs()
    
    result = device.device_ready(10)
    logging.info('Device Status: %s', result)
    assert all(result.values()), "Device not in ready state!"

@pytest.fixture()
def setup_teardown_custom_substrate(cdm, spice):
    """Setup/teardown fixture for custom substrate tests."""
    
    logging.info('-- SETUP (Custom substrate Tests) --')
    
    # Delete created substrate
    substrate_ids = cdm.media.get_media_custom_substrates()
    if len(substrate_ids) > 0:
        for substrate_id in substrate_ids:
            logging.info("Deleting Media with ID: {}".format(substrate_id))
            cdm.media.delete_media(substrate_id)
    
    spice.goto_homescreen()

    yield

    logging.info('-- TEARDOWN (Custom substrate Tests) --')
   
    spice.goto_homescreen()

    # Delete created substrate
    substrate_ids = cdm.media.get_media_custom_substrates()
    if len(substrate_ids) > 0:
        for substrate_id in substrate_ids:
            logging.info("Deleting Media with ID: {}".format(substrate_id))
            cdm.media.delete_media(substrate_id)



@pytest.fixture()
def setup_teardown_add_print_time(tcl, tray, cdm, tclMaia):
    logging.info("Setup")
    try:
        tcl.execute("EngineSimulatorUw executeSimulatorAction PRINT setPrintSimulationConfiguration {{ printTimePerPageInMilliseconds: 65000 }}")
    except:
        tclMaia.execute("setEmulatorReady",  recvTimeout=20)
    response = cdm.get_raw(cdm.SYSTEM_IDENTITY)
    assert response.status_code == 200
    data = json.loads(response.content)
    product = data["makeAndModel"]["base"] 
    if("HP Latex"  in product):
        try:
            tray.load_simulator_media(tcl, "GENERIC_SAV", "150100")
        except:
            tclMaia.execute("setMediaLoaded ROLL 64 150100", recvTimeout=20)
    elif("HP DesignJet XL 3800"  in product):
        tray.reset_trays()
    
    yield

    logging.info("Teardown")
    try:
        tcl.execute("EngineSimulatorUw executeSimulatorAction PRINT setPrintSimulationConfiguration {{ printTimePerPageInMilliseconds: 0 }}")
    except:
        pass


@pytest.fixture()
def load_tray(tray, tcl, tclMaia):
    try:
        tclMaia.execute("setEmulatorReady", recvTimeout=20)
    except:
        tray.load_simulator_media(tcl, "GENERIC_SAV", "150100")
    

    
    
@pytest.fixture()
def setup_teardown_set_emulator_ready(ssh, net, tclMaia, spice, tcl,maiaEngine):

    #--------- Set Up -----------

    logging.info("Test GuidedFlow Set Up")

    # Wait for HomeScreen to appear and dismiss SystemError if exists
    spice.cleanSystemEventAndWaitHomeScreen()

    ssh.run("rm -f /tmp/EngineStatusDump_*_auto_*")
    ssh.run("rm -f /tmp/activeFlowStepsDump.json")

    # Register to status changes
    tcl.execute("EngineStatusDriver registerStatus")

    # Set maia as ready
    tclMaia.execute("setEmulatorReady", recvTimeout=20)
    flush_script = """setMediaLoaded"""
    tclMaia.execute(flush_script)
    # Finishes OOBE steps if device is in OOBE
    oobe = OOBE(net.ip_address)
    resp = oobe.complete_OOBE()
    print("OOBE Done Resp :{0}".format(resp))
    
    
    # Sets ph oobe nvm bit
    maiaEngine.set_oobe_state("1")
    assert maiaEngine.is_Oobe_Done()
    # Wait until engine is ready
    tcl.wait_for_status("IDLE")

    # Start json dump.
    tcl.execute("GuidedFlowDriver startDump " + PATH_DUMP_JSON)

    #--------- Execute Test ----------

    yield

    #--------- Test Tear Down --------

    logging.info("Test Tear Down")

    try:
        tclMaia.supplies.close_ph_door()
    except:
        pass
    # Forcing an update to ensure a EngineStatus update and that we come back to IDLE
    tclMaia.execute("setEmulatorReady", recvTimeout=20)
    flush_script = """setMediaLoaded"""
    tclMaia.execute(flush_script)
    # Wait until engine is ready
    tcl.wait_for_status("IDLE")

    ## Stop json dump.
    tcl.execute("GuidedFlowDriver stopDump")
    ssh.run("rm -f /tmp/EngineStatusDump_*_auto_*")
    ssh.run("rm -f /tmp/activeFlowStepsDump.json")
    
    # Wait for HomeScreen to appear
    spice.goto_homescreen()
