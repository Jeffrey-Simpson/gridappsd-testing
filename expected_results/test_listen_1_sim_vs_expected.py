import argparse
import json
import os
import time

from gridappsd import GridAPPSD, DifferenceBuilder, utils
from gridappsd.topics import simulation_input_topic, simulation_output_topic, simulation_log_topic, simulation_output_topic
import request_test_expected_vs_running
test_output_topic = "/topic/goss.gridappsd.simulation.test.output."

class SimpleListener(object):
    """ A simple class to listen for the test results
    """

    def __init__(self, gridappsd_obj, test_id):
        """ Create
        """
        self._gapps = gridappsd_obj
        self._test_id = test_id

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

        # json_message = json.loads(message)
        # "{\"status\":\"start\"}")
        if 'status' in message and message['status'] == 'finish':
            print("Exit")
            os._exit(1)


def _main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-test_id", default=3258685887,
                        help="Simulation id to use for responses on the message bus.")

    opts = parser.parse_args()
    sim_id, test_id = request_test_expected_vs_running.start_test()
    print('sent test request ' + test_id)

    gapps = GridAPPSD(opts.test_id, address=utils.get_gridappsd_address(),
                      username=utils.get_gridappsd_user(), password=utils.get_gridappsd_pass())
    sl = SimpleListener(gapps, opts.test_id)
    print(test_output_topic+str(test_id))
    response = gapps.subscribe(test_output_topic+str(test_id), sl)
    print(response)

    with open('test_id_request_1.json', 'w') as f:
        json.dump({'sim_id1': sim_id}, f)

    while True:
        time.sleep(0.1)


if __name__ == "__main__":
    _main()

