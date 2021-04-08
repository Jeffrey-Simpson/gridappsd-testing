from contextlib import contextmanager
import json
import logging
import os
import yaml
from time import sleep, time
import sys
import pytest

from gridappsd import GridAPPSD
from gridappsd.simulation import Simulation
from gridappsd import topics as t

LOGGER = logging.getLogger(__name__)

tapchanger_value = []
alarm_count = 0
mrid_values = {}


def compare_ids(measurement_id):
    def on_message(headers, message):
        global tapchanger_value
        global alarm_count
        global mrid_values

        if "gridappsd-alarms" in headers["destination"]:
            for y in message:
                print(message)
                if "Open" or "Close" in y['value']:
                    LOGGER.info(f'Alarm created {y}')
                    alarm_count += 1

        if "gridappsd-alarms" not in headers["destination"]:
            measurement_values = message["message"]["measurements"]
            for x in measurement_values:
                m = measurement_values[x]
                if m.get("measurement_mrid") == measurement_id:
                    if not tapchanger_value:
                        LOGGER.info(f'Tap Changer value is {m.get("value")}')
                        tapchanger_value.append(m.get("value"))
                    else:
                        if m.get("value") != tapchanger_value[-1]:
                            LOGGER.info(f'Tap Changer value changed from {tapchanger_value[-1]} to {m.get("value")} {m}')
                            tapchanger_value.append(m.get("value"))

    return on_message


def get_reg_mrids(gridappsd_obj, mrid):
    query = """
PREFIX r:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX c:  <http://iec.ch/TC57/CIM100#>
    SELECT ?reg_id ?trmid ?rname ?pname ?tname ?bus
    WHERE {
    VALUES ?fdrid {"%s"}  # 123
    ?pxf c:Equipment.EquipmentContainer ?fdr.
    ?fdr c:IdentifiedObject.mRID ?fdrid.
    ?rtc r:type c:RatioTapChanger.
    ?rtc c:IdentifiedObject.name ?rname.
    ?rtc c:IdentifiedObject.mRID ?reg_id.
    ?rtc c:RatioTapChanger.TransformerEnd ?end.
    ?end c:TransformerEnd.Terminal ?trm.
    ?trm c:IdentifiedObject.mRID ?trmid.
    ?trm c:Terminal.ConnectivityNode ?cn.
    ?cn c:IdentifiedObject.name ?bus.
    ?end c:TransformerEnd.endNumber ?wnum.
    OPTIONAL {?end c:TransformerTankEnd.phases ?phsraw.
    bind(strafter(str(?phsraw),"PhaseCode.") as ?phs)}
    ?end c:TransformerTankEnd.TransformerTank ?tank.
    ?tank c:TransformerTank.PowerTransformer ?pxf.
    ?pxf c:IdentifiedObject.name ?pname.
    ?tank c:IdentifiedObject.name ?tname.
    }
    ORDER BY ?pname ?tname ?rname ?wnum ?bus
    """ % mrid

    results_reg = gridappsd_obj.query_data(query)
    regulators = []
    reg_name = []
    results_obj = results_reg['data']
    # print(results_obj)
    return results_obj


@pytest.mark.parametrize("sim_config_file", [("13-new.json"), ("123-config.json"), ("9500-alarm-config.json")])
def test_alarm_output(gridappsd_client, sim_config_file):
    global measurement_id
    sim_config_file = os.path.join(os.path.dirname(__file__), f"simulation_config_files/{sim_config_file}")
    assert os.path.exists(sim_config_file), f"File {sim_config_file} must exist to run simulation test"

    gapps = gridappsd_client
    # Allow proven to come up
    sleep(30)

    sim_complete = False
    rcvd_measurement = False

    def onfinishsimulation(sim):
        nonlocal sim_complete
        sim_complete = True
        LOGGER.info('Simulation Complete')

    with open(sim_config_file) as fp:
        LOGGER.info('Loading config')
        run_config = json.load(fp)
        events = run_config["test_config"]["events"]
        switch_mrid1, switch_mrid2 = [], []
        # regulator_mrid1, regulator_mrid2 = [], []
        for i in range(len(events)):
            if "message" in events[i] and events[i]["message"]["forward_differences"][0]["attribute"] == "Switch.open":
                switch_mrid1.append(events[i]["message"]["forward_differences"][0]["object"])
                switch_mrid2.append(events[i]["message"]["reverse_differences"][0]["object"])

    model_mrid = run_config["power_system_config"]["Line_name"]
    try:

        equipment_dict = {}

        request1 = {
            "modelId": model_mrid,
            "requestType": "QUERY_OBJECT_DICT",
            "resultFormat": "JSON",
            "objectType": "LoadBreakSwitch"
        }

        request2 = {
            "modelId": model_mrid,
            "requestType": "QUERY_OBJECT_MEASUREMENTS",
            "resultFormat": "JSON",
            "objectType": "PowerTransformer"
        }

        response = gapps.get_response("goss.gridappsd.process.request.data.powergridmodel", request1, timeout=60)
        switch_list = []
        # print(response["data"])
        for switch in response["data"]:
            equipment_dict[switch["id"]] = switch
            switch_list.append(switch['IdentifiedObject.mRID'])
        # print("switch_list", switch_list)

        for i in range(min(3, len(switch_list))):
            print(i)
            run_config["test_config"]["events"][i]["message"]["forward_differences"][0]["object"] = switch_list[i]
            run_config["test_config"]["events"][i]["message"]["reverse_differences"][0]["object"] = switch_list[i]

        print("testing regulator")
        regulator = get_reg_mrids(gapps, model_mrid)
        value = regulator['results']['bindings'][0]['reg_id']['value']
        terminal_id = regulator['results']['bindings'][0]['trmid']['value']
        print("value", value, terminal_id)

        for i in range(len(events)):
            if "message" in events[i] and events[i]["message"]["forward_differences"][0]["attribute"] == "TapChanger.step":
                run_config["test_config"]["events"][i]["message"]["forward_differences"][0]["object"] = value
                run_config["test_config"]["events"][i]["message"]["reverse_differences"][0]["object"] = value
            if "inputOutageList" in events[i]:
                run_config["test_config"]["events"][i]["inputOutageList"][0]["objectMRID"] = value
        response2 = gapps.get_response("goss.gridappsd.process.request.data.powergridmodel", request2, timeout=60)
        for reg in response2["data"]:
            if reg['trmid'] == terminal_id:
                measurement_id = reg['measid']
                print(measurement_id, terminal_id)
    except Exception as e:
        message_str = "An error occurred while trying to translate the  message received" + str(e)

    LOGGER.info('Starting the simulation')
    LOGGER.info(f'Simulation start time {run_config["simulation_config"]["start_time"]}')
    sim = Simulation(gapps, run_config)
    # print(sim._run_config)
    sim.start_simulation(timeout=300)
    # regulators = sim.simulation_id, gapps, regulator
    LOGGER.info('sim.add_oncomplete_callback')
    sim.add_oncomplete_callback(onfinishsimulation)
    LOGGER.info("Querying for alarm topic")
    alarms_topic = t.service_output_topic('gridappsd-alarms', sim.simulation_id)
    log_topic = t.simulation_output_topic(sim.simulation_id)
    # print(gapps.subscribe(log_topic, compare_ids(measurement_id)))
    gapps.subscribe(alarms_topic, compare_ids(measurement_id))
    gapps.subscribe(log_topic, compare_ids(measurement_id))

    while not sim_complete:
        LOGGER.info('Sleeping')
        sleep(30)


def test_tap_changer():
    global tapchanger_value
    # commoutage prevents recording of last tap_changer change
    assert 10 in tapchanger_value, f"Expected tap changer values [4, 10] received {tapchanger_value}"


def test_comm_outage():
    global tapchanger_value
    # commoutage prevents recording of last tap_changer change
    assert 10 in tapchanger_value, f"Comm outage should prevent last tap change value from being recorded.  " \
                                        f"Expected values [4, 10] received {tapchanger_value} "


def test_alarm_count():
    global alarm_count
    assert alarm_count > 2, f"Expecting 3 alarms received {alarm_count}"
