
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from main.models import Field_Device
from device.forms import DeviceForm

    
def device_list( request ):
	queryset_list = Field_Device.objects.all()
	page_request_var = "page"
	paginator = Paginator(queryset_list, 5)
	page = request.GET.get(page_request_var)
	try:	
		queryset = paginator.page(page)
	except PageNotAnInteger:
		queryset = paginator.page(1)
	except EmptyPage:
		queryset = paginator.page(paginator.num_pages)

	context_dict = {}
	context_dict["pagetitle"] = "Leawood"
	context_dict["pagename"] = "Devices"
	context_dict["titlebar"] = "Leawood - Devices"
	context_dict["object_list"] = queryset
	context_dict["page_request_var"] = page_request_var
	
	
	response = render(request, 'device/list.htm', context=context_dict)
	return response


def device_detail( request , id=None ):
	
	instance = get_object_or_404(Field_Device, id=id)
	
	context_dict = {}
	context_dict["pagetitle"] = "Leawood"
	context_dict["pagename"] = "Devices"
	context_dict["titlebar"] = "Leawood - Devices"
	context_dict["instance"] = instance
	response = render(request, 'device/detail.htm', context=context_dict)
	return response


	
def device_create( request ):
	form = DeviceForm(request.POST or None)
	
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request, "Successfully Created")
		return HttpResponseRedirect(instance.get_absolute_url())
	
	context_dict = {}
	context_dict["pagetitle"] = "Leawood"
	context_dict["pagename"] = "Devices"
	context_dict["titlebar"] = "Leawood - Devices"
	context_dict["form"] = form
	response = render(request, 'device/device_form.htm', context=context_dict)
	return response
		
	
def device_update( request, id=None ):
	instance = get_object_or_404(Field_Device, id=id)
	form = DeviceForm(request.POST or None, instance=instance)
	
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request, "Saved")
		return HttpResponseRedirect(instance.get_absolute_url())

	context_dict = {}
	context_dict["pagetitle"] = "Leawood"
	context_dict["pagename"] = "Devices"
	context_dict["titlebar"] = "Leawood - Devices"
	context_dict["instance"] = instance
	context_dict["form"] = form

	response = render(request, 'device/device_form.htm', context=context_dict)
	return response



def device_delete( request, id=None ):
	instance = get_object_or_404(Field_Device, id=id)
	instance.delete()
	messages.success(request, "Successully deleted")
	return redirect("device:list")
		
	
