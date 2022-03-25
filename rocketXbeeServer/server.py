from digi.xbee.devices import XBeeDevice
from digi.xbee.devices import ZigBeeDevice

# The server is the raspberry pi on the rocket
#
# Remember to replace the COM port with the one your sender XBee device is connected to. 
# In UNIX-based systems, the port usually starts with /dev/tty.

#Port and Baude Rate
xbee = ZigBeeDevice("/dev/ttyAMA0", 9600)

currentData = 0

try:
    xbee.open()
finally:
    print("Xbee failed to Connect")
    xbee.close()

def main():
        xbee.send_expl_data_async(xbee, currentData)


if __name__ == '__main__':
    main()