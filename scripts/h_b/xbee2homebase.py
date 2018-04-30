## /boot/config.txt needs to have the setting for the device
## tree overlay pi3-disable-bt
## Also configure the UART to be OFF (i.e. not to be used as a
## serial console
## dtoverlay=pi3-disable-bt ( pi3-miniuart-bt could also be a possibility )


import serial
import time
import datetime
import json
from xbee import XBee, DigiMesh, ZigBee

ser = serial.Serial('/dev/ttyS0', baudrate=9600)
##ser = serial.Serial('/dev/ttyAMA0', baudrate=9600)
##ser = serial.Serial('/dev/ttyUSB0', baudrate=9600)
print(ser.name)


def print_data( data ):
    msg = str(data["rf_data"])
    dStart = msg.find('{')
    dEnd = msg.rfind('}')+ 1
    data = json.loads('[' + msg[dStart:dEnd] + ']')
    localtime = time.asctime( time.localtime(time.time()) )
    print( "Recevied: " + str(json.dumps(data)))

    ## This is a JSON telegram.
    ## 1. Assert the field device
    ## 2. Build the JSON object to send to the server.
    ##    From the telegram, we also need the sender and this needs
    ##    to be populated in the object to create the log entry.
    ##
    ##    The address of the device should be captured in the model so that
    ##    we can use this for the prompting of data and the locate the device
    ##    again.

xbee = ZigBee(ser=ser, escaped=True, callback=print_data)
digi = DigiMesh(ser=ser)

while True:
    try:
        print("Requesting data - " + str(datetime.datetime.now()) )
        digi.tx(frame_id = b'\x01', dest_addr=b'\x00\x13\xA2\x00\x41\x5C\x0F\x64', data=b'D' )
        ## Request new data every five minutes.
        time.sleep(5 * 60)
    except KeyboardInterrupt:
        break

xbee.halt()
ser.close()


