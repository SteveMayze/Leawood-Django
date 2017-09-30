from django.contrib import admin
from main.models import Unit, Field_Device, Property_Metadata, Data_Log_Entry

# Register your models here.

admin.site.register(Unit)
admin.site.register(Field_Device)
admin.site.register(Property_Metadata)
admin.site.register(Data_Log_Entry)



