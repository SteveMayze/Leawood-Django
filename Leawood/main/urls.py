from django.conf.urls import url, include
from main import views

app_name = 'main'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^fence$', views.index, name='fence'),
    ]

