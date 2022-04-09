import socket
import time

# standard local host
host = socket.gethostname()
# doesn't really matter as long as it's not in use by another program and > 1023
port = 55021

baudrate = 57600
# creating and connecting to the socket to send to the web front end
try:
    s = socket.socket()
except socket.error as err:
    print("socket creation failed, for why?")
s.connect((host, port))


def main():
    data = b''
    list_data = [0, 0, 0, 0, -90, -180, 1.909090]
    while True:
        # data = b','.join(data)
        for i in range(0, len(list_data)):
            if i != 6:
                list_data[i] += 1
            else:
                list_data[6] += 1.3898
            if list_data[4] >= 90:
                list_data[4] = -90
            if list_data[5] >= 180:
                list_data[5] = -180
            
        for i in range(0, len(list_data)):
            if i < (len(list_data) - 1):
                data += (bytes(str(int(list_data[i])), 'utf-8') + bytes(',', 'utf-8'))
            else:
                data += (bytes(str(int(list_data[i])), 'utf-8'))
        print(data)
        s.send(data)
        data = b''
        time.sleep(1)


if __name__ == "__main__":
    main()
