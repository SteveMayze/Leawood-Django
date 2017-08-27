

## /boot/config.txt needs to have the setting for the device
## tree overlay pi3-disable-bt
## Also configure the UART to be OFF (i.e. not to be used as a
## serial console
## dtoverlay=pi3-disable-bt ( pi3-miniuart-bt could also be a possibility )


import serial
import time
from xbee import XBee, DigiMesh, ZigBee

ser = serial.Serial('/dev/ttyAMA0', baudrate=9600)
##ser = serial.Serial('/dev/ttyUSB0', baudrate=9600)
print(ser.name)

def print_data( data ):
    msg = str(data["rf_data"])
    print("{0}".format(msg));


xbee = ZigBee(ser=ser, escaped=True, callback=print_data)

while True:
    try:
        ## print(xbee.wait_read_frame())
        time.sleep(1)
    except KeyboardInterrupt:
        break

xbee.halt()
ser.close()

