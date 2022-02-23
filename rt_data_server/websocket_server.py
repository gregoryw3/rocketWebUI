from glob import glob
import time
import random
import json
import datetime
import os
from tornado import websocket, web, ioloop
from datetime import timedelta
from random import randint

import tornado

class WebSocketHandler(websocket.WebSocketHandler):
  # Addition for Tornado as of 2017, need the following method
  # per: http://stackoverflow.com/questions/24851207/tornado-403-get-warning-when-opening-websocket/25071488#25071488
  def check_origin(self, origin):
    return True
  #on open of this socket
  def open(self):
    print ('Connection established.')
    #ioloop to wait for 3 seconds before starting to send data

  def on_message(self, message):
    jsonMessage = json.loads(message)
    print (jsonMessage)
    webMessage = jsonMessage.get('run')
    startTime = time.time()
    pastHeight = 0
    ioloop.IOLoop.instance().add_timeout(datetime.timedelta(seconds=3), self.send_data(startTime, pastHeight, webMessage))
    

 #close connection
  def on_close(self):
    print ('Connection closed.')

  def check_origin(self, origin):
    return True

  
  # Our function to send new (random) data for charts
  def send_data(self, startTime, pastHeight, webMessage):
    print ("Sending Data")

    #create a bunch of random data for various dimensions we want
    currentHeight = random.randrange(1, 300)

    #create a new data point
    point_data = {
    	'Time': (round((time.time() - startTime), 4)),
    	'Height' : currentHeight + pastHeight,
      'AirPressure' : random.randrange(1, 100),
      'Humidity' : random.randrange(1, 100),
      'Temperature' : random.randrange(1, 100),
    }

    pastHeight = currentHeight + pastHeight

    print (point_data)

    #write the json object to the socket
    if (webMessage):
      self.write_message(json.dumps(point_data))

    time.sleep(1)

    #create new ioloop instance to intermittently publish data
    ioloop.IOLoop.instance().add_timeout(datetime.timedelta(seconds=1), self.send_data(startTime, pastHeight, webMessage))

if __name__ == "__main__":
  #create new web app w/ websocket endpoint available at /websocket
  print ("Starting websocket server program. Awaiting client requests to open websocket ...")
  application = web.Application([(r'/static/(.*)', web.StaticFileHandler, {'path': os.path.dirname(__file__)}),
                                 (r'/websocket', WebSocketHandler)])
  application.listen(8001)
  ioloop.IOLoop.instance().start()