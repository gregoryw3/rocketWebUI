from digi.xbee.devices import XBeeDevice

# The client is our groundstation laptop
#
# Remember to replace the COM port with the one your sender XBee device is connected to. 
# In UNIX-based systems, the port usually starts with /dev/tty.
#
# Instantiate a local XBee object.
# Port and Baud Rate
xbee = XBeeDevice("/dev/tty.usbserial-DA01HY9O", 57600)

# The default timeout to wait for the send status is two seconds. However, you can configure the timeout using the
# get_sync_ops_timeout() and set_sync_ops_timeout() methods of an XBee class.
xbee.open()


# Define callback.
def my_data_received_callback(xbee_message):
    address = xbee_message.remote_device.get_64bit_addr()
    data = xbee_message.data.decode("utf8")
    send_to_web("Received data from %s: %s" % (address, data))


def send_to_web(child_conn, message):
    child_conn.send(message)
    child_conn.close()


# Add the callback.
xbee.add_data_received_callback(my_data_received_callback)
# This mechanism for reading data does not block your application. Instead, you can be notified when new data has
# been received if you are subscribed or registered to the data reception service using the
# add_data_received_callback() method with a data reception callback as parameter.
#
# To stop listening to new received data, use the del_data_received_callback() method 
# to unsubscribe the already-registered callback.


# Closes the xbee connection
xbee.close()
