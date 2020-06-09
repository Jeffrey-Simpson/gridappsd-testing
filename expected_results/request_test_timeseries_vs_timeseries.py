import json
import argparse
import random
from gridappsd import GOSS

goss_sim = "goss.gridappsd.process.request.simulation"
test_input = "/topic/goss.gridappsd.simulation.test.input."

def start_test(simulationID1, simulationID2):
    goss = GOSS()
    goss.connect()

    test_id = str(random.getrandbits(32))
    testCfgAll = {
               "appId": "sample_app",
                "testId": test_id
               }

    testCfgAll['compareWithSimId'] = simulationID1 # 847461010 # 660948920
    testCfgAll['compareWithSimIdTwo'] = simulationID2 # 912453649
    testCfgAll['testType'] = 'timeseries_vs_timeseries'
    request = json.dumps(testCfgAll)

    status = goss.get_response(test_input+str(test_id), request, timeout=60)
    print(status)
    print('sent test status')
    return test_id

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--id1", type=int, help="simulation id 1", required=False)
    parser.add_argument("-j", "--id2", type=int, help="simulation id 2", required=False)
    args = parser.parse_args()

    start_test(simulationID1=args.id1, simulationID2=args.id2)
