
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from main.models import Field_Device
from device.forms import DeviceForm
from django.db.models import Q


def check_user( request ):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
		
	## if not request.user.is_authenticated():
	##	raise Http404

    
def device_list( request ):
	
	query = request.GET.get("q")
	current_tab = request.GET.get("t")
	if current_tab == None:
		current_tab = "list"
		
	if request.method == 'POST':
		current_tab = request.POST.get("t")
		payload = request.POST
		print(">> POST: {0}".format(request.POST))
		print(">> content_params: {0}".format(request.content_params))
		for item in payload:
			if item.startswith('device: '):
				print(">> ITEM: {0} = {1}".format(item, payload[item]))
				tmp, device_id = item.split(":")
				device = Field_Device.objects.get(id = device_id)
				device.registered = True
				device.save()
			else:
				print("UNMATCHED ITEM {0}".format(item))
		
	page_request_var = "page"
	tab_request_var = "t"		
	
	queryset_list = Field_Device.objects.filter(registered = True )
	if query and current_tab == "list":
		queryset_list = queryset_list.filter(
				Q(name__icontains=query) | 
				Q(description__icontains=query)
			).distinct()


	queryset_register = Field_Device.objects.filter(registered = False )
	if query and current_tab == "register":
		queryset_register = queryset_register.filter(
				Q(name__icontains=query) | 
				Q(description__icontains=query)
			).distinct()
			
			
	paginator_list = Paginator(queryset_list, 5)
	paginator_register = Paginator(queryset_register, 5)
	page = request.GET.get(page_request_var)
	try:
		print("PAGINATOR LIST PAGE={0}".format(page))
		queryset_l = paginator_list.page(page)
	except PageNotAnInteger:
		queryset_l = paginator_list.page(1)
	except EmptyPage:
		print("PAGINATOR LIST EXCEPTION - EMPTY PAGE")
		queryset_l = paginator_list.page(paginator_list.num_pages)
	try:
		print("PAGINATOR REGISTER PAGE={0}".format(page))
		queryset_r = paginator_register.page(page)
	except PageNotAnInteger:
		queryset_r = paginator_register.page(1)
	except EmptyPage:
		print("PAGINATOR REGISTER EXCEPTION - EMPTY PAGE")
		queryset_r = paginator_register.page(paginator_register.num_pages)



	context_dict = {}
	context_dict["pagetitle"] = "Leawood"
	context_dict["pagename"] = "Devices"
	context_dict["titlebar"] = "Leawood - Devices"
	context_dict["object_list"] = queryset_l
	context_dict["object_register"] = queryset_r
	context_dict["page_request_var"] = page_request_var
	context_dict["tab_request_var"] = tab_request_var
	context_dict["current_tab"] = current_tab
	
	
	response = render(request, 'device/device.htm', context=context_dict)
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
	
	check_user(request)
	
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
	
	check_user(request)		

	
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
	
	check_user(request)		

	instance = get_object_or_404(Field_Device, id=id)
	instance.delete()
	messages.success(request, "Successully deleted")
	return redirect("device:list")
		
	
