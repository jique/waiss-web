#WAISSYSTEMS
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Personnel, Farm, FieldUnit, Sensor, Soil, Crop, CalibrationConstant, WAISSystems, Basin, Furrow, Border, Drip, Sprinkler
from .forms import WAISSystemsForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from itertools import chain
from operator import attrgetter

def save_all_system(request,form,template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            systems = WAISSystems.objects.all()
            data['list_system'] = render_to_string('waissapp/list_system_2.html',{'systems':systems})
        else:
            data['form_is_valid'] = False
    context = {
    'form':form
    }
    data['html_form'] = render_to_string(template_name,context,request=request)
    return JsonResponse(data)

@login_required
def add_system(request):
	if request.method == 'POST':  # data sent by user
		form = WAISSystemsForm(request.POST)
		if form.is_valid():
			new_system = form.save(commit=False)
			new_system.author = request.user
			new_system.personal = True
			new_system.save()
	else:  # display empty form
		form = WAISSystemsForm()
	return save_all_system(request, form, 'waissapp/add_system.html')

@login_required
def list_system(request):
	current_user = request.user
	systems = WAISSystems.objects.filter(author=current_user)

	if request.method == 'POST' and 'deleteModal' in request.POST:
		pk=request.POST.get('deleteModal')
		para = WAISSystems.objects.get(id=pk)
		para.delete()
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

	context = {
		"systems": systems,
	}
	return render(request, 'waissapp/list_system.html', context)

@login_required
def edit_system(request, id):
	system = get_object_or_404(WAISSystems, id=id)
	if request.method == 'POST':  # data sent by user
		form = WAISSystemsForm(request.POST, instance=system)
	else:
		form = WAISSystemsForm(instance=system)
	return save_all_system(request, form, 'waissapp/edit_system.html')
@login_required
def new_system(request):
	current_user = request.user
	#lists
	farm_list = Farm.objects.filter(author=current_user)
	farm_manager_list = Personnel.objects.filter(author=current_user)
	#
	current_user_list = Crop.objects.filter(author=current_user)
	public_use_list = Crop.objects.filter(personal=False)
	combined_list = set(public_use_list) - set(current_user_list)
	crop_list = sorted(chain(current_user_list, combined_list), key=attrgetter('crop'))
	#
	current_user_list = Soil.objects.filter(author=current_user)
	public_use_list = Soil.objects.filter(personal=False)
	combined_list = set(public_use_list) - set(current_user_list)
	soil_list = sorted(chain(current_user_list, combined_list), key=attrgetter('soiltype'))
	#
	fieldunit_list = FieldUnit.objects.filter(author=current_user)
	calib_list = CalibrationConstant.objects.filter(author=current_user)
	basin_list = Basin.objects.filter(author=current_user)
	border_list = Border.objects.filter(author=current_user)
	furrow_list = Furrow.objects.filter(author=current_user)
	sprinkler_list = Sprinkler.objects.filter(author=current_user)
	drip_list = Drip.objects.filter(author=current_user)

	#sessions
	farm_ses = request.session.get('farm_ses', None)
	farm_manager_ses = request.session.get('personnel_ses', None)
	crop_ses = request.session.get('crop_ses', None)
	soil_ses = request.session.get('soil_ses', None)
	calib_ses = request.session.get('calib_ses', None)
	fieldunit_ses = request.session.get('fieldunit_ses', None)
	basin_ses = request.session.get('basin_ses', None)
	border_ses = request.session.get('border_ses', None)
	furrow_ses = request.session.get('furrow_ses', None)
	drip_ses = request.session.get('drip_ses', None)
	sprinkler_ses = request.session.get('sprinkler_ses', None)

	no_irrigation = ""
	if basin_ses or border_ses or furrow_ses or sprinkler_ses or drip_ses:
		no_irrigation = False
	else:
		no_irrigation = True

	#GetFromInputBox
	farm = request.POST.get('farm')
	farm_manager = request.POST.get('farm_manager')
	crop = request.POST.get('crop')
	soil = request.POST.get('soil')
	calib = request.POST.get('calib')
	fieldunit = request.POST.get('fieldunit')
	basin = request.POST.get('basin')
	border = request.POST.get('border')
	furrow = request.POST.get('furrow')
	sprinkler = request.POST.get('sprinkler')
	drip = request.POST.get('drip')

	form = WAISSystemsForm(request.POST or None)
	if request.method == 'POST' and 'btn_submit' in request.POST:  # data sent by user
		farm = Farm.objects.get(id=farm)
		farm_manager = Personnel.objects.get(id=farm_manager)
		crop = Crop.objects.get(id=crop)
		soil = Soil.objects.get(id=soil)
		calib = CalibrationConstant.objects.get(id=calib)
		fieldunit = FieldUnit.objects.get(id=fieldunit)

		form = WAISSystemsForm(request.POST)
		waiss, created = WAISSystems.objects.get_or_create(name=request.POST.get('name'))
		waiss.author = request.user
		waiss.fieldunit = fieldunit
		waiss.farm = farm
		waiss.farm_manager = farm_manager
		waiss.crop = crop
		waiss.soil = soil
		waiss.calib = calib
		for key in request.POST:
			value = request.POST.get(key)
			if value != "":
				if key == 'basin':
					waiss.basin = basin
				if key == "border":
					waiss.border = border
				if key == "furrow":
					waiss.furrow = furrow
				if key == "sprinkler":
					waiss.sprinkler = sprinkler
				if key == "drip":
					waiss.drip = drip
		waiss.save()
		return redirect('/dashboard/')

	ses_farm = "" #blank sessions .text
	ses_farm_manager = ""
	ses_crop = ""
	ses_soil = ""
	ses_calib = ""
	ses_fieldunit = ""
	ses_basin = ""
	ses_border = ""
	ses_furrow = ""
	ses_drip = ""
	ses_sprinkler = ""
	
	if farm_ses != None: #get sessions .text
		ses_farm = Farm.objects.get(id=farm_ses)
	if farm_manager_ses != None:
		ses_farm_manager = Personnel.objects.get(id=farm_manager_ses)
		f = ses_farm_manager.first_name
		l = ses_farm_manager.last_name
		ses_farm_manager = str(f)+ ' ' + str(l)
	if crop_ses != None:
		ses_crop = Crop.objects.get(id=crop_ses)
	if soil_ses != None:
		ses_soil = Soil.objects.get(id=soil_ses)
	if calib_ses != None:
		ses_calib = CalibrationConstant.objects.get(id=calib_ses)
	if fieldunit_ses != None:
		ses_fieldunit = FieldUnit.objects.get(id=fieldunit_ses)
	if basin_ses != None:
		ses_basin = Basin.objects.get(id=basin_ses)
	if border_ses != None:
		ses_border = Border.objects.get(id=border_ses)
	if furrow_ses != None:
		ses_furrow = Furrow.objects.get(id=furrow_ses)
	if sprinkler_ses != None:
		ses_sprinkler = Sprinkler.objects.get(id=sprinkler_ses)
	if drip_ses != None:
		ses_drip = Drip.objects.get(id=drip_ses)

	fieldunit = FieldUnit.objects.filter(id=fieldunit_ses) #to check excess sensors
	sensors_list = Sensor.objects.filter(fieldunit__in=fieldunit)
	num_sensors = len(sensors_list)
	if num_sensors > 3:
		excess = True
	else:
		excess= False
	if request.method == 'POST' and 'delete_sensor' in request.POST:
		sensor_id = request.POST.get('delete_sensor')
		sensor_obj = Sensor.objects.get(id=sensor_id)
		sensor_obj.delete()
		return redirect('/new_system/')

	context = {
		"form": form,
		"basin_ses": basin_ses,
		"border_ses": border_ses,
		"furrow_ses": furrow_ses,
		"drip_ses": drip_ses,
		"sprinkler_ses": sprinkler_ses,
		"farm_list": farm_list,
		"farm_manager_list": farm_manager_list,
		"crop_list": crop_list,
		"soil_list": soil_list,
		"calib_list": calib_list,
		"fieldunit_list": fieldunit_list,
		"basin_list": basin_list,
		"border_list": border_list,
		"furrow_list": furrow_list,
		"sprinkler_list": sprinkler_list,
		"drip_list": drip_list,
		"farm_ses": farm_ses,
		"farm_manager_ses": farm_manager_ses,
		"crop_ses": crop_ses,
		"soil_ses": soil_ses,
		"calib_ses": calib_ses,
		"fieldunit_ses": fieldunit_ses,
		"ses_farm": ses_farm,
		"ses_farm_manager": ses_farm_manager,
		"ses_crop": ses_crop,
		"ses_soil": ses_soil,
		"ses_calib": ses_calib,
		"ses_fieldunit": ses_fieldunit,
		"ses_basin": ses_basin,
		"ses_border": ses_border,
		"ses_furrow": ses_furrow,
		"ses_sprinkler": ses_sprinkler,
		"ses_drip": ses_drip,
		"sensors_list": sensors_list,
		"excess": excess,
		"no_irrigation": no_irrigation,
	}
	return render(request, 'waissapp/new_system.html', context)