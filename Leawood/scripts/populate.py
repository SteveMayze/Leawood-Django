import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Leawood.settings')
cwd = os.getcwd()
sys.path.append(cwd)
import django

django.setup()
from main.models import Field_Device, Unit, Property_Metadata, Data_Log_Entry

def populate():
    si_units = [{"name": "volt","symbol": "V","measure": "voltage"},
        {"name": "degrees Celcius","symbol": "°C","measure": "temperature"}]

    field_devices = [
        {
            "name": "Remote device 1",
            "serial_id": "abfe-401f-001",
            "description": "Test device ",
            "address": "0001",
            "metadata":[{"name": "battery", "unit": "volt", "data_type": "decimal", "scale": "1.0"},
                        {"name": "temperature", "unit": "degrees Celcius", "data_type": "decimal", "scale": "1.0"},]
        }
        ]
    
    Property_Metadata.objects.all().delete()
    Unit.objects.all().delete()    
    Field_Device.objects.all().delete()
    
    for unit in si_units:
        print("Adding Unit " + str(unit))
        add_unit(unit['name'], unit['symbol'], unit['measure'])

    for device in field_devices:
        print("Adding Device " + str(device))
        add_device( device['name'], device['serial_id'], device['description'], device['address'], device['metadata'] )


def add_unit( name, symbol, measure ):
    entity = Unit.objects.get_or_create(name=name, symbol=symbol, measure=measure)[0]
    entity.save()
    print(">> " + str(entity))
    return entity

def add_device( name, serial_id, description, address, metadata ):
    entity = Field_Device.objects.get_or_create(name=name, serial_id = serial_id)[0]
    entity.description = description
    entity.address = address
    entity.save()
    print(">> " + str(entity))

    for prop_md in metadata:
        unit = Unit.objects.get(name=prop_md["unit"])
        print("    Adding unit=" + str(unit) + " for " + prop_md["name"])
        add_metadata(entity, prop_md["name"], unit, prop_md["data_type"], prop_md["scale"] )
    return entity


def add_metadata(field_device, name, unit, data_type, scale):
    print("Creating metadata for " + str(field_device) + ", name=" + name + ", unit=" + str(unit) + ", data_type=" + data_type + ", scale=" + scale)
    entity = Property_Metadata.objects.get_or_create(field_device = field_device, name=name, unit=unit, data_type=data_type)[0]
    entity.data_type = data_type
    entity.scale = scale
    entity.save()


if __name__ == '__main__':
    print("Starting the Leawood population script...")
    populate()

    

    
