from digi.xbee.devices import XBeeDevice
import time
import socket
import serial

# standard local host
host = "127.0.0.1"
# doesn't really matter as long as its not in use by another program and > 1023
port = 55021

comm_port = "COM6"
baudrate = 57600


def open_socket():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err:
        print("socket creation failed, for why?")
    s.bind(host, port)
    return s


def send(data, s):
    s.send(data)


def main():
    device = serial.Serial(port="COM6", baudrate=baudrate, parity=serial.PARITY_EVEN)
    sock = open_socket()
    data = b''
    while True:
        if device.inWaiting() > 0:
            data = device.read(size=device.inWaiting())
        print(data)
        print('post data')
        send(data, sock)


if __name__ == "__main__":
    main()