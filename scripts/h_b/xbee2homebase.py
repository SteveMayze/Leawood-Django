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

import requests


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

url = 'http://leawood:8000/leawood/api/v1/field_device'
headers = {'Authorization':'ApiKey admin:40a7590dd47da3443b7fff6dbcdcdfafee5446b8'}

all_devices = requests.get(url, headers=headers).json()['objects']

while True:
    try:
        for device in all_devices:
            address = device['serial_id']
            print("{0} - Requesting data from {1}".format(datetime.datetime.now(), address))
            ### Python3
            ## digi.tx(frame_id = b'\x01', dest_addr=bytes.fromhex(address), data=b'D')
            digi.tx(frame_id = b'\x01', dest_addr=address.decode('hex'), data=b'D')
        ## Request new data every five minutes.
        time.sleep(5 * 60)
    except KeyboardInterrupt:
        break
# http://Tqbfj07ld
xbee.halt()
ser.close()


