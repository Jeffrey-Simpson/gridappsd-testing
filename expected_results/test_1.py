import time
from gridappsd import GOSS
import request_test_expected_vs_timeseries
import request_test_expected_vs_running

def test_expected():
    sim_id, test_id = request_test_expected_vs_running.start_test()
    time.sleep(75)
    print('sent test request')
    log_topic = 'goss.gridappsd.process.request.data.log'
    goss = GOSS()
    goss.connect()
    query = '{"query":"select * from expected_results"}'
    test_id = "1702722370"
    sim_id = "847461010"
    # select * from expected_results where  match_flag=0 and difference_direction<>'NA'
    count_query = '{"query":"select COUNT(*) from expected_results where test_id=\'' + test_id + '\' and match_flag=0"}'
    response = goss.get_response(log_topic, count_query, timeout=10)
    print(response['data'][0]['COUNT(*)'] == '5')
    query = '{"query":"select * from expected_results where test_id=\'' + test_id + '\' and match_flag=0"}'
    response = goss.get_response(log_topic, query, timeout=10)
    for i in response['data']:
        print(i)
    test_id = request_test_expected_vs_timeseries.start_test(sim_id)
    time.sleep(2)
    count_query = '{"query":"select COUNT(*) from expected_results where test_id=\'' + test_id + '\' and match_flag=0"}'
    response = goss.get_response(log_topic, count_query, timeout=10)
    print(response)
    print(response['data'][0]['COUNT(*)'] == '5')
    query = '{"query":"select * from expected_results where test_id=\'' + test_id + '\' and match_flag=0"}'
    response = goss.get_response(log_topic, query, timeout=10)
    for i in response['data']:
        print(i)


if __name__ == '__main__':
    test_expected()
