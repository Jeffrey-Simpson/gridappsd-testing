import json
import time
import os
import argparse
# import goss_forward_sim
from gridappsd import GOSS
# from pprint import pprint
goss_sim = "goss.gridappsd.process.request.simulation"
test_topic = 'goss.gridappsd.test'
responseQueueTopic = '/temp-queue/response-queue'
goss_simulation_status_topic = '/topic/goss.gridappsd/simulation/status/'
def makeJavaString(request, name="requestString"):
    javaString = json.dumps(json.loads(request)).replace('"','\\"')
    javaString = "String " + name + ' = "' + javaString + '";'
    print(javaString)

def _startTest(username,password,gossServer='localhost',stompPort='61613', simulationID=1234, rulePort=5000, topic="input"):
    loc = os.path.realpath(__file__)
    loc = os.path.dirname(loc)
    # loc =  os.path.dirname(os.path.dirname(os.path.dirname(loc)))
    # loc ='/gridappsd/applications/sample_app/tests' # DOCKER
    print(loc)

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



    testCfg = {"testConfigPath":loc+"/SampleTestConfig.json",
            "testScriptPath":loc+"/SampleTestScript.json",
            "simulationID": 1234,
            "rulePort": 5000,
            "topic":"input",
            "expectedResultPath":loc + "/expected_result_series_filtered_8500_2.json"
            }

    testCfgAll = {
               "simulationID": 1234,
               "rulePort": 5000,
               "topic": "input"
               }

    testCfgAll = {

               "appId": "sample_app"
               }

    testHistCfgAll = {
               "simulationID": 1234,
               "rulePort": 5000,
               "topic": "input"
               }

    testHistCfg = {"testConfigPath":loc+"/SampleHistoricalTestConfig.json",
            "testScriptPath":loc+"/SampleTestScript.json",
            "simulationID": 1234,
            "rulePort": 5000,
            "topic":"input",
            "expectedResult":loc + "/expected_result_series_filtered_8500.json"
            }

    # with open("SampleTestConfig.json") as f:
    #     testCfgJson = json.load(f)

    with open(os.path.join(loc,"..","SampleTestScript.json")) as f:
        tesScriptJson = json.load(f)

    with open(os.path.join(loc,"..","SampleHistoricalTestConfig.json")) as f:
        testHistCfg = json.load(f)

    # with open("expected_result_series_filtered_8500_2_small.json") as f:
    #     expectedJson = json.load(f)

    # with open("expected_result_series_filtered_123_pv_small.json") as f:
    #     expectedJson = json.load(f)

    with open("expected_result_series_filtered_123_normal_small_4.json") as f:
        expectedJson = json.load(f)

    # print(testCfgJson)
    # print(tesScriptJson)
    # print(expectedJson)
    # testCfgAll['test_config'] = testCfgJson
    # testCfgAll['testScript'] = tesScriptJson
    testCfgAll['expectedResults'] = expectedJson['expectedResults']
    testCfgAll['events'] = events
    testHistCfgAll['test_config'] = testHistCfg
    testHistCfgAll['testScript'] = tesScriptJson
    testHistCfgAll['expectedResults'] = expectedJson['expectedResults']

    # pprint(testCfgAll)
    # print(json.dumps(testCfgAll,indent=2))

    #  2009-07-21 00:00:00
    # 1248156000

    req_template = {"power_system_config":{"SubGeographicalRegion_name":"_1CD7D2EE-3C91-3248-5662-A43EFEFAC224","GeographicalRegion_name":"_24809814-4EC6-29D2-B509-7F8BFB646437","Line_name":"_C1C3E687-6FFD-C753-582B-632A27E28507"},"simulation_config":{"power_flow_solver_method":"NR","duration":120,"simulation_name":"ieee123","simulator":"GridLAB-D","start_time":1248156000,"run_realtime":True,"simulation_output":{},"model_creation_config":{"load_scaling_factor":1.0,"triplex":"y","encoding":"u","system_frequency":60,"voltage_multiplier":1.0,"power_unit_conversion":1.0,"unique_names":"y","schedule_name":"ieeezipload","z_fraction":0.0,"i_fraction":1.0,"p_fraction":0.0,"randomize_zipload_fractions":False,"use_houses":False},"simulation_broker_port":52798,"simulation_broker_location":"127.0.0.1"},"application_config":{"applications":[{"name":"sample_app","config_string":""}]},"simulation_request_type":"NEW"}
    req_template['simulation_config']['duration'] = 60
    # req_template['simulation_config']['start_time'] = 1538484951
    # req_template['simulation_config']['start_time'] = 1530000000 # Tuesday, June 26, 2018 2:00:00 AM GMT-06:00 DST
    # req_template['power_system_config']['Line_name'] = '_E407CBB6-8C8D-9BC9-589C-AB83FBF0826D'  # Mine 123pv
    # req_template['power_system_config']['Line_name'] = '_4F76A5F9-271D-9EB8-5E31-AA362D86F2C3'  # IEEEE 8500
    req_template['power_system_config']['Line_name'] = '_C1C3E687-6FFD-C753-582B-632A27E28507'  # IEEE 123

    # req_template['power_system_config']['Line_name'] = '_C77C898B-788F-8442-5CEA-0D06ABA0693B'  # 123 PV REG
    # req_template['power_system_config']['Line_name'] = '_EBDB5A4A-543C-9025-243E-8CAD24307380'

    req_template["application_config"]["applications"][0]['name'] = 'sample_app'
    # req_template["application_config"]["applications"][0]['name'] = 'der_dispatch_app'

    req_template['test_config'] = testCfgAll
    # testCfgAll['testScript'] = tesScriptJson
    # req_template['expectedResults'] = expectedJson['expectedResults']

    simCfg13pv = json.dumps(req_template)
    print(simCfg13pv)
    print()
    print(makeJavaString(simCfg13pv))
    print()
    print(json.dumps(testCfgAll,indent=2))

    goss = GOSS()
    goss.connect()

    # simulationId =123
    test_hist_old = False
    test_compare = False
    if test_hist_old:
        testHistCfgAll['test_config']['compareWithSimId'] = 559402036
        testHistCfgAll['test_config']['testType'] = 'simulation_vs_expected'
        testHistCfgAll = json.dumps(testHistCfgAll)
        print(testHistCfgAll)
        goss.send(test_topic, testHistCfgAll)

        time.sleep(1)
        print('sent testHistCfgAll request')
    elif test_compare:
        del req_template['test_config']['expectedResults']
        req_template['test_config']['compareWithSimId'] = 559402036
        exit(0)
        simCfg13pv = json.dumps(req_template)
        simulationId = goss.get_response(goss_sim, simCfg13pv, timeout=10)
        print('sent simulation request')
        time.sleep(1)
    else:
        simulationId = goss.get_response(goss_sim, simCfg13pv, timeout=10)
        print('sent simulation request')
        print('simulation id ', simulationId)
        time.sleep(1)

        testCfgAll['simulationID'] = simulationId
        # testCfgAll['simulationID'] = 653676970
        testCfgAll = json.dumps(testCfgAll)
        print(testCfgAll)
        # goss.send(test_topic, testCfgAll)

        time.sleep(1)
        print('sent test request')





if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t","--topic", type=str, help="topic, the default is input", default="input", required=False)
    parser.add_argument("-p","--port", type=int, help="port number, the default is 5000", default=5000, required=False)
    parser.add_argument("-i", "--id", type=int, help="simulation id", required=False)
    # parser.add_argument("--start_date", type=str, help="Simulation start date", default="2017-07-21 12:00:00", required=False)
    # parser.add_argument("--end_date", type=str, help="Simulation end date" , default="2017-07-22 12:00:00", required=False)
    # parser.add_argument('-o', '--options', type=str, default='{}')
    args = parser.parse_args()

    _startTest('system','manager',gossServer='127.0.0.1',stompPort='61613', simulationID=args.id, rulePort=args.port, topic=args.topic)


 # python /usr/src/gridappsd-sample/sample_app/runsample.py 1201658254 {"power_system_config":{"SubGeographicalRegion_name":"_1CD7D2EE-3C91-3248-5662-A43EFEFAC224","GeographicalRegion_name":"_24809814-4EC6-29D2-B509-7F8BFB646437","Line_name":"_C1C3E687-6FFD-C753-582B-632A27E28507"},"simulation_config":{"power_flow_solver_method":"NR","duration":120,"simulation_name":"ieee123","simulator":"GridLAB-D","start_time":1248156000,"run_realtime":true,"simulation_output":{},"model_creation_config":{"load_scaling_factor":1.0,"triplex":"y","encoding":"u","system_frequency":60,"voltage_multiplier":1.0,"power_unit_conversion":1.0,"unique_names":"y","schedule_name":"ieeezipload","z_fraction":0.0,"i_fraction":1.0,"p_fraction":0.0,"randomize_zipload_fractions":false,"use_houses":false},"simulation_broker_port":52798,"simulation_broker_location":"127.0.0.1"},"application_config":{"applications":[{"name":"sample_app","config_string":""}]},"simulation_request_type":"NEW"}