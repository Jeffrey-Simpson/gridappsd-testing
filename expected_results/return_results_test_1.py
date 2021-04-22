import time
import json
from gridappsd import GOSS,  utils, topics as t
import request_test_expected_vs_timeseries
import request_test_expected_vs_running
import request_test_running_vs_timeseries
import request_test_timeseries_vs_timeseries


def test_expected():
    sim_id, test_id = request_test_expected_vs_running.start_test()
    print('sent test request ' + test_id)
    time.sleep(75)
    log_topic = 'goss.gridappsd.process.request.data.log'

    goss = GOSS()
    # goss = GOSS(1234, address=utils.get_gridappsd_address(),
    #                   username=utils.get_gridappsd_user(), password=utils.get_gridappsd_pass())
    goss.connect()

    # test_id = "1702722370"
    # sim_id = "847461010"
    # select * from expected_results where  match_flag=0 and difference_direction<>'NA'
    count_query = '{"query":"select COUNT(*) from expected_results where test_id=\'' + test_id + '\' and match_flag=0"}'
    response = goss.get_response(log_topic, count_query, timeout=10)
    test_1_count = response['data'][0]['COUNT(*)']
    print(test_1_count)
    print(test_1_count == '7') # 5?
    assert int(test_1_count) == 7, f" For expected_vs_running expecting 7 non matching results. Received {test_1_count}"
    query = '{"query":"select * from expected_results where test_id=\'' + test_id + '\' and match_flag=0"}'
    print(query)
    response = goss.get_response(log_topic, query, timeout=10)
    for i in response['data']:
        print(i)

    # exit(0) 1873688741

    sim_id2, test_id2 = request_test_running_vs_timeseries.start_test(sim_id)
    print('sent test request ' + test_id2)
    time.sleep(75)
    count_query = '{"query":"select COUNT(*) from expected_results where test_id=\'' + test_id2 + '\' and match_flag=0"}'
    response = goss.get_response(log_topic, count_query, timeout=10)
    print(response)
    test_2_count = response['data'][0]['COUNT(*)']
    print(test_2_count == '0')
    assert test_2_count == 0, f" For running_vs_timeseries expecting 0 non matching results. Received {test_2_count}"
    query = '{"query":"select * from expected_results where test_id=\'' + test_id2 + '\' and match_flag=0"}'
    print(query)
    response = goss.get_response(log_topic, query, timeout=10)
    for i in response['data']:
        print(i)

    with open('test_ids.json', 'w') as f:
        json.dump({'sim_id1': sim_id, 'sim_id2': sim_id2}, f)

if __name__ == '__main__':
    test_expected()
