import json
import time
import argparse
from gridappsd import GOSS
from pprint import pprint
goss_sim = "goss.gridappsd.process.request.simulation"
test_input = "/topic/goss.gridappsd.simulation.test.input."

def _startTest(username,password,gossServer='localhost',stompPort='61613', simulationID=1234):
    goss = GOSS()
    goss.connect()

    testCfgAll = {
               "appId": "sample_app"
               }
    testCfgAll['testType'] = 'expected_vs_timeseries'
    with open("expected_result_series_filtered_123_normal_small_4.json") as f:
    # with open("expected_result_series_filtered_9500.json") as f:
        expectedJson = json.load(f)

    testCfgAll['expectedResults'] = expectedJson['expectedResults']

    testCfgAll['compareWithSimId'] = 1121239269 # 272071421
    request = json.dumps(testCfgAll)
    simulationID=1259505150

    # simulationId =123
    status = goss.get_response(test_input+str(simulationID), request, timeout=10)
    print(status)
    print('sent test status')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--id", type=int, help="simulation id", required=False)
    args = parser.parse_args()

    _startTest('system','manager',gossServer='127.0.0.1',stompPort='61613', simulationID=args.id)
