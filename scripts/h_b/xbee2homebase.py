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

## Defining some variables that are used by the REST connection
## TODO These should be configurable.
baseurl = 'http://leawood:8000/leawood/api/v1'
field_device_prefix = "/leawood/api/v1/field_device/{0}/"
param_prefix = "/leawood/api/v1/metadata/{0}/"
headers = {'Authorization':'ApiKey admin:40a7590dd47da3443b7fff6dbcdcdfafee5446b8'}


def persist_data( data ):
    print("BEGIN {0}".format(data))
    msg = str(data["rf_data"])
    addr = data["source_addr_long"]
    dStart = msg.find('{')
    dEnd = msg.rfind('}')+ 1
    data = json.loads( msg[dStart:dEnd] )
    log_time = datetime.datetime.now()
    print( "Recevied: {source_addr: "+str(addr.hex())+" data: "+str(json.dumps(data)))
    
    url = baseurl + '/field_device?address={0}'.format(addr.hex().upper())
    device_id = requests.get(url, headers=headers).json()['objects'][0]['id']

    url = baseurl + '/metadata?field_device={0}'.format(device_id)
    all_metadata = requests.get(url, headers=headers).json()['objects']

    data_value = ""
    for metadata in all_metadata:
        ## The metadata schema needs a key type column that will come from the
        ## field device so that the metadata row can be located.
        ## At the moment, I have to hard code this.
        meta_name = metadata['name']
        print("Prcessing param {0}".format(meta_name))
        if meta_name == 'temperature':
            ## Process for temperature
            data_value = data['temp']

        if meta_name == 'battery':
            ## Process for battery voltage
            data_value = data['voltage']

        if meta_name == 'backup_battery':
            ## Process for the backup battery
            data_value = data['batt']

        payload = {}
        payload['field_device'] = field_device_prefix.format(device_id)
        payload['param_metadata'] = param_prefix.format(metadata['id'])
        payload['time_stamp'] = log_time.isoformat()
        payload['value'] = data_value

        print("Logging {0}".format(payload))

        url= baseurl+'/log_entry/'
        response = requests.post(url, headers=headers, json=payload)
        print("Response {0}".format(response.status_code))

        ## Handler needed to interpet the responses etc.

    print("END")

#######################################################################
## Scrip Start
#######################################################################
    
xbee = ZigBee(ser=ser, escaped=True, callback=persist_data)
digi = DigiMesh(ser=ser)

url = baseurl + '/field_device'

all_devices = requests.get(url, headers=headers).json()['objects']

while True:
    try:
        for device in all_devices:
            address = device['serial_id']
            print("{0} - Requesting data from {1}".format(datetime.datetime.now(), address))
            digi.tx(frame_id = b'\x01', dest_addr=bytes.fromhex(address), data=b'D')
            ## digi.tx(frame_id = b'\x01', dest_addr=address.decode('hex'), data=b'D')
        ## Request new data every five minutes.
        time.sleep(5 * 60)
    except KeyboardInterrupt:
        break
# http://Tqbfj07ld
xbee.halt()
ser.close()


