import socket
import serial
#standard local host
host = socket.gethostname()
#doesn't really matter as long as its not in use by another program and > 1023
port = 55021

baudrate = 57600
#creating and conencting to the socket to send to the web front end
try:
    s = socket.socket()
except socket.error as err:
    print("socket creation failed, for why?")
s.connect((host,port))    

def main():
    #initializing the radio port
    device = serial.Serial(port="COM6",baudrate=baudrate,parity=serial.PARITY_EVEN)

    data = b''
    c = b''
    while True:
        #waiting to do anything until there's something in the input buffer
        if device.inWaiting()> 0:
            data = device.read(size=device.inWaiting()).strip()
            #lol spaghetti code to ensure that I send a correct packet of data to the ui
            #id make it not spaghetti if I started earlier...
            c = data
            c.decode('utf-8')
            l = c.split(b',')
            #add check for gps in the the data receiver 
            for i in range(0,len(l)):
                if(l[i] == b''):
                    l[i] = b'0'
            print(l)
            
            #lol more spaghetti
            if len(l) == 4:
                data = b','.join(l)
                print(data)
                #sending data to the ui
                s.send(data)
        #resetting the data value
        data = b''
            
if __name__ == "__main__":
    main()