import time
import json
from gridappsd import GOSS
import request_test_expected_vs_timeseries
import request_test_timeseries_vs_timeseries
from pytest import fixture

@fixture
def sim_id1():
    with open('test_ids.json') as f:
        d = json.load(f)
    print(d)
    return int(d['sim_id2'])


@fixture
def sim_id2():
    with open('test_ids.json') as f:
        d = json.load(f)
    print(d)
    return int(d['sim_id2'])

def test_expected(sim_id1, sim_id2):
    # sim_id, test_id = request_test_expected_vs_running.start_test()
    # time.sleep(75)
    print('sent test request')
    log_topic = 'goss.gridappsd.process.request.data.log'
    goss = GOSS()
    goss.connect()
    query = '{"query":"select * from expected_results"}'
    # test_id = "1702722370"
    # sim_id = "847461010"
    # select * from expected_results where  match_flag=0 and difference_direction<>'NA'
    # count_query = '{"query":"select COUNT(*) from expected_results where test_id=\'' + test_id + '\' and match_flag=0"}'
    # response = goss.get_response(log_topic, count_query, timeout=10)
    # print(response['data'][0]['COUNT(*)'] == '5')
    # query = '{"query":"select * from expected_results where test_id=\'' + test_id + '\' and match_flag=0"}'
    # response = goss.get_response(log_topic, query, timeout=10)
    # for i in response['data']:
    #     print(i)

    test_id = request_test_expected_vs_timeseries.start_test(sim_id1)
    time.sleep(2)
    count_query = '{"query":"select COUNT(*) from expected_results where test_id=\'' + test_id + '\' and match_flag=0"}'
    response = goss.get_response(log_topic, count_query, timeout=10)
    test_3_count = response['data'][0]['COUNT(*)']
    print(test_3_count)
    print(test_3_count == '7') # 5?
    # assert test_3_count != 7, f" For expected_vs_timeseries expecting 7 non matching results. Received {test_3_count}"
    query = '{"query":"select * from expected_results where test_id=\'' + test_id + '\' and match_flag=0"}'
    print(query)
    response = goss.get_response(log_topic, query, timeout=10)
    for i in response['data']:
        print(i)
    # {"1248156014":{"message":{"measurements":[{"hasMeasurementDifference":"FORWARD","difference_mrid":"c7e477f5-208e-401f-a032-30570e86f695","attribute":"ShuntCompensator.sections","value":0.0,"object":"_939CA567-AA3D-4972-AABC-1D0AAF4859FE"},{"hasMeasurementDifference":"REVERSE","difference_mrid":"c7e477f5-208e-401f-a032-30570e86f695","attribute":"ShuntCompensator.sections","value":1.0,"object":"_939CA567-AA3D-4972-AABC-1D0AAF4859FE"}]}},"1248156029":{"message":{"measurements":[{"hasMeasurementDifference":"FORWARD","difference_mrid":"44d77bf5-0b88-4a68-acee-20cd4f72494c","attribute":"ShuntCompensator.sections","value":1.0,"object":"_939CA567-AA3D-4972-AABC-1D0AAF4859FE"},{"hasMeasurementDifference":"REVERSE","difference_mrid":"44d77bf5-0b88-4a68-acee-20cd4f72494c","attribute":"ShuntCompensator.sections","value":0.0,"object":"_939CA567-AA3D-4972-AABC-1D0AAF4859FE"}]}},"1248156044":{"message":{"measurements":[{"hasMeasurementDifference":"REVERSE","difference_mrid":"92098f43-8f26-4652-8078-072ed2a005c0","attribute":"ShuntCompensator.sections","value":1.0,"object":"_939CA567-AA3D-4972-AABC-1D0AAF4859FE"},{"hasMeasurementDifference":"FORWARD","difference_mrid":"92098f43-8f26-4652-8078-072ed2a005c0","attribute":"ShuntCompensator.sections","value":0.0,"object":"_939CA567-AA3D-4972-AABC-1D0AAF4859FE"}]}}}
    # exit(0)

    test_id = request_test_timeseries_vs_timeseries.start_test(sim_id1, sim_id1)
    time.sleep(2)
    count_query = '{"query":"select COUNT(*) from expected_results where test_id=\'' + test_id + '\' and match_flag=0"}'
    response = goss.get_response(log_topic, count_query, timeout=10)
    print(response['data'][0]['COUNT(*)'])
    test_4_count = response['data'][0]['COUNT(*)']
    print(test_4_count == '0')
    # assert test_4_count != 0, f" For timeseries_vs_timeseries expecting 0 non matching results. Received {test_4_count}"

    query = '{"query":"select * from expected_results where test_id=\'' + test_id + '\' and match_flag=0"}'
    print(query)
    response = goss.get_response(log_topic, query, timeout=120)
    for i in response['data']:
        print(i)

    test_id = request_test_timeseries_vs_timeseries.start_test(sim_id1, sim_id2)
    time.sleep(5)
    # count_query = '{"query":"select COUNT(*) from expected_results where test_id=\'' + test_id + '\' and match_flag=0"}'
    # print(count_query)
    # response = goss.get_response(log_topic, count_query, timeout=10)
    # print(response['data'][0]['COUNT(*)'])
    # print(response['data'][0]['COUNT(*)'] == '0')
    query = '{"query":"select * from expected_results where test_id=\'' + test_id + '\' and match_flag=0"}'
    print(query)
    response = goss.get_response(log_topic, query, timeout=120)
    for i in response['data']:
        print(i)


if __name__ == '__main__':
    with open('test_ids.json') as f:
        d = json.load(f)
    print(d)
    test_expected(int(d['sim_id1']), int(d['sim_id2']))
    # test_expected(273529813, 2272136042)
    # test_expected(1232216123, 2040676147)
