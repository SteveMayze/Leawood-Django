import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Leawood.settings')
cwd = os.getcwd()
sys.path.append(cwd)
import django

django.setup()
from main.models import Field_Device, Unit, Data_Log_Entry

def populate():
    si_units = [{"name": "volt","symbol": "V","measure": "voltage"},
        {"name": "degrees Celcius","symbol": "°C","measure": "temperature"}]

    field_devices = [
        {
            "name": "Remote device 1",
            "description": "Test device ",
            "address": "0001",
        }
        ]


    Unit.objects.all().delete()
    Field_Device.objects.all().delete()
    
    for unit in si_units:
        print("Adding Unit " + str(unit))
        add_unit(unit['name'], unit['symbol'], unit['measure'])

    for device in field_devices:
        print("Adding Device " + str(device))
        add_device( device['name'], device['description'], device['address'] )


def add_unit( name, symbol, measure ):
    entity = Unit.objects.get_or_create(name=name, symbol=symbol, measure=measure)[0]
    entity.save()
    print(">> " + str(entity))
    return entity

def add_device( name, description, address ):
    entity = Field_Device.objects.get_or_create(name=name)[0]
    entity.description = description
    entity.address = address
    entity.save()
    print(">> " + str(entity))
    return entity


if __name__ == '__main__':
    print("Starting the Leawood population script...")
    populate()

    

    
