import datetime
import json
import os
import random
import socket
import time

from tornado import ioloop, web, websocket

host = "127.0.0.1"
port = 55021

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as err:
    print("socket creation failed, for why?")
    s.bind(host, port)


class WebSocketHandler(websocket.WebSocketHandler):
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
    def send_data(self, start_time, web_message):
        print("Sending Data")

        # create a bunch of random data for various dimensions we want
        current_height = random.randrange(1, 300)

        radio_message = s.recv()
        radio_message = parse_radio(radio_message)

        print(radio_message)

        # write the json object to the socket
        if web_message:
            self.write_message(json.dumps(radio_message))

        time.sleep(1)

        # create new ioloop instance to intermittently publish data
        ioloop.IOLoop.instance().add_timeout(datetime.timedelta(seconds=1),
                                             self.send_data(start_time, web_message))


def parse_radio(radio_message):
    data = radio_message.decode('utf-8')
    data = data.split(';')
    pr_alt_data = data[0].split(',')
    t_h_data = data[1].split(',')
    lat_long__time_data = data[2].split(',')

    pressure = int(pr_alt_data[0])
    altitude = int(pr_alt_data[1])
    humidity = int(t_h_data[1])
    temperature = int(t_h_data[0])
    latitude = int(lat_long__time_data[0])
    longitude = int(lat_long__time_data[1])
    gps_time = float(lat_long__time_data[2])

    point_data = {
        'Time': gps_time,
        'Height': altitude,
        'AirPressure': pressure,
        'Humidity': humidity,
        'Temperature': temperature,
        'latitude': latitude,
        'longitude': longitude
    }

    return point_data


def main():
    print("Starting websocket server program. Awaiting client requests to open websocket ...")
    application = web.Application([(r'/static/(.*)', web.StaticFileHandler, {'path': os.path.dirname(__file__)}),
                                   (r'/websocket', WebSocketHandler)])
    application.listen(8001)
    ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
