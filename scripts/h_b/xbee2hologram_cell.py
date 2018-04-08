
## /boot/config.txt needs to have the setting for the device
## tree overlay pi3-disable-bt
## Also configure the UART to be OFF (i.e. not to be used as a
## serial console
## dtoverlay=pi3-disable-bt ( pi3-miniuart-bt could also be a possibility )

import serial
import time
import json
from xbee import XBee, DigiMesh, ZigBee
from Hologram.HologramCloud import HologramCloud

hologram = HologramCloud(dict(), network='cellular')


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
    # print(str("SENDING: {0}, ID:{1}, {2} V,  {3}"+ chr(176)+"C").format(localtime, data[0]['id'], data[0]['voltage'], data[0]['temperature']))
    print( "SENDING: " + str(json.dumps(data)) )
    response = hologram.sendMessage(json.dumps(data), topics=["leawood/sensors/fence1"])
    print( "RESPONSE: " + response )


xbee = ZigBee(ser=ser, escaped=True, callback=print_data)

while True:
    try:
        ## print(xbee.wait_read_frame())
        time.sleep(1)
    except KeyboardInterrupt:
        break

xbee.halt()
ser.close()


