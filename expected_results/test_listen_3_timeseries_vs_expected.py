import argparse
import json
import os
import time
import logging
import random
import pytest

from gridappsd import GridAPPSD, DifferenceBuilder, utils
from gridappsd.topics import simulation_input_topic, simulation_output_topic, simulation_log_topic, simulation_output_topic
import request_test_expected_vs_timeseries
test_output_topic = "/topic/goss.gridappsd.simulation.test.output."
# LOGGER = logging.getLogger(__name__)
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
            print(self._error_count == 7)  # 5?
            # assert self._error_count == 7, f" For expected_vs_timeseries expecting 7 non matching results. Received {self._error_count}"
            # os._exit(0)

# # finished=False
# error_count=0
#
# def on_message(headers, message):
#     """ Handle incoming messages on the simulation_output_topic for the simulation_id
#     Parameters
#     ----------
#     headers: dict
#         A dictionary of headers that could be used to determine topic of origin and
#         other attributes.
#     message: object
#         A data structure following the protocol defined in the message structure
#         of ``GridAPPSD``.  Most message payloads will be serialized dictionaries, but that is
#         not a requirement.
#     """
#     print(headers["destination"])
#     print(message)
#     global error_count
#     # global error_count
#     # global finished
#     logging.info("On message")
#     if 'status' in message and (message['status'] == 'finish' or message['status'] == 'start'):
#         pass
#     else:
#         error_count+=1
#     # json_message = json.loads(message)
#     # "{\"status\":\"start\"}")
#     if 'status' in message and message['status'] == 'finish':
#         print("Exit")
#         print("Error count " + str(error_count))
#         logging.info("on_message error count " + str(error_count))
#         print(error_count == 7)
#         # finished = True
#         # os._exit(0)

def test():

    # parser = argparse.ArgumentParser()
    # parser.add_argument("-test_id", default=3258685887,
    #                     help="Simulation id to use for responses on the message bus.")
    # opts = parser.parse_args()
    # gapps = GridAPPSD(opts.test_id, address=utils.get_gridappsd_address(),
    #                   username=utils.get_gridappsd_user(), password=utils.get_gridappsd_pass())

    gapps = GridAPPSD()
    gapps.connect()
    logging.info('Starting')
    sl = SimpleListener(gapps, 1)

    with open('test_id_request_1.json') as f:
        sim_id = json.load(f)
    sim_id = sim_id['sim_id1']

    test_id2 = request_test_expected_vs_timeseries.start_test(sim_id)

    response = gapps.subscribe(test_output_topic + str(test_id2), sl)
    print(response)
    print(type(test_id2))
    print('simid ' + str(sim_id))
    print('sent test request ' + str(test_id2))
    print(test_output_topic + str(test_id2))

    # response = gapps.subscribe(test_output_topic+str(test_id2), on_message)
    # print(response)

    # while True:
    #     time.sleep(0.1)
    # time.sleep(2)
    logging.info("Start waiting")
    finished = False
    while not finished:
        time.sleep(3)
        finished = True
    error_count = sl._error_count
    print(error_count)
    logging.info("Error count " + str(error_count))
    assert error_count == 7, f" For expected_vs_timeseries expecting 7 non matching results. Received {error_count}"

if __name__ == "__main__":
    test()
