import datetime
import json
import os
import random
import socket
import time

from tornado import ioloop, web, websocket

host = socket.gethostname()
port = 55021

global count 
count = 0

try:
    s = socket.socket()
except socket.error as err:
    print("socket creation failed, for why?")
s.bind((host, port))
s.listen(1)
cli_sock, address= s.accept()


print("yes")
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
                                                 self.send_data(start_time, web_message))
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
        #dont need this anymore
        radio_message = cli_sock.recv(1024)
        radio_message = parse_radio(radio_message)
        
        print(radio_message)
        web_message=radio_message
        # write the json object to the socket
        if web_message:
            self.write_message(json.dumps(radio_message))

        time.sleep(1)

        # create new ioloop instance to intermittently publish data
        ioloop.IOLoop.instance().add_timeout(datetime.timedelta(seconds=1),
                                             self.send_data(start_time, web_message))


def parse_radio(radio_message):
    global count
    data = radio_message.decode('utf-8')
    data = data.split(',')
    #sort of spaghetti? kind of not really, but parsing the data recieved from the receiver
    pressure = int(data[0])
    altitude = int(data[1])
    humidity = int(data[2])
    temperature = int(data[3])
    latitude = int(data[4])
    longitude = int(data[5])
    gps_time = float(data[6])

    #count variable a place holder that may stay forever
    point_data = {
        'Time': count,
        'Height': altitude,
        'AirPressure': pressure,
        'Humidity': humidity,
        'Temperature': temperature,
        'Latitude': latitude,
        'Longitude': longitude
    }
    count += 1
    return point_data


def main():
    global count
    print("Starting websocket server program. Awaiting client requests to open websocket ...")
    application = web.Application([(r'/static/(.*)', web.StaticFileHandler, {'path': os.path.dirname(__file__)}),
                                   (r'/websocket', WebSocketHandler)])
    application.listen(8001)
    ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
