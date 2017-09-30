from django.db import models

# Create your models here.

"""
Field Device
The entity the represents a device positioned out in the field that
will be equipped with a sensor and some type of data sender

"""
class Field_Device(models.Model):
     name = models.CharField(max_length=100, unique=True)
     serial_id = models.CharField(max_length=100, unique=True)
     description = models.CharField(max_length=1000, blank=True)
     address=models.CharField(max_length=200)

     class Meta:
         ordering = ('name',)

     def __str__(self):
          return self.name



"""
Unit
A reference table to hold the SI units of measure. This is used to render
the output for the graphs and reports of the data log entry for a field
device.
"""
class Unit(models.Model):
     name = models.CharField(max_length=100, unique=True)
     symbol = models.CharField(max_length=15)
     measure = models.CharField(max_length=100)


     class Meta:
          ordering = ('name',)

     def __str__(self):
          return self.name

"""
Metadata
This defines the name, data type and if requried the SI Unit of the
property value. This information is provided by the Field Devices on pairing
"""
class Property_Metadata(models.Model):
     field_device = models.ForeignKey(Field_Device, on_delete=models.CASCADE)
     name = models.CharField(max_length=100)
     unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
     data_type = models.CharField(max_length=50, blank=True)
     scale = models.DecimalField(max_digits=9, decimal_places=3, default=1.0)

     class Meta:
          verbose_name_plural = 'Property_Metadata'
          unique_together = ('field_device', 'name')
          indexes = [
               models.Index(fields=['field_device', 'name']),
          ]
          order_with_respect_to = 'field_device'

     def __str__(self):
          return str(self.field_device) + ' ' + self.name + ' ' + str(self.unit)


"""
Data Log Entry
This represents a unit of data recorded from the field device at a
particular point in time.
"""
class Data_Log_Entry(models.Model):
     field_device = models.ForeignKey(Field_Device, on_delete=models.CASCADE)
     name = models.CharField(max_length=100)
     time_stamp = models.DateTimeField()
     value = models.DecimalField(max_digits=9, decimal_places=3)
     metadata = models.ForeignKey(Property_Metadata, on_delete=models.CASCADE)

     class Meta:
          verbose_name_plural = 'Data_log_Entries'
          unique_together = ("field_device", "name", "time_stamp")
          indexes = [
               models.Index(fields=['field_device', 'name', 'time_stamp']),
          ]
          order_with_respect_to = 'field_device'

     def __str__(self):
          return self.field_device + ' ' + self.name + ' ' + self.time_stamp + ' ' + self.value


