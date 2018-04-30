from tastypie.resources import ModelResource
from main.models import Field_Device, Unit, Property_Metadata, Data_Log_Entry
from tastypie import fields
from tastypie.api import Api
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.exceptions import InvalidFilterError


class AuthenticationMixin(object):
    def __init__(self):
        self._meta.authentication = ApiKeyAuthentication()
        self._meta.authorization = DjangoAuthorization()
        super(AuthenticationMixin, self).__init__()


class Field_DeviceResource(AuthenticationMixin, ModelResource):
    class Meta:
        queryset = Field_Device.objects.all()
        resource_name = 'field_device'

class UnitResource(AuthenticationMixin, ModelResource):
    class Meta:
        queryset = Unit.objects.all()
        resource_name = 'unit'

class Property_MetadataResource(AuthenticationMixin, ModelResource):
    field_device = fields.ForeignKey(Field_DeviceResource, 'field_device')
    unit = fields.ForeignKey(UnitResource, 'unit')
    class Meta:
        queryset = Property_Metadata.objects.all()
        resource_name = 'metadata'

class Data_Log_EntryResource(AuthenticationMixin, ModelResource):
    field_device = fields.ForeignKey(Field_DeviceResource, 'field_device')

    class Meta:
        queryset = Data_Log_Entry.objects.all()
        resource_name = 'log_entry'


v1_api = Api(api_name='v1')
v1_api.register(Field_DeviceResource())
v1_api.register(UnitResource())
v1_api.register(Property_MetadataResource())
v1_api.register(Data_Log_EntryResource())
