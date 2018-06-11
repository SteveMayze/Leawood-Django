from django.contrib import admin
from main.models import Unit, Field_Device, Property_Metadata, Data_Log_Entry

# Register your models here.

class Data_Log_Entry_Admin(admin.ModelAdmin):
	list_display = ['field_device', 'param_metadata', 'time_stamp', 'value']
	list_filter = ['time_stamp', 'field_device','param_metadata']
	class Meta:
		model = Data_Log_Entry

admin.site.register(Unit)
admin.site.register(Field_Device)
admin.site.register(Property_Metadata)
admin.site.register(Data_Log_Entry, Data_Log_Entry_Admin)



