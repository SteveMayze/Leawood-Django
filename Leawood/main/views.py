from django.shortcuts import render

# Create your views here.


def index( request ):
        response = render(request, 'main/index.htm')
        return response
