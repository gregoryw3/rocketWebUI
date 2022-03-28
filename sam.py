import time
import board
from board import *
import adafruit_bmp3xx
import adafruit_sht31d
import adafruit_gps
from digi.xbee.devices import XBeeDevice

#i2c = busio.I2C(board.SCL, board.SDA)
def altimeter_barometer(bmp):
    pressure = bmp.pressure
    altitude = bmp.altitude
    return (pressure, altitude) 
    
def gps_func(gps):
    return (gps.latitude, gps.longitude)

def temp_humidity(sensor):
    return (sensor.relative_humidity, sensor.temperature)

def main():
    i2c = board.I2C()
   # gps = adafruit_gps.GPS_GtopI2C(i2c,debug=False)
   # gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
   # gps.send_command(b"PMTK220,1000")
    radio =  XBeeDevice("/dev/ttyAMA0",57600)
    data = bytearray()
    bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)
    #sht = adafruit_sht31d.SHT31D(i2c)
    while True:
        data.clear()
        alt_pres = altimeter_barometer(bmp)
        temp_hum_data = temp_humidity(sht)
        gps_d = gps_func()
        t_h = temp_humidity()
        data.add(bytes(alt_pres[0]))
        data.add(bytes(alt_pres[1]))
        """
        data.add(bytes(gps_d[0]))
        data.add(bytes(gps_d[1]))
        data.add(bytes(temp_hum_data[0]))
        data.add(bytes(temp_hum_data[1]))
        """
        #send data to socket program with radio script
        radio.send_data_broadcast(data)
        time.sleep(1)

if __name__ == "__main__":
    main()