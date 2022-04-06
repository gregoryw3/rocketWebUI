import datetime
import json
import os
import random
import socket
import time
from abc import ABC
from glob import glob
from multiprocessing import Pipe, Process, Queue

from tornado import ioloop, web, websocket

host = "127.0.0.1"
port = 55021


def open_socket():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err:
        print("socket creation failed, for why?")
    s.bind(host, port)
    return s


class WebSocketHandler(websocket.WebSocketHandler, ABC):
    # Addition for Tornado as of 2017, need the following method
    # per: http://stackoverflow.com/questions/24851207/tornado-403-get-warning-when-opening-websocket/25071488#25071488
    def check_origin(self, origin):
        return True

    # on open of this socket
    def open(self):
        print('Connection established.')
        # ioloop to wait for 3 seconds before starting to send data

    def on_message(self, message):
        json_message = json.loads(message)
        print(json_message)
        web_message = json_message.get('run')
        start_time = time.time()
        past_height = 0
        if web_message:
            ioloop.IOLoop.instance().add_timeout(datetime.timedelta(seconds=3),
                                                 self.send_data(start_time, past_height, web_message))
        else:
            ioloop.IOLoop.instance().stop()

    # close connection
    def on_close(self):
        print('Connection closed.')

    def check_origin(self, origin):
        return True

    # Our function to send new (random) data for charts
    def send_data(self, start_time, past_height, web_message):
        print("Sending Data")

        # create a bunch of random data for various dimensions we want
        currentHeight = random.randrange(1, 300)

        # create a new data point
        point_data = {
            'Time': (round((time.time() - start_time), 4)),
            'Height': currentHeight + past_height,
            'AirPressure': random.randrange(1, 100),
            'Humidity': random.randrange(1, 100),
            'Temperature': random.randrange(1, 100),
        }

        past_height = currentHeight + past_height

        print(point_data)

        # write the json object to the socket
        if web_message:
            self.write_message(json.dumps(point_data))

        time.sleep(1)

        # create new ioloop instance to intermittently publish data
        ioloop.IOLoop.instance().add_timeout(datetime.timedelta(seconds=1),
                                             self.send_data(start_time, past_height, web_message))


def main():
    print("Starting websocket server program. Awaiting client requests to open websocket ...")
    application = web.Application([(r'/static/(.*)', web.StaticFileHandler, {'path': os.path.dirname(__file__)}),
                                   (r'/websocket', WebSocketHandler)])
    application.listen(8001)
    ioloop.IOLoop.instance().start()
    open_socket()


if __name__ == "__main__":
    main()
