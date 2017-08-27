from django.db import models

# Create your models here.

class Field_Device(models.Model):
     name = models.CharField(max_length=100, unique=true)
     description = models.CharField(max_length(1000), blank=True)
     address=models.CharField(max_length=200)

     class Meta:
         ordering = ('name',)



class Data_logger(models.Model):
    field_device = models.ForeignKey(Field_Device, on_delete=models.CASCADE)
    time_stamp = models.DateTimeField()
    metric_01 = models.DecimalField(max_digits=9, decimal_places=3)
    metric_02 = models.DecimalField(max_digits=9, decimal_places=3)
    metric_03 = models.DecimalField(max_digits=9, decimal_places=3)

    class Meta:
        ordering = ('field_device.name', 'time_stamp',)




class Metric_Binding(models.Model):
    field_device = models.ForeignKey(Field_Device, on_delete=models.CASCADE)
    metric_01_name = models.CharField(max_length=100)
    metric_01_scale = models.DecimalField(max_digits=6, deimcal_places=3)
    metric_01_unit = modles.CharField(max_length=100)
    metric_02_name = models.CharField(max_length=100)
    metric_02_scale = models.DecimalField(max_digits=6, deimcal_places=3)
    metric_02_unit = modles.CharField(max_length=100)
    metric_03_name = models.CharField(max_length=100)
    metric_03_scale = models.DecimalField(max_digits=6, deimcal_places=3)
    metric_03_unit = modles.CharField(max_length=100)

    class Meta:
        ordering = ('field_device.name',)
