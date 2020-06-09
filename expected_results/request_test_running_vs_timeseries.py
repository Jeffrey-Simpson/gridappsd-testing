import json
import time
import os
import argparse
from gridappsd import GOSS
import random

goss_sim = "goss.gridappsd.process.request.simulation"
test_topic = 'goss.gridappsd.test'
responseQueueTopic = '/temp-queue/response-queue'
goss_simulation_status_topic = '/topic/goss.gridappsd/simulation/status/'

def start_test(simulationID):
    events = [{
        "message": {
            "forward_differences": [
                {
                    "object": "_307E4291-5FEA-4388-B2E0-2B3D22FE8183",
                    "attribute": "ShuntCompensator.sections",
                    "value": "0"
                }
            ],
            "reverse_differences": [
                {
                    "object": "_307E4291-5FEA-4388-B2E0-2B3D22FE8183",
                    "attribute": "ShuntCompensator.sections",
                    "value": "1"
                }
            ]
        },
        "event_type": "ScheduledCommandEvent",
        "occuredDateTime": 1248156002 + 6,
        "stopDateTime": 1248156002 + 21
    }]

    test_id = str(random.getrandbits(32))
    testCfgAll = {
               "appId": "sample_app",
               "testId": test_id
               }

    # # testCfgAll['events'] = events

    req_template = {"power_system_config": {"SubGeographicalRegion_name": "_1CD7D2EE-3C91-3248-5662-A43EFEFAC224",
                                            "GeographicalRegion_name": "_24809814-4EC6-29D2-B509-7F8BFB646437",
                                            "Line_name": "_C1C3E687-6FFD-C753-582B-632A27E28507"},
                    "simulation_config": {"power_flow_solver_method": "NR", "duration": 120,
                                          "simulation_name": "ieee123", "simulator": "GridLAB-D",
                                          "start_time": 1248156000, "run_realtime": True, "simulation_output": {},
                                          "model_creation_config": {"load_scaling_factor": 1.0, "triplex": "y",
                                                                    "encoding": "u", "system_frequency": 60,
                                                                    "voltage_multiplier": 1.0,
                                                                    "power_unit_conversion": 1.0, "unique_names": "y",
                                                                    "schedule_name": "ieeezipload", "z_fraction": 0.0,
                                                                    "i_fraction": 1.0, "p_fraction": 0.0,
                                                                    "randomize_zipload_fractions": False,
                                                                    "use_houses": False},
                                          "simulation_broker_port": 52798, "simulation_broker_location": "127.0.0.1"},
                    "application_config": {"applications": [{"name": "sample_app", "config_string": ""}]},
                    "simulation_request_type": "NEW"}
    req_template['simulation_config']['duration'] = 60
    req_template['power_system_config']['Line_name'] = '_C1C3E687-6FFD-C753-582B-632A27E28507'  # IEEE 123
    # req_template['power_system_config']['Line_name'] = '_AAE94E4A-2465-6F5E-37B1-3E72183A4E44'  # test9500new

    req_template["application_config"]["applications"][0]['name'] = 'sample_app'
    # req_template["application_config"]["applications"][0]['name'] = 'sample_app_opp'

    req_template['test_config'] = testCfgAll

    goss = GOSS()
    goss.connect()

    req_template['test_config']['compareWithSimId'] = simulationID # 913015800
    req_template['test_config']['testType'] ='simulation_vs_timeseries'
    print(json.dumps(req_template['test_config'], indent=2))
    simCfg13pv = json.dumps(req_template)

    simulationId = goss.get_response(goss_sim, simCfg13pv, timeout=10)
    print('sent simulation request')
    print('simulation id ', simulationId)

    return(simulationId['simulationId'],test_id)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--id", type=int, help="simulation id", required=False)
    args = parser.parse_args()

    start_test(simulationID=args.id)
