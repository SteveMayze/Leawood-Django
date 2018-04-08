
##
## xbee2db.py
##
## A service utility script to populate the database
## from the information recevied through the XBEE.
##
import serial
import time
import json
from xbee import XBee, DigiMesh, ZigBee

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Leawood.settings')
import django
django.setup()


## TODO - Consider some type of configuration script
##        to hold the Serial connection details and
##        even the database connection.

ser = serial.Serial('/dev/ttyS0', baudrate=9600)

print(ser.name)


def print_data( data ):

    ## A case type costruct is requried on Data to determine
    ## the type of message. The data structure should be queried
    ## for the MAC address of the sender. This can be a pseudo
    ## serial number (does this hold true for routed messages?).
    ##
    ## Request to Learn - Register a new device
    ##    This is quite complex at the moment as the server needs
    ##    to acknowlege the request and ask the device for its
    ##    features. The response should be a list of metadata that
    ##    the device will later send. I.e. what key-value pairs are
    ##    to be expected later.
    ##
    ## Data Send (answer to a data request).
    ##
    ## Event - Asynchronous message from the field.
    
    msg = str(data["rf_data"])
    dStart = msg.find('{')
    dEnd = msg.rfind('}')+ 1
    data = json.loads('[' + msg[dStart:dEnd] + ']')
    localtime = time.asctime( time.localtime(time.time()) )
    print( "Recevied: " + str(json.dumps(data)) )

xbee = ZigBee(ser=ser, escaped=True, callback=print_data)

while True:
    try:
        time.sleep(10)
    except KeyboardInterrupt:
        break

xbee.halt()
ser.close()


