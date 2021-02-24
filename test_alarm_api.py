from contextlib import contextmanager
import json
import logging
import os
import yaml
from time import sleep, time
import sys
import pytest
from assumptions import CapacitorToggler as c
from gridappsd import GridAPPSD
from gridappsd.simulation import Simulation
from gridappsd_docker import docker_up, docker_down
from gridappsd import topics as t

LOGGER = logging.getLogger(__name__)

tapchanger_value = []
alarm_count = 0
mrid_values = {}


def on_message(headers, message):
    global tapchanger_value
    global alarm_count
    global mrid_values

    if "gridappsd-alarms" in headers["destination"]:
        if "ln1047pvfrm_sw" or "ln5001chp_sw" or "ln0895780_sw" in \
                message['equipment_name']:
            for y in message:
                if "Open" in y['value']:
                    LOGGER.info(f'Alarm created {y}')
                    alarm_count += 1

    if "gridappsd-alarms" not in headers["destination"]:
        measurement_values = message["message"]["measurements"]
        for x in measurement_values:
            m = measurement_values[x]
            if m.get("measurement_mrid") == "_9c869e50-c9c6-49bb-b1f3-949841a06ed3":
                if not tapchanger_value:
                    LOGGER.info(f'Tap Changer value is {m.get("value")}')
                    tapchanger_value.append(m.get("value"))
                else:
                    if m.get("value") != tapchanger_value[-1]:
                        LOGGER.info(f'Tap Changer value changed from {tapchanger_value[-1]} to {m.get("value")} {m}')
                        tapchanger_value.append(m.get("value"))


@pytest.mark.parametrize("sim_config_file, sim_result_file", [
    ("9500-alarm-config.json", "9500-alarm-simulation.output")

])
def test_alarm_output(gridappsd_client, sim_config_file, sim_result_file):
    sim_config_file = os.path.join(os.path.dirname(__file__), f"simulation_config_files/{sim_config_file}")
    sim_result_file = os.path.join(os.path.dirname(__file__), f"simulation_baseline_files/{sim_result_file}")
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
        # print(run_config["test_config"]["events"])
        events = run_config["test_config"]["events"]
        switch_mrid1, switch_mrid2 = [], []
        for i in range(len(events)):
            if "message" in events[i] and events[i]["message"]["forward_differences"][0]["attribute"] == "Switch.open":
                switch_mrid1.append(events[i]["message"]["forward_differences"][0]["object"])
                switch_mrid2.append(events[i]["message"]["reverse_differences"][0]["object"])
        LOGGER.info(f'Simulation start time {run_config["simulation_config"]["start_time"]}')
    sim = Simulation(gapps, run_config)
    model_mrid = run_config["power_system_config"]["Line_name"]
    try:

        equipment_dict = {}
        # measurement_dict = {}
        capacitors_dict = {}
        switches_dict = {}
        # request1 = {
        #     "modelId": model_mrid,
        #     "requestType": "QUERY_OBJECT_DICT",
        #     "resultFormat": "JSON",
        #     "objectType": "RatioTapChanger"
        # }
        #
        # response = gapps.get_response("goss.gridappsd.process.request.data.powergridmodel", request1, timeout=60)
        # print(response["data"])

        request2 = {
            "modelId": model_mrid,
            "requestType": "QUERY_OBJECT_DICT",
            "resultFormat": "JSON",
            "objectType": "LoadBreakSwitch"
        }

        response = gapps.get_response("goss.gridappsd.process.request.data.powergridmodel", request2, timeout=60)
        print(response["data"])
        name = {'ln1047pvfrm_sw': 0, 'ln0895780_sw': 1, 'ln5001chp_sw': 2}
        for switch in response["data"]:
            equipment_dict[switch["id"]] = switch
            if switch['IdentifiedObject.name'] in {'ln1047pvfrm_sw', 'ln0895780_sw', 'ln5001chp_sw'}:
                switch_mrid1[name[switch['IdentifiedObject.name']]] = switch['IdentifiedObject.mRID']
                switch_mrid2[name[switch['IdentifiedObject.name']]] = switch['IdentifiedObject.mRID']
                print("passed")

        for i in range(len(switch_mrid1)):
            print(run_config["test_config"]["events"])
            run_config["test_config"]["events"][i]["message"]["forward_differences"][0]["object"] = switch_mrid1[i]
            run_config["test_config"]["events"][i]["message"]["reverse_differences"][0]["object"] = switch_mrid2[i]



    except Exception as e:
        message_str = "An error occurred while trying to translate the  message received" + str(e)

    LOGGER.info('Starting the simulation')
    sim.start_simulation(timeout=300)
    LOGGER.info('sim.add_oncomplete_callback')
    sim.add_oncomplete_callback(onfinishsimulation)
    LOGGER.info("Querying for alarm topic")
    alarms_topic = t.service_output_topic('gridappsd-alarms', sim.simulation_id)
    log_topic = t.simulation_output_topic(sim.simulation_id)
    gapps.subscribe(alarms_topic, on_message)
    gapps.subscribe(log_topic, on_message)

    while not sim_complete:
        LOGGER.info('Sleeping')
        sleep(30)


def test_tap_changer():
    global tapchanger_value
    # commoutage prevents recording of last tap_changer change
    # assert tapchanger_value == [4, 10, 5], f"Expected tap changer values [4, 10, 5] received {tapchanger_value}"
    assert tapchanger_value == [4, 10], f"Expected tap changer values [4, 10] received {tapchanger_value}"


def test_comm_outage():
    global tapchanger_value
    # commoutage prevents recording of last tap_changer change
    assert tapchanger_value == [4,10], f"Comm outage should prevent last tap change value from being recorded.  Expected values [4, 10] received {tapchanger_value}"


def test_alarm_count():
    global alarm_count
    assert alarm_count == 3, f"Expecting 3 alarms received {alarm_count}"
