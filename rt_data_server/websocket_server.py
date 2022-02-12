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

  continueGoing = True

  #on open of this socket
  def open(self):
    print ('Connection established.')
    #ioloop to wait for 3 seconds before starting to send data

  def on_message(self, message):
    jsonMessage = json.loads(message)
    print (jsonMessage)
    if jsonMessage.get('run') == 'true':
      startTime = time.time()
      ioloop.IOLoop.instance().add_timeout(datetime.timedelta(seconds=3), self.send_data(startTime))
    if jsonMessage.get('run') == 'false':
      global continueGoing
      continueGoing = False
      ioloop.IOLoop.instance().stop()
    

 #close connection
  def on_close(self):
    print ('Connection closed.')

  def check_origin(self, origin):
    return True

  
  # Our function to send new (random) data for charts
  def send_data(self, startTime):
    print ("Sending Data")

    #create a bunch of random data for various dimensions we want
    currentHeight = random.randrange(1, 5)

    #create a new data point
    point_data = {
    	'Time': (round((time.time() - startTime), 4)),
    	'Height' : currentHeight,
    }

    print (point_data)

    #write the json object to the socket
    self.write_message(json.dumps(point_data))

    time.sleep(1)

    #create new ioloop instance to intermittently publish data
    ioloop.IOLoop.instance().add_timeout(datetime.timedelta(seconds=1), self.send_data(startTime))

if __name__ == "__main__":
  #create new web app w/ websocket endpoint available at /websocket
  print ("Starting websocket server program. Awaiting client requests to open websocket ...")
  application = web.Application([(r'/static/(.*)', web.StaticFileHandler, {'path': os.path.dirname(__file__)}),
                                 (r'/websocket', WebSocketHandler)])
  application.listen(8001)
#TODO Fix ContinuGoing/ Start and Stop Buttons
  global continueGoing


  if (continueGoing):
    ioloop.IOLoop.instance().start()