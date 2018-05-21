from django.shortcuts import render
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from device.as_dash import dispatcher

# Create your views here.

def dash(request, **kwargs):
    ''' '''
    return HttpResponse(dispatcher(request))

@csrf_exempt
def dash_ajax(request):
    ''' '''
    return HttpResponse(dispatcher(request), content_type='application/json')
    
## def index(request):
## 	return render(request, 'device/index.htm')
	
	
