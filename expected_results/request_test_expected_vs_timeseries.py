import json
import argparse
from gridappsd import GOSS
import random
import time
import os

goss_sim = "goss.gridappsd.process.request.simulation"
test_input = "/topic/goss.gridappsd.simulation.test.input."

def start_test(simulationID=1234):
    loc = os.path.realpath(__file__)
    loc = os.path.dirname(loc)
    goss = GOSS()
    goss.connect()

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

    # status = goss.get_response(test_input+str(simulationID), request, timeout=20)
    # status = goss.get_response(test_input+str(test_id), request, timeout=20)
    status = goss.send(test_input+str(test_id), request)
    print(status)
    print('sent test status')
    return test_id

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--id", type=int, help="simulation id", required=False)
    args = parser.parse_args()

    start_test(simulationID=args.id)
