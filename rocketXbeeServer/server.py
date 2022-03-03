from digi.xbee.devices import XBeeDevice

# The server is the raspberry pi on the rocket
#
# Remember to replace the COM port with the one your sender XBee device is connected to. 
# In UNIX-based systems, the port usually starts with /dev/tty.
device = XBeeDevice("COM1", 9600)
device.open()
device.send_data_broadcast("Hello XBee World!")
device.close()