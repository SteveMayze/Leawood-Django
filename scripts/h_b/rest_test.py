
import requests
import json

url = 'http://leawood:8000/leawood/api/v1/field_device'
headers = {'Authorization':'ApiKey admin:40a7590dd47da3443b7fff6dbcdcdfafee5446b8'}


r = requests.get(url, headers=headers)
devices = r.json()['objects']

for device in devices:
    serial = device['serial_id']
    print ('XBEE Address -> ' + serial)
    
    
