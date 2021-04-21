import argparse
import json
import os
import time
import logging

from gridappsd import GridAPPSD, DifferenceBuilder, utils
from gridappsd.topics import simulation_input_topic, simulation_output_topic, simulation_log_topic, simulation_output_topic
import request_test_running_vs_timeseries
test_output_topic = "/topic/goss.gridappsd.simulation.test.output."
logging.basicConfig(filename=__name__+'.log', level=logging.INFO)

class SimpleListener(object):
    """ A simple class to listen for the test results
    """

    def __init__(self, gridappsd_obj, test_id):
        """ Create
        """
        self._gapps = gridappsd_obj
        self._test_id = test_id
        self._error_count = 0

    def on_message(self, headers, message):
        """ Handle incoming messages on the simulation_output_topic for the simulation_id
        Parameters
        ----------
        headers: dict
            A dictionary of headers that could be used to determine topic of origin and
            other attributes.
        message: object
            A data structure following the protocol defined in the message structure
            of ``GridAPPSD``.  Most message payloads will be serialized dictionaries, but that is
            not a requirement.
        """
        print(message)
        if 'status' in message and (message['status'] == 'finish' or message['status'] == 'start'):
            pass
        else:
            self._error_count+=1
        # json_message = json.loads(message)
        # "{\"status\":\"start\"}")
        if 'status' in message and message['status'] == 'finish':
            print("Exit")
            print("Error count " + str(self._error_count))
            print(self._error_count == 0)
            # assert self._error_count != 0, f" For running_vs_timeseries expecting 0 non matching results. Received {self._error_count}"
            #
            # os._exit(1)



def test():
    # parser = argparse.ArgumentParser()
    # parser.add_argument("-test_id", default=3258685887,
    #                     help="Simulation id to use for responses on the message bus.")
    #
    # opts = parser.parse_args()

    with open('test_id_request_1.json') as f:
        sim_id = json.load(f)
    sim_id = sim_id['sim_id1']
    # sim_id = 877159920
    sim_id2, test_id2 = request_test_running_vs_timeseries.start_test(sim_id)
    print('simid ' + sim_id2)
    print('sent test request ' + test_id2)

    # gapps = GridAPPSD(opts.test_id, address=utils.get_gridappsd_address(),
                      # username=utils.get_gridappsd_user(), password=utils.get_gridappsd_pass())
    gapps = GridAPPSD()
    gapps.connect()
    sl = SimpleListener(gapps, 1)
    print(test_output_topic+str(test_id2))
    response = gapps.subscribe(test_output_topic+str(test_id2), sl)
    print('response')
    print(response)

    with open('test_id_request_2.json', 'w') as f:
        json.dump({'sim_id2': sim_id2}, f)

    finished = False
    while not finished:
        time.sleep(65)
        finished = True
    error_count = sl._error_count
    print(error_count)
    logging.info("Error count " + str(error_count))
    assert error_count == 0, f" For running_vs_timeseries expecting 0 non matching results. Received {error_count}"


if __name__ == "__main__":
    test()

