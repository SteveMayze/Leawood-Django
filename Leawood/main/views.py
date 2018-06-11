from django.shortcuts import render

# Create your views here.


def index( request ):
	context_dict = {}
	context_dict["pagetitle"] = "Leawood"
	context_dict["pagename"] = "Leawood"
	context_dict["titlebar"] = "Leawood - main"
	response = render(request, 'main/index.htm', context=context_dict)
	return response
