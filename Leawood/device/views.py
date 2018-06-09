from django.shortcuts import render

# Create your views here.



def index( request ):
        response = render(request, 'device/index.htm')
        return response
