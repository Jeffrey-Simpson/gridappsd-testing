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
    testCfgAll['compareWithSimId'] = 1062322800 # 660948920
    testCfgAll['compareWithSimIdTwo'] = 272071421
    testCfgAll['testType'] = 'timeseries_vs_timeseries'
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

#{'data': [{'allOutputOutage': False, 'allInputOutage': False, 'inputOutageList': [{'objectMRID': '_233D4DC1-66EA-DF3C-D859-D10438ECCBDF', 'attribute': 'PowerElectronicsConnection.p'}, {'objectMRID': '_233D4DC1-66EA-DF3C-D859-D10438ECCBDF', 'attribute': 'PowerElectronicsConnection.q'}, {'objectMRID': '_60E702BC-A8E7-6AB8-F5EB-D038283E4D3E', 'attribute': 'PowerElectronicsConnection.p'}, {'objectMRID': '_60E702BC-A8E7-6AB8-F5EB-D038283E4D3E', 'attribute': 'PowerElectronicsConnection.q'}], 'outputOutageList': ['_facde6ab-95e2-471b-b151-1b7125d863f0', '_888e15c8-380d-4dcf-9876-ccf8949d45b1'], 'faultMRID': '_f05569df-665f-4b25-b721-926ff32b4ab3', 'event_type': 'CommOutage', 'occuredDateTime': 1374510750, 'stopDateTime': 1374510960, 'status': 'CLEARED'}]}
#{'data': [{'allOutputOutage': False, 'allInputOutage': False, 'inputOutageList': [{'objectMRID': '_233D4DC1-66EA-DF3C-D859-D10438ECCBDF', 'attribute': 'PowerElectronicsConnection.p'}, {'objectMRID': '_233D4DC1-66EA-DF3C-D859-D10438ECCBDF', 'attribute': 'PowerElectronicsConnection.q'}, {'objectMRID': '_60E702BC-A8E7-6AB8-F5EB-D038283E4D3E', 'attribute': 'PowerElectronicsConnection.p'}, {'objectMRID': '_60E702BC-A8E7-6AB8-F5EB-D038283E4D3E', 'attribute': 'PowerElectronicsConnection.q'}], 'outputOutageList': ['_facde6ab-95e2-471b-b151-1b7125d863f0', '_888e15c8-380d-4dcf-9876-ccf8949d45b1'], 'faultMRID': '_b93ae63b-c959-476f-a4e8-3020be90db2c', 'event_type': 'CommOutage', 'occuredDateTime': 1374510750, 'stopDateTime': 1374510960, 'status': 'INITIATED'}]}
