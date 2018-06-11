from django.shortcuts import render

# Create your views here.



def index( request ):
	context_dict = {}
	context_dict["pagetitle"] = "Leawood"
	context_dict["pagename"] = "Devices"
	context_dict["titlebar"] = "Leawood - Devices"
	response = render(request, 'device/index.htm', context=context_dict)
	return response

