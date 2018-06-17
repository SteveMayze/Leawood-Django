from django import forms

from main.models import Field_Device


class DeviceForm(forms.ModelForm):
	class Meta:
		model=Field_Device
		fields = [
			"name",
			"serial_id",
			"description",
			"address"
		]

