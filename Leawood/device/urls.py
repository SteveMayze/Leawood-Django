# Device URLs

from django.conf.urls import url, include
from device import views

app_name = 'device'
urlpatterns = [
    url(r'^$', views.dash),
    ]

