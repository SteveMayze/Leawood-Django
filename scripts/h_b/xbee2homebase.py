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

baseurl = 'http://leawood:8000/leawood/api/v1'
headers = {'Authorization':'ApiKey admin:40a7590dd47da3443b7fff6dbcdcdfafee5446b8'}


def persist_data( data ):
    print("BEGIN {0}".format(data))
    msg = str(data["rf_data"])
    addr = data["source_addr_long"]
    dStart = msg.find('{')
    dEnd = msg.rfind('}')+ 1
    data = json.loads( msg[dStart:dEnd] )
    localtime = time.asctime( time.localtime(time.time()) )
    ## print( "Recevied: {source_addr: {0}, data: {1}".format(addr, json.dumps(data)))
    print( "Recevied: {source_addr: "+str(addr.hex())+" data: "+str(json.dumps(data)))
    
    ## This is a JSON telegram.
    ## 1. Assert the field device
    ## print("Getting the field device details")

    url = baseurl + '/field_device?address={0}'.format(addr.hex().upper())
    device_id = requests.get(url, headers=headers).json()['objects'][0]['id']
    ## print("Device ID {0} "+str(device_id))


##    ## Temperature
##    url = "http://leawood:8000/leawood/api/v1/metadata?field_device={0}&name=temperature".format(device_id)
##    headers = {'Authorization':'ApiKey admin:40a7590dd47da3443b7fff6dbcdcdfafee5446b8'}
##    temp_id = requests.get(url, headers=headers).json()['objects'][0]['id']
##    print("Temperature ID {0}".format(temp_id))
##
##    ## Temperature
##    url = "http://leawood:8000/leawood/api/v1/metadata?field_device={0}&name=temperature".format(device_id)
##    headers = {'Authorization':'ApiKey admin:40a7590dd47da3443b7fff6dbcdcdfafee5446b8'}
##    temp_id = requests.get(url, headers=headers).json()['objects'][0]['id']
##    print("Temperature ID {0}".format(temp_id))

    url = baseurl + '/metadata?field_device={0}'.format(device_id)
    ## print("Getting the parameter details from {0}".format(url))
    all_metadata = requests.get(url, headers=headers).json()['objects']

    ## print("All metadata {0}".format(all_metadata))

    ## print("RAW JSON={0}".format(data))

    for metadata in all_metadata:
        ## The metadata schema needs a key type column that will come from the
        ## field device so that the metadata row can be located.
        meta_name = metadata['name']
        ## print("Prcessing param {0}".format(meta_name))
        if meta_name == 'temperature':
            ## Process for temperature
            temp = data['temp']
            print("The temperature is {0} C".format(temp))

            url= baseurl+'log_entry'
            

        if meta_name == 'battery':
            ## Process for battery voltage
            voltage = data['voltage']
            print("The battery voltage is {0} V".format(voltage))

        if meta_name == 'backup_battery':
            ## Process for the backup battery
            backup_battery = data['batt']
            print("The backup battery voltage is {0} V".format(backup_battery))

        ## We now have basically all the information
        ## LOG ENTRY
            ## name
            ## field_device
            ## metadata
            ## time_stamp
            ## value
    
    
    print("END")

    
    
    
    ## 2. Build the JSON object to send to the server.
    ##    From the telegram, we also need the sender and this needs
    ##    to be populated in the object to create the log entry.
    ##
    ##    The address of the device should be captured in the model so that
    ##    we can use this for the prompting of data and the locate the device
    ##    again.

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


