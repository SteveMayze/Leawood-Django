# Device URLs

from django.conf.urls import url
## from device import views

from .views import (
	device_list,
	device_create,
	device_scan,
	device_detail,
	device_update,
	device_delete
	)

app_name = 'device'
urlpatterns = [
    url(r'^$', device_list, name='list'),
    url(r'^create/$', device_create, name='create'),
    url(r'^scan/$', device_scan, name='scan'),
    url(r'^(?P<id>\d+)$', device_detail, name='detail'),
    url(r'^(?P<id>\d+)/edit$', device_update, name='update'),
    url(r'^(?P<id>\d+)/delete/$', device_delete, name='device_delete'),
    ]

