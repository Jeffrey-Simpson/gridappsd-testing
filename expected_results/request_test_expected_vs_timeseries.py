import json
import argparse
from gridappsd import GOSS, utils,GridAPPSD
import random
import time
import os

goss_sim = "goss.gridappsd.process.request.simulation"
test_input = "/topic/goss.gridappsd.simulation.test.input."

def start_test(simulationID=1234):
    loc = os.path.realpath(__file__)
    loc = os.path.dirname(loc)
    gapps = GridAPPSD()
    gapps.connect()

    test_id = str(random.getrandbits(32))
    testCfgAll = {
               "appId": "sample_app",
                "testId": test_id
               }

    with open(os.path.join(loc,"expected_result_series_filtered_123_normal_small_4.json")) as f:
    # with open("expected_result_series_filtered_9500.json") as f:
        expectedJson = json.load(f)

    testCfgAll['compareWithSimId'] = simulationID # 847461010
    testCfgAll['expectedResults'] = expectedJson['expectedResults']
    testCfgAll['testType'] = 'expected_vs_timeseries'
    request = json.dumps(testCfgAll)
    print('request:')
    print(json.dumps(testCfgAll,indent=2))
#     test_id=3657827110
#     viz_request ={
# 	"appId": "sample_app",
# 	"testId": 3657827110,
# 	"compareWithSimId": 402293585,
# 	"expectedResults": {
# 		"output": {
# 			"1248156002": {
# 				"simulation_id": "559402036",
# 				"message": {
# 					"timestamp": 1535574871,
# 					"measurements": [{
# 						"measurement_mrid": "_0028728e-4a2f-4ef7-b248-840319a3e370",
# 						"angle": -5.066423674487563,
# 						"magnitude": 2388.676720682955,
# 						"simulation_id": "1961648576",
# 						"time": 1248156002
# 					}, {
# 						"measurement_mrid": "_0018886d-363a-456c-8b1b-116e8c2e6fc6",
# 						"angle": -86.36800510651457,
# 						"magnitude": 1.4651647694061578,
# 						"simulation_id": "1961648576",
# 						"time": 1248156002
# 					}, {
# 						"measurement_mrid": "_00b26415-b4a0-4ef3-ab95-77e1beafc59a",
# 						"angle": 28.940770423235723,
# 						"magnitude": 374545.4981119089,
# 						"simulation_id": "1961648576",
# 						"time": 1248156002
# 					}]
# 				}
# 			}
# 		},
# 		"input": {
# 			"27": {
# 				"simulation_id": "559402036",
# 				"message": {
# 					"timestamp": 1587670665,
# 					"measurements": [{
# 						"hasMeasurementDifference": "FORWARD",
# 						"difference_mrid": "1fae379c-d0e2-4c80-8f2c-c5d7a70ff4d4",
# 						"simulation_id": "1961648576",
# 						"time": 1587670665,
# 						"attribute": "ShuntCompensator.sections",
# 						"value": 0,
# 						"object": "_939CA567-AA3D-4972-AABC-1D0AAF4859FE"
# 					}, {
# 						"hasMeasurementDifference": "REVERSE",
# 						"difference_mrid": "1fae379c-d0e2-4c80-8f2c-c5d7a70ff4d4",
# 						"simulation_id": "1961648576",
# 						"time": 1587670665,
# 						"attribute": "ShuntCompensator.sections",
# 						"value": 1,
# 						"object": "_939CA567-AA3D-4972-AABC-1D0AAF4859FE"
# 					}]
# 				}
# 			},
# 			"1248156014": {
# 				"simulation_id": "559402036",
# 				"message": {
# 					"timestamp": 1248156014,
# 					"measurements": [{
# 						"hasMeasurementDifference": "FORWARD",
# 						"difference_mrid": "1fae379c-d0e2-4c80-8f2c-c5d7a70ff4d4",
# 						"simulation_id": "1961648576",
# 						"time": 1248156014,
# 						"attribute": "ShuntCompensator.sections",
# 						"value": 1,
# 						"object": "_939CA567-AA3D-4972-AABC-1D0AAF4859FE"
# 					}, {
# 						"hasMeasurementDifference": "REVERSE",
# 						"difference_mrid": "1fae379c-d0e2-4c80-8f2c-c5d7a70ff4d4",
# 						"simulation_id": "1961648576",
# 						"time": 1248156014,
# 						"attribute": "ShuntCompensator.sections",
# 						"value": 0,
# 						"object": "_939CA567-AA3D-4972-AABC-1D0AAF4859FE"
# 					}]
# 				}
# 			},
# 			"1248156029": {
# 				"simulation_id": "559402036",
# 				"message": {
# 					"timestamp": 1248156029,
# 					"measurements": [{
# 						"hasMeasurementDifference": "FORWARD",
# 						"difference_mrid": "1fae379c-d0e2-4c80-8f2c-c5d7a70ff4d4",
# 						"simulation_id": "1961648576",
# 						"time": 1248156029,
# 						"attribute": "ShuntCompensator.sections",
# 						"value": 0,
# 						"object": "_939CA567-AA3D-4972-AABC-1D0AAF4859FE"
# 					}, {
# 						"hasMeasurementDifference": "REVERSE",
# 						"difference_mrid": "1fae379c-d0e2-4c80-8f2c-c5d7a70ff4d4",
# 						"simulation_id": "1961648576",
# 						"time": 1248156029,
# 						"attribute": "ShuntCompensator.sections",
# 						"value": 1,
# 						"object": "_939CA567-AA3D-4972-AABC-1D0AAF4859FE"
# 					}]
# 				}
# 			},
# 			"1248156044": {
# 				"simulation_id": "559402036",
# 				"message": {
# 					"timestamp": 1248156044,
# 					"measurements": [{
# 						"hasMeasurementDifference": "FORWARD",
# 						"difference_mrid": "1fae379c-d0e2-4c80-8f2c-c5d7a70ff4d4",
# 						"simulation_id": "1961648576",
# 						"time": 1248156044,
# 						"attribute": "ShuntCompensator.sections",
# 						"value": 0,
# 						"object": "_939CA567-AA3D-4972-AABC-1D0AAF4859FE"
# 					}, {
# 						"hasMeasurementDifference": "REVERSE",
# 						"difference_mrid": "1fae379c-d0e2-4c80-8f2c-c5d7a70ff4d4",
# 						"simulation_id": "1961648576",
# 						"time": 1248156044,
# 						"attribute": "ShuntCompensator.sections",
# 						"value": 1,
# 						"object": "_939CA567-AA3D-4972-AABC-1D0AAF4859FE"
# 					}]
# 				}
# 			}
# 		}
# 	},
# 	"testType": "expected_vs_timeseries"
# }
#     request = json.dumps(viz_request)
#

    # status = goss.get_response(test_input+str(simulationID), request, timeout=20)
    # status = goss.get_response(test_input+str(test_id), request, timeout=20)
    status = gapps.send(test_input+str(test_id), request)
    print(status)
    print('sent test status')
    return test_id

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--id", type=int, help="simulation id", required=False)
    args = parser.parse_args()

    start_test(simulationID=args.id)
