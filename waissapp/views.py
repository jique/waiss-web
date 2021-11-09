from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from .models import SentMsgs, ReceivedMsgs, Personnel, Farm, Sensor, MoistureContent, FieldUnit, Soil, Crop, CalibrationConstant, PercentShaded, Rainfall, Gravimetric, Basin, Furrow, Border, Drip, Sprinkler
from django.forms import modelformset_factory
from .forms import SentMsgsForm, PersonnelForm, SoilForm, CalibForm, CropForm, FarmForm, FieldUnitForm, SensorForm, MCForm, BasinForm, DripForm, SprinklerForm, FurrowForm, BorderForm, PercentShadedForm, GravimetricForm, RainfallForm, RegistrationForm, UserForm
from itertools import chain
from operator import attrgetter
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
import io, csv
from .decorators import unauthenticated_user
from django.http import JsonResponse
from django.template.loader import render_to_string

@unauthenticated_user
def register(request):
	if request.method == 'POST':  # data sent by user
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()  # this will save info to database
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			return redirect ('/dashboard/')
	else:  # display empty form
		form = RegistrationForm
	context = {
		"form" : form,
	}
	return render(request, 'registration/register.html', context)

@login_required
def profile(request):
	user = get_object_or_404(User, id=request.user.id)
	if request.method == 'POST':  # data sent by user
		form = UserForm(request.POST, instance=user)
		if form.is_valid():
			form.save()
			messages.success(request, 'Changes saved!')
	else:
		form = UserForm(instance=user)
	
	context = {
		"form" : form,
	}
	return render(request, 'registration/profile.html', context)

def about(request):
	return render(request, 'waissapp/about.html')

def articles_etcal(request):
	return render(request, 'waissapp/learnmore_etcal.html')

def articles_waiss(request):
	return render(request, 'waissapp/learnmore_waiss.html')

def home(request):
	farm_list = Farm.objects.all()
	lat_list = []
	long_list = []
	f_list = []
	for f in farm_list:
		lat_list.append(f.lat)
		long_list.append(f.long)
		f_list.append(f.name)
	lt_list = [float(i) for i in lat_list]
	lng_list = [float(i) for i in long_list]
	context = {
		"lat_list": lt_list,
		"long_list": lng_list,
		"f_list": f_list,
	}
	return render(request, 'waissapp/home_page.html', context)

def sarai_header(request):
	return render(request, 'waissapp/sarai-header.html')

#CALIB
@login_required
def new_calib(request):
	calib_name = request.session.get('calib_ses', None) #Session
	if calib_name == None:
		form = CalibForm()
		selected_calib_text = '--choose--'
		selected_calib = ""
		select_value = ""
	else:
		calib_name = CalibrationConstant.objects.get(id=calib_name)
		form = CalibForm(instance=calib_name)
		selected_calib = calib_name
		selected_calib_text = calib_name
		select_value = calib_name.calib_equation
	current_user = request.user
	calib_list = CalibrationConstant.objects.filter(author=current_user) #Loading database
	if request.method == 'POST' and 'loadData' in request.POST:
		pk=request.POST.get('loadData')
		id = CalibrationConstant.objects.get(name=pk)
		form = CalibForm(instance=id)
		selected_calib = id
		selected_calib_text = id
		select_value = id.calib_equation
	if request.method == 'POST' and 'btn_submit' in request.POST:  # data sent by user
		form = CalibForm(request.POST)
		calib, created = CalibrationConstant.objects.get_or_create(name=request.POST.get('name'))
		calib.calib_equation = request.POST.get('calib_equation')
		calib.coeff_a = request.POST.get('coeff_a')
		calib.coeff_b = request.POST.get('coeff_b')
		coeff_c = request.POST.get('coeff_c')
		coeff_d = request.POST.get('coeff_d')
		coeff_m = request.POST.get('coeff_m')
		date_tested = request.POST.get('date_tested')
		tested_by = request.POST.get('tested_by')
		calib.author = request.user
		for key in request.POST:
			value = request.POST.get(key)
			if value != "":
				if key == 'coeff_c':
					calib.coeff_c = coeff_c
				if key == 'coeff_d':
					calib.coeff_d = coeff_d
				if key == 'coeff_m':
					calib.coeff_m = coeff_m
				if key == 'date_tested':
					calib.date_tested = date_tested
				if key == 'tested_by':
					calib.tested_by = tested_by
			else:
				if key == 'date_tested':
					calib.date_tested = None
				if key == 'tested_by':
					calib.tested_by = None
		calib.save()
		request.session['calib_ses'] = calib.id
		return redirect('/new_irrigation/')
	context = {
		'calib_form': form,
		'calib_list': calib_list,
		'selected_calib': selected_calib,
		'selected_calib_text': selected_calib_text,
		'select_value': select_value
	}
	return render(request, 'waissapp/new_calib.html', context)

def save_all_calib(request,form,template_name):
	data = dict()
	if request.method == 'POST':
		if form.is_valid():
			form.save()
			data['form_is_valid'] = True
			calibs = CalibrationConstant.objects.all()
			data['list_calib'] = render_to_string('waissapp/list_calib_2.html',{'calibs':calibs})
		else:
			data['form_is_valid'] = False
	context = {
	'form':form
	}
	data['html_form'] = render_to_string(template_name,context,request=request)
	return JsonResponse(data)

@login_required
def add_calib(request):
	if request.method == 'POST':  # data sent by user
		form = CalibForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.author = request.user
			instance.personal = True
			instance.save()
	else:  # display empty form
		form = CalibForm()
	return save_all_calib(request, form, 'waissapp/add_calib.html')

def list_calib(request):
	current_user = request.user
	queryset_1 = CalibrationConstant.objects.filter(author=current_user)
	queryset_2 = CalibrationConstant.objects.filter(personal=False)
	second_list = list(set(queryset_2) - set(queryset_1)) #remove duplicate
	calibs = sorted(chain(queryset_1, second_list), key=attrgetter('name'))#sort as a combined list
	if request.method == 'POST' and 'deleteModal' in request.POST: #delete
		pk=request.POST.get('deleteModal')
		para = CalibrationConstant.objects.get(id=pk)
		para.delete()
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	context = {
		"calibs": calibs,
	}
	return render(request, 'waissapp/list_calib.html', context)

@login_required
def edit_calib(request, id):
	calib = get_object_or_404(CalibrationConstant,id=id)
	if request.method == 'POST':  # data sent by user
		form = CalibForm(request.POST, instance=calib)
	else:
		form = CalibForm(instance=calib)
	return save_all_calib(request, form, 'waissapp/edit_calib.html')
#END#CALIB_PARAMETERS

#CROP_PARAMETERS
@login_required
def new_crop(request):
	crop_name = request.session.get('crop_ses', None) #Session
	if crop_name == None:
		form = CropForm()
		selected_crop_text = '--choose--'
		selected_crop = ""
	else:
		crop_name = Crop.objects.get(id=crop_name)
		form = CropForm(instance=crop_name)
		selected_crop = crop_name
		selected_crop_text = crop_name
	current_user = request.user
	current_user_list = Crop.objects.filter(author=current_user)
	public_use_list = Crop.objects.filter(personal=False)
	combined_list = set(public_use_list) - set(current_user_list)
	crop_list = sorted(chain(current_user_list, combined_list), key=attrgetter('crop'))
	
	if request.method == 'POST' and 'loadData' in request.POST:
		pk=request.POST.get('loadData')
		id = Crop.objects.get(crop=pk)
		form = CropForm(instance=id)
		selected_crop = id
		selected_crop_text = id
	if request.method == 'POST' and 'btn_submit' in request.POST:  # data sent by user
		form = CropForm(request.POST)
		personal_get = request.POST.get('crop')
		try:
			personal_value = Crop.objects.get(crop=personal_get).personal
		except:
			personal_value = True
		if personal_value == False:
			if form.is_valid():
				form = form.save(commit=False)
				form.author = request.user
				form.save()
				request.session['crop_ses'] = form.id
				return redirect('/new_soil/')
		else:
			crop, created = Crop.objects.get_or_create(crop=request.POST.get('crop'))
			crop.growingperiod = request.POST.get('growingperiod')
			crop.root_ini = request.POST.get('root_ini')
			crop.drz = request.POST.get('drz')
			crop.mad = request.POST.get('mad')
			crop.root_growth_model = request.POST.get('root_growth_model')
			crop.select_drip = request.POST.get('select_drip')
			peak_Etcrop = request.POST.get('peak_Etcrop')
			transpiration_ratio = request.POST.get('transpiration_ratio')
			eqnform = request.POST.get('eqnform')
			root_a = request.POST.get('root_a')
			root_b = request.POST.get('root_b')
			root_c = request.POST.get('root_c')
			kc_ini = request.POST.get('kc_ini')
			kc_mid = request.POST.get('kc_mid')
			kc_end = request.POST.get('kc_end')
			kc_cc_1 = request.POST.get('kc_cc_1')
			kc_cc_2 = request.POST.get('kc_cc_2')
			kc_cc_3 = request.POST.get('kc_cc_3')
			source = request.POST.get('source')
			crop.author = request.user
			for key in request.POST:
				value = request.POST.get(key)
				if value != "":
					if key == 'peak_Etcrop':
						crop.peak_Etcrop = peak_Etcrop
					if key == 'transpiration_ratio':
						crop.transpiration_ratio = transpiration_ratio
					if key == 'eqnform':
						crop.eqnform = eqnform
					if key == 'root_a':
						crop.root_a = root_a
					if key == 'root_b':
						crop.root_b = root_b
					if key == 'root_c':
						crop.root_c = root_c
					if key == 'kc_ini':
						crop.kc_ini = kc_ini
					if key == 'kc_mid':
						crop.kc_mid = kc_mid
					if key == 'kc_end':
						crop.kc_end = kc_end
					if key == 'kc_cc_1':
						crop.kc_cc_1 = kc_cc_1
					if key == 'kc_cc_2':
						crop.kc_cc_2 =kc_cc_2
					if key == 'kc_cc_3':
						crop.kc_cc_3 = kc_cc_3
					if key == 'source':
						crop.source = source
			crop.save()
			request.session['crop_ses'] = crop.id
			return redirect('/new_soil/')

	context = {
		'crop_form': form,
		'crop_list': crop_list,
		'selected_crop': selected_crop,
		'selected_crop_text': selected_crop_text
	}

	return render(request, 'waissapp/new_crop.html', context)

def save_all_crop(request,form,template_name):
	data = dict()
	if request.method == 'POST':
		if form.is_valid():
			form.save()
			data['form_is_valid'] = True
			crops = Crop.objects.all()
			data['list_crop'] = render_to_string('waissapp/list_crop_2.html',{'crops':crops})
		else:
			data['form_is_valid'] = False
	context = {
	'form':form
	}
	data['html_form'] = render_to_string(template_name,context,request=request)
	return JsonResponse(data)

@login_required
def add_crop(request):
	if request.method == 'POST':  # data sent by user
		form = CropForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.author = request.user
			instance.personal = True
			instance.save()
	else:  # display empty form
		form = CropForm()
	return save_all_crop(request, form, 'waissapp/add_crop.html')

@login_required
def list_crop(request):
	current_user = request.user
	current_user_list = Crop.objects.filter(author=current_user)
	public_use_list = Crop.objects.filter(personal=False)
	combined_list = set(public_use_list) - set(current_user_list)
	crops = sorted(chain(current_user_list, combined_list), key=attrgetter('crop'))
	if request.method == 'POST' and 'deleteModal' in request.POST:
		pk=request.POST.get('deleteModal')
		para = Crop.objects.get(id=pk)
		para.delete()
		crop_ses = request.session.get('crop_ses', None)
		if crop_ses == para:
			del request.session['crop_ses']
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

	context = {
		"crops": crops,
	}
	return render(request, 'waissapp/list_crop.html', context)

@login_required
def edit_crop(request, id):
	crop = get_object_or_404(Crop,id=id)
	if request.method == 'POST':  # data sent by user
		form = CropForm(request.POST, instance=crop)
	else:
		form = CropForm(instance=crop)
	return save_all_crop(request, form, 'waissapp/edit_crop.html')
#END#CROP_PARAMETERS

#SOIL_PARAMETERS
@login_required
def new_soil(request):
	soil_name = request.session.get('soil_ses', None) #Session
	if soil_name == None:
		form = SoilForm()
		selected_soil = ""
		selected_soil_text = '--choose--'
	else:
		soil_name = Soil.objects.get(id=soil_name)
		form = SoilForm(instance=soil_name)
		selected_soil = soil_name
		selected_soil_text = soil_name
	current_user = request.user
	current_user_list = Soil.objects.filter(author=current_user)
	public_use_list = Soil.objects.filter(personal=False)
	combined_list = set(public_use_list) - set(current_user_list)
	soil_list = sorted(chain(current_user_list, combined_list), key=attrgetter('soiltype'))
	if request.method == 'POST' and 'loadData' in request.POST:
		pk=request.POST.get('loadData')
		id = Soil.objects.get(soiltype=pk)
		form = SoilForm(instance=id)
		selected_soil = id
		selected_soil_text = id

	if request.method == 'POST' and 'btn_submit' in request.POST: # data sent by user
		form = SoilForm(request.POST)
		personal_get = request.POST.get('soiltype')
		try:
			personal_value = Soil.objects.get(soiltype=personal_get).personal
		except:
			personal_value = True
		if personal_value == False:
			if form.is_valid():
				form = form.save(commit=False)
				form.author = request.user
				form.save()
				request.session['soil_ses'] = form.id
				return redirect('/new_calib/')
		else:
			soil, created = Soil.objects.get_or_create(soiltype=request.POST.get('soiltype'))
			soil.fc = request.POST.get('fc')
			soil.pwp = request.POST.get('pwp')
			soil.bln_surface_irrigation = request.POST.get('bln_surface_irrigation')
			intakefamily = request.POST.get('intakefamily')
			source = request.POST.get('source')
			for key in request.POST:
				value = request.POST.get(key)
				if value != "":
					if key == 'intakefamily':
						soil.intakefamily = intakefamily
					if key == 'source':
						soil.source = source
			soil.author = request.user
			soil.save()
			request.session['soil_ses'] = soil.id
			return redirect('/new_calib/')

	context = {
		'soil_form': form,
		'soil_list': soil_list,
		'selected_soil': selected_soil,
		"selected_soil_text": selected_soil_text
	}

	return render(request, 'waissapp/new_soil.html', context)

def save_all_soil(request,form,template_name):
	data = dict()
	if request.method == 'POST':
		if form.is_valid():
			form.save()
			data['form_is_valid'] = True
			soils = Soil.objects.all()
			data['list_soil'] = render_to_string('waissapp/list_soil_2.html',{'soils':soils})
		else:
			data['form_is_valid'] = False
	context = {
	'form':form
	}
	data['html_form'] = render_to_string(template_name,context,request=request)
	return JsonResponse(data)

@login_required
def add_soil(request):
	if request.method == 'POST':  # data sent by user
		form = SoilForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.author = request.user
			instance.personal = True
			instance.save()
	else:  # display empty form
		form = SoilForm()
	return save_all_soil(request, form, 'waissapp/add_soil.html')

def list_soil(request):
	current_user = request.user
	queryset_1 = Soil.objects.filter(author=current_user)
	queryset_2 = Soil.objects.filter(personal=False)
	second_list = list(set(queryset_2) - set(queryset_1)) #remove duplicate
	soils = sorted(chain(queryset_1, second_list), key=attrgetter('soiltype')) #sort combined list
	if request.method == 'POST' and 'deleteModal' in request.POST:
		pk=request.POST.get('deleteModal')
		para = Soil.objects.get(id=pk)
		para.delete()
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

	context = {
		"soils":soils,
	}
	return render(request, 'waissapp/list_soil.html', context)

@login_required
def edit_soil(request, id):
	soil = get_object_or_404(Soil,id=id)
	if request.method == 'POST':  # data sent by user
		form = SoilForm(request.POST, instance=soil)
	else:
		form = SoilForm(instance=soil)
	return save_all_soil(request, form, 'waissapp/edit_soil.html')
#END#SOIL_PARAMETERS

#FIELDUNIT_PARAMETERS
@login_required
def new_fieldunit(request):
	current_user = request.user
	fieldunit_name = request.session.get('fieldunit_ses', None)
	fieldunit_list = FieldUnit.objects.filter(author=current_user)
	if fieldunit_name == None:
		form = FieldUnitForm()
		selected_fieldunit = ""
		selected_fieldunit_text = '--choose--'
	else:
		fieldunit_name = FieldUnit.objects.get(id=fieldunit_name)
		form = FieldUnitForm(instance=fieldunit_name)
		selected_fieldunit = fieldunit_name
		selected_fieldunit_text = fieldunit_name
	
	if request.method == 'POST' and 'loadData' in request.POST:
		pk=request.POST.get('loadData')
		id = FieldUnit.objects.get(name=pk)
		form = FieldUnitForm(instance=id)
		selected_fieldunit = id
		selected_fieldunit_text = id

	if request.method == 'POST' and 'btn_submit' in request.POST:  # data sent by user
		form = FieldUnitForm(request.POST)
		fieldunit, created = FieldUnit.objects.get_or_create(name=request.POST.get('name'))
		fieldunit.usk = request.POST.get('usk')
		fieldunit.number = request.POST.get('number')
		fieldunit.author = request.user
		fieldunit.timestart = request.POST.get('timestart')
		fieldunit.timestop = request.POST.get('timestop')
		fieldunit.fieldunitstatus =  True
		fieldunit.withirrigation = True
		fieldunit.automaticthreshold = True
		fieldunit.samples = 10
		fieldunit.sensorintegrationtime = 10
		fieldunit.delay = 10
		fieldunit.clockcorrection = 0
		fieldunit.save()
		request.session['fieldunit_ses'] = fieldunit.id
		return redirect('/new_sensor/')
	
	context ={
		"fieldunit_form": form,
		"fieldunit_list": fieldunit_list,
		"selected_fieldunit": selected_fieldunit,
		"selected_fieldunit_text": selected_fieldunit_text,
	}

	return render(request, 'waissapp/new_fieldunit.html', context)

def save_all_fieldunit(request,form,template_name):
	data = dict()
	if request.method == 'POST':
		if form.is_valid():
			form.save()
			data['form_is_valid'] = True
			fieldunits = FieldUnit.objects.all()
			data['list_fieldunit'] = render_to_string('waissapp/list_fieldunit_2.html',{'fieldunits':fieldunits})
		else:
			data['form_is_valid'] = False
	context = {
	'form':form
	}
	data['html_form'] = render_to_string(template_name,context,request=request)
	return JsonResponse(data)

@login_required
def add_fieldunit(request):
	if request.method == 'POST':  # data sent by user
		form = FieldUnitForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.author = request.user
			instance.personal = True
			instance.save()
	else:  # display empty form
		form = FieldUnitForm()
	return save_all_fieldunit(request, form, 'waissapp/add_fieldunit.html')

def list_fieldunit(request):
	current_user = request.user
	queryset_1 = FieldUnit.objects.filter(author=current_user)
	queryset_2 = FieldUnit.objects.filter(personal=False)
	second_list = list(set(queryset_2) - set(queryset_1)) #remove duplicate
	fieldunits = sorted(chain(queryset_1, second_list), key=attrgetter('name'))
	if request.method == 'POST' and 'deleteModal' in request.POST: #delete
		pk=request.POST.get('deleteModal')
		para = FieldUnit.objects.get(id=pk)
		para.delete()
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	context = {
		"fieldunits": fieldunits,
	}
	return render(request, 'waissapp/list_fieldunit.html', context)

@login_required
def edit_fieldunit(request, id):
	fieldunit = get_object_or_404(FieldUnit,id=id)
	if request.method == 'POST':  # data sent by user
		form = FieldUnitForm(request.POST, instance=fieldunit)
	else:
		form = FieldUnitForm(instance=fieldunit)
	return save_all_fieldunit(request, form, 'waissapp/edit_fieldunit.html')
#END#FIELDUNIT_PARAMETERS

#SENSOR_PARAMETERS
@login_required
def new_sensor(request):
	current_user = request.user
	fieldunit_ses = request.session.get('fieldunit_ses', None)
	fieldunit_list = FieldUnit.objects.filter(author=current_user)
	fieldunit = FieldUnit.objects.filter(id=fieldunit_ses)
	if fieldunit_ses == None:
		SensorFormSet = modelformset_factory(Sensor, exclude=(), extra=3, can_delete=True)
		formset = SensorFormSet(queryset=Sensor.objects.none())
	else:
		SensorFormSet = modelformset_factory(Sensor, exclude=(), extra=3, max_num=3, can_delete=True)
		formset = SensorFormSet(queryset=Sensor.objects.filter(fieldunit__in=fieldunit))
	
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
		if excess == True:
			return redirect('/new_sensor/')
		else:
			return redirect('/new_system/')

	if request.method == 'POST' and 'btn_submit' in request.POST:
		formset = SensorFormSet(request.POST)
		if formset.is_valid():
			for form in formset:
				data = {
					'name': form.cleaned_data.get('name'),
					'fieldunit': form.cleaned_data.get('fieldunit'),
				}
				sensors, created = Sensor.objects.get_or_create(**data)
				sensors.depth = form.cleaned_data.get('depth')
				sensors.save()
			sensors_list = Sensor.objects.filter(fieldunit__in=fieldunit)
			num_sensors = len(sensors_list)
			if num_sensors > 3:
				excess = True
				return redirect('/new_sensor/')
			else:
				excess= False
				return redirect('/new_system/')
	
	context = {
		"formset": formset,
		"fieldunit_list": fieldunit_list,
		"fieldunit_ses": fieldunit_ses,
		"excess": excess,
		"sensors_list": sensors_list
	}

	return render(request, 'waissapp/new_sensor.html', context)

def save_all_sensor(request,form,template_name):
	data = dict()
	if request.method == 'POST':
		if form.is_valid():
			form.save()
			data['form_is_valid'] = True
			sensors = Sensor.objects.all()
			data['list_sensor'] = render_to_string('waissapp/list_sensor_2.html',{'sensors':sensors})
		else:
			data['form_is_valid'] = False
	context = {
	'form':form
	}
	data['html_form'] = render_to_string(template_name,context,request=request)
	return JsonResponse(data)

@login_required
def add_sensor(request):
	if request.method == 'POST':
		form = SensorForm(request.POST)
		if form.is_valid():
			form.save()
	else:  # display empty form
		form = SensorForm()
	
	return save_all_sensor(request, form, 'waissapp/add_sensor.html')

def list_sensor(request):
	current_user = request.user
	get_fieldunit = FieldUnit.objects.filter(author=current_user)
	sensors = Sensor.objects.filter(fieldunit__in=get_fieldunit)
	if request.method == 'POST' and 'deleteModal' in request.POST:
		pk=request.POST.get('deleteModal')
		para = Sensor.objects.get(id=pk)
		para.delete()
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	context = {
		"sensors":sensors,
	}

	return render(request, 'waissapp/list_sensor.html', context)

@login_required
def edit_sensor(request, id):
	sensor = get_object_or_404(Sensor,id=id)
	if request.method == 'POST':  # data sent by user
		form = SensorForm(request.POST, instance=sensor)
	else:
		form = SensorForm(instance=sensor)
	return save_all_sensor(request, form, 'waissapp/edit_sensor.html')

#END#SENSOR_PARAMETERS

#FARM_PARAMETERS
@login_required
def new_farm(request):
	current_user = request.user
	farm_list = Farm.objects.filter(author=current_user)
	farm_name = request.session.get('farm_ses', None) #Session
	if farm_name == None:
		form = FarmForm()
		selected_farm_text = '--choose--'
		selected_farm = ""
	else:
		farm_name = Farm.objects.get(id=farm_name)
		form = FarmForm(instance=farm_name)
		selected_farm = farm_name
		selected_farm_text = farm_name
	if request.method == 'POST' and 'loadData' in request.POST:
		pk=request.POST.get('loadData')
		id = Farm.objects.get(name=pk)
		form = FarmForm(instance=id)
		selected_farm = id
		selected_farm_text = id
	if request.method == 'POST' and 'btn_submit' in request.POST:  #Saving database
		form = FarmForm(request.POST)
		farm, created = Farm.objects.get_or_create(name=request.POST.get('name'))
		farm.farm_area = request.POST.get('farm_area')
		farm.province = request.POST.get('province')
		farm.municipality = request.POST.get('municipality')
		farm.brgy = request.POST.get('brgy')
		farm.lat = request.POST.get('lat')
		farm.long = request.POST.get('long')
		farm.author = request.user
		farm.save()
		request.session['farm_ses'] = farm.id
		return redirect('/new_personnel/')
			
	context = {
		'farm_form': form,
		'farm_list': farm_list,
		'selected_farm': selected_farm,
		'selected_farm_text': selected_farm_text,
	}
	return render(request, 'waissapp/new_farm.html', context)

def save_all_farm(request,form,template_name):
	data = dict()
	if request.method == 'POST':
		if form.is_valid():
			form.save()
			data['form_is_valid'] = True
			farms = Farm.objects.all()
			data['list_farm'] = render_to_string('waissapp/list_farm_2.html',{'farms':farms})
		else:
			data['form_is_valid'] = False
	context = {
	'form':form
	}
	data['html_form'] = render_to_string(template_name,context,request=request)
	return JsonResponse(data)

@login_required
def add_farm(request):
	if request.method == 'POST':  # data sent by user
		form = FarmForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.author = request.user
			instance.personal = True
			instance.save()
	else:  # display empty form
		form = FarmForm()
	return save_all_farm(request, form, 'waissapp/add_farm.html')

@login_required
def edit_farm(request, id):
	farm = get_object_or_404(Farm,id=id)
	if request.method == 'POST':  # data sent by user
		form = FarmForm(request.POST, instance=farm)
	else:
		form = FarmForm(instance=farm)
	return save_all_farm(request, form, 'waissapp/edit_farm.html')

@login_required
def list_farm(request):
	current_user = request.user
	farms = Farm.objects.filter(author=current_user)
	if request.method == 'POST' and 'deleteModal' in request.POST:
		pk=request.POST.get('deleteModal')
		para = Farm.objects.get(id=pk)
		para.delete()
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	context = {
		"farms": farms,
	}
	return render(request, 'waissapp/list_farm.html', context)
#END#FARM_PARAMETERS

#PERSONNEL_PARAMETERS
def save_all_personnel(request,form,template_name):
	data = dict()
	if request.method == 'POST':
		if form.is_valid():
			form.save()
			data['form_is_valid'] = True
			personnels = Personnel.objects.all()
			data['list_personnel'] = render_to_string('waissapp/list_personnel_2.html',{'personnels':personnels})
		else:
			data['form_is_valid'] = False
	context = {
	'form':form
	}
	data['html_form'] = render_to_string(template_name,context,request=request)
	return JsonResponse(data)

@login_required
def new_personnel(request):
	current_user = request.user
	personnel_list = Personnel.objects.filter(author=current_user)
	personnel_name = request.session.get('personnel_ses', None) #Session
	num_load = ""
	if personnel_name == None:
		form = PersonnelForm()
		selected_personnel = '--choose--'
		selected_id = None
	else:
		personnel_name = Personnel.objects.get(id=personnel_name)
		form = PersonnelForm(instance=personnel_name)
		selected_personnel = str(personnel_name.first_name) + ' ' + str(personnel_name.last_name)
		selected_id = personnel_name.id
		num_load = personnel_name.number
	if request.method == 'POST' and 'loadData' in request.POST:
		pk=request.POST.get('loadData')
		id = Personnel.objects.get(id=pk)
		form = PersonnelForm(instance=id)
		selected_personnel = str(id.first_name) + ' ' + str(id.last_name)
		selected_id = id.id
		num_load = id.number
	if request.method == 'POST' and 'btn_submit' in request.POST:  # data sent by user
		form = PersonnelForm(request.POST)
		personnel, created = Personnel.objects.get_or_create(first_name=request.POST.get('first_name'), last_name=request.POST.get('last_name'))
		personnel.first_name = request.POST.get('first_name')
		personnel.last_name = request.POST.get('last_name')
		personnel.number = request.POST.get('number')
		personnel.author = request.user
		personnel.save()
		request.session['personnel_ses'] = personnel.id
		return redirect('/new_crop/')
	context = {
		'personnel_form': form,
		'personnel_list': personnel_list,
		'selected_personnel': selected_personnel,
		'selected_id': selected_id,
		'num_load': num_load
	}

	return render(request, 'waissapp/new_personnel.html', context)

@login_required
def add_personnel(request):
	if request.method == 'POST':  # data sent by user
		form = PersonnelForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.author = request.user
			instance.personal = True
			instance.save()
	else:  # display empty form
		form = PersonnelForm()
		
	return save_all_personnel(request, form, 'waissapp/add_personnel.html')

def list_personnel(request):
	current_user = request.user
	queryset_1 = Personnel.objects.filter(author=current_user)
	queryset_2 = Personnel.objects.filter(personal=False)
	second_list = list(set(queryset_2) - set(queryset_1)) #remove duplicate
	personnels = sorted(chain(queryset_1, second_list), key=attrgetter('last_name'))
	if request.method == 'POST'and 'deleteModal' in request.POST:
		pk=request.POST.get('deleteModal')
		para = Personnel.objects.get(id=pk)
		para.delete()
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	context = {
		"personnels": personnels,
	}
	return render(request, 'waissapp/list_personnel.html', context)

@login_required
def edit_personnel(request, id):
	personnel = get_object_or_404(Personnel,id=id)
	if request.method == 'POST':  # data sent by user
		form = PersonnelForm(request.POST, instance=personnel)
	else:
		form = PersonnelForm(instance=personnel)
	return save_all_personnel(request, form, 'waissapp/edit_personnel.html')
#END_OF_PERSONNEL_PARAMETERS

@login_required
def add_basin(request):
	if request.method == 'POST':  # data sent by user
		form = BasinForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.bln_irrigation = True
			instance.select_irrigation = "basin"
			instance.author = request.user
			instance.personal = True
			instance.save()
	else:  # display empty form
		form = BasinForm()
	return save_all(request, form, 'waissapp/add_basin.html')

@login_required
def add_furrow(request):
	if request.method == 'POST':  # data sent by user
		form = FurrowForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.bln_irrigation = True
			instance.select_irrigation = "furrow"
			instance.author = request.user
			instance.personal = True
			instance.save()
	else:  # display empty form
		form = FurrowForm()
	return save_all_furrow(request, form, 'waissapp/add_furrow.html')

@login_required
def add_border(request):
	if request.method == 'POST':  # data sent by user
		form = BorderForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.bln_irrigation = True
			instance.select_irrigation = "border"
			instance.author = request.user
			instance.personal = True
			instance.save()
	else:  # display empty form
		form = BorderForm()
	return save_all_border(request, form, 'waissapp/add_border.html')

@login_required
def add_drip(request):
	if request.method == 'POST':  # data sent by user
		form = DripForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.bln_irrigation = True
			instance.select_irrigation = "drip"
			instance.author = request.user
			instance.personal = True
			instance.save()
	else:  # display empty form
		form = DripForm()
	return save_all_drip(request, form, 'waissapp/add_drip.html')

@login_required
def add_sprinkler(request):
	if request.method == 'POST':  # data sent by user
		form = SprinklerForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.bln_irrigation = True
			instance.select_irrigation = "sprinkler"
			instance.author = request.user
			instance.personal = True
			instance.save()
	else:  # display empty form
		form = SprinklerForm()
	return save_all_sprinkler(request, form, 'waissapp/add_sprinkler.html')

@login_required
def new_irrigation(request):
	select_ses = None
	basin_name = request.session.get('basin_ses', None) #Session
	furrow_name = request.session.get('furrow_ses', None)
	border_name = request.session.get('border_ses', None)
	sprinkler_name = request.session.get('sprinkler_ses', None)
	drip_name = request.session.get('drip_ses', None)
	#basin
	basin_ea = 0
	if basin_name == None:
		basin_form = BasinForm()
		selected_basin_text = '--choose--'
		selected_basin = ""
	else:
		basin_name = Basin.objects.get(id=basin_name)
		basin_form = BasinForm(instance=basin_name)
		selected_basin = basin_name
		selected_basin_text = basin_name
		select_ses = 'basin'
		basin_ea = basin_name.ea #for select tag not loading selected value
	
	basin_list = Basin.objects.filter(author=request.user) #Dropdown database
	bln_irrigation = ""
	bln_irrigation_text = ""
	select_irrigation = ""
	if request.method == 'POST' and 'loadData_basin' in request.POST: #load data
		pk = request.POST.get('loadData_basin')
		id = Basin.objects.get(name=pk)
		basin_form = BasinForm(instance=id)
		basin_ea = round(id.ea, 0)
		selected_basin = id
		selected_basin_text = id
		select_ses = 'basin'

	if request.method == 'POST' and 'submit-basin' in request.POST:  #submit data
		basin_form = BasinForm(request.POST)
		basin, created = Basin.objects.get_or_create(name=request.POST.get('name'))
		basin.basin_length = request.POST.get('basin_length')
		basin.discharge = request.POST.get('discharge')
		basin.ea = request.POST.get('ea')
		basin.author = request.user
		basin.save() #save
		request.session.pop('border_ses', None) #delete sessions
		request.session.pop('furrow_ses', None)
		request.session.pop('sprinkler', None)
		request.session.pop('drip_ses', None)
		request.session['basin_ses'] = basin.id #create session
		return redirect('/new_fieldunit/')

	#border
	if border_name == None:
		border_form = BorderForm()
		selected_border_text = '--choose--'
		selected_border = ""
	else:
		border_name = Border.objects.get(id=border_name)
		border_form = BorderForm(request.POST or None, instance=border_name)
		selected_border = border_name
		selected_border_text = border_name
		select_ses = 'border'

	border_list = Border.objects.filter(author=request.user) #Loading database
	if request.method == 'POST' and 'loadData_border' in request.POST:
		pk=request.POST.get('loadData_border')
		id = Border.objects.get(name=pk)
		border_form = BorderForm(instance=id)
		selected_border = id
		selected_border_text = id
		select_ses = 'border'
	if request.method == 'POST' and 'submit-border' in request.POST:
		border_form = BorderForm(request.POST)
		border, created = Border.objects.get_or_create(name=request.POST.get('name'))
		border.author = request.user
		border.discharge = request.POST.get('discharge')
		border.mannings_coeff = request.POST.get('mannings_coeff')
		border.area_slope = request.POST.get('area_slope')
		border.save() #save
		request.session.pop('basin_ses', None) #delete session from other irrigation systems
		request.session.pop('furrow_ses', None)
		request.session.pop('sprinkler_ses', None)
		request.session.pop('drip_ses', None)
		request.session['border_ses'] = border.id #create session for border
		return redirect('/new_fieldunit/')
	#furrow
	if furrow_name == None:
		furrow_form = FurrowForm()
		selected_furrow_text = '--choose--'
		selected_furrow = ""
	else:
		furrow_name = Furrow.objects.get(id=furrow_name)
		furrow_form = FurrowForm(request.POST or None, instance=furrow_name)
		selected_furrow = furrow_name
		selected_furrow_text = furrow_name
		select_ses = 'furrow'
	furrow_list = Furrow.objects.filter(author=request.user) #Loading database
	if request.method == 'POST' and 'loadData_furrow' in request.POST:
		pk = request.POST.get('loadData_furrow')
		id = Furrow.objects.get(name=pk)
		furrow_form = FurrowForm(instance=id)
		selected_furrow = id
		selected_furrow_text = id
		select_ses = 'furrow'
	if request.method == 'POST' and 'submit-furrow' in request.POST:
		furrow_form = FurrowForm(request.POST)
		furrow, created = Furrow.objects.get_or_create(name=request.POST.get('name'))
		furrow.author = request.user
		furrow.discharge = request.POST.get('discharge')
		furrow.mannings_coeff = request.POST.get('mannings_coeff')
		furrow.area_slope = request.POST.get('area_slope')
		furrow.bln_furrow_type = bool(request.POST.get('bln_furrow_type'))
		furrow.furrow_spacing = request.POST.get('furrow_spacing')
		furrow.furrow_length = request.POST.get('furrow_length')
		furrow.save() #save
		request.session.pop('basin_ses', None) #delete other sessions from other irrigation systems
		request.session.pop('border_ses', None)
		request.session.pop('sprinkler', None)
		request.session.pop('drip_ses', None)
		request.session['furrow_ses'] = furrow.id #create session for furrow
		return redirect('/new_fieldunit/')
	#sprinkler
	if sprinkler_name == None:
		sprinkler_form = SprinklerForm()
		selected_sprinkler_text = "--choose--"
		selected_sprinkler = ""
	else:
		sprinkler_name = Sprinkler.objects.get(id=sprinkler_name)
		sprinkler_form = SprinklerForm(request.POST or None, instance=sprinkler_name)
		selected_sprinkler = sprinkler_name
		selected_sprinkler_text = ""
		select_ses = 'sprinkler'
	sprinkler_list = Sprinkler.objects.filter(author=request.user) #Loading database
	if request.method == 'POST' and 'loadData_sprinkler' in request.POST:
		pk=request.POST.get('loadData_sprinkler')
		id = Sprinkler.objects.get(name=pk)
		sprinkler_form = SprinklerForm(instance=id)
		selected_sprinkler = id			
		selected_sprinkler_text = id
		select_ses = 'sprinkler'
	if request.method == 'POST' and 'submit-sprinkler' in request.POST:
		sprinkler_form = SprinklerForm(request.POST)
		sprinkler, created = Sprinkler.objects.get_or_create(name=request.POST.get('name'))
		sprinkler.author = request.user
		discharge = request.POST.get('discharge')
		nozzle_diameter = request.POST.get('nozzle_diameter')
		operating_pressure = request.POST.get('operating_pressure')
		sprinkler.ea = request.POST.get('ea')
		sprinkler.lateral_spacing = request.POST.get('lateral_spacing')
		sprinkler.with_q_bln = request.POST.get('with_q_bln')
		sprinkler.sprinkler_spacing = request.POST.get('sprinkler_spacing')
		for key in request.POST:
			value = request.POST.get(key)
			if value != "":
				if key == "discharge":
					sprinkler.discharge = discharge
				if key == "nozzle_diameter":
					sprinkler.nozzle_diameter = nozzle_diameter
				if key == "operating_pressure":
					sprinkler.operating_pressure = operating_pressure
		sprinkler.save()
		request.session['sprinkler_ses'] = sprinkler.id
		request.session.pop('basin_ses', None)
		request.session.pop('furrow_ses', None)
		request.session.pop('border_ses', None)
		request.session.pop('drip_ses', None)
		return redirect('/new_fieldunit/')
	#drip
	if drip_name == None:
		drip_form = DripForm()
		selected_drip_text = "--choose--"
		selected_drip = ""
	else:
		selected_drip = Drip.objects.get(id=drip_name)
		drip_form = DripForm(request.POST or None, instance=selected_drip)
		selected_drip_text = selected_drip
		select_ses = 'drip'
	drip_list = Drip.objects.filter(author=request.user) #Loading database
	if request.method == 'POST' and 'loadData_drip' in request.POST:
		pk=request.POST.get('loadData_drip')
		selected_drip = Drip.objects.get(name=pk)
		drip_form = DripForm(instance=selected_drip)
		selected_drip_text = selected_drip
		select_ses = 'drip'
	if request.method == 'POST' and 'submit-drip' in request.POST:
		drip_form = DripForm(request.POST)
		drip, created = Drip.objects.get_or_create(name=request.POST.get('name'))
		drip.author = request.user
		drip.discharge = request.POST.get('discharge')
		drip.bln_single_lateral = bool(request.POST.get('bln_single_lateral'))
		drip.emitters_per_plant = request.POST.get('emitters_per_plant')
		drip.emitter_spacing = request.POST.get('emitter_spacing')
		drip.plant_spacing = request.POST.get('plant_spacing')
		drip.row_spacing = request.POST.get('row_spacing')
		drip.wetted_dia = request.POST.get('wetted_dia')
		drip.bln_ii = request.POST.get('bln_ii')
		drip.EU = request.POST.get('EU')
		irrigation_interval = request.POST.get('irrigation_interval')
		for key in request.POST:
			value = request.POST.get(key)
			if value != "":
				if key == "irrigation_interval":
					drip.irrigation_interval = irrigation_interval
		drip.save()
		request.session.pop('basin_ses', None)
		request.session.pop('furrow_ses', None)
		request.session.pop('sprinkler_ses', None)
		request.session.pop('border_ses', None)
		request.session['drip_ses'] = drip.id
		return redirect('/new_fieldunit/')
	context = {
		"basin" : basin_form,
		"basin_ea": basin_ea,
		"border" : border_form,
		"furrow" : furrow_form,
		"sprinkler" : sprinkler_form,
		"drip" : drip_form,
		"selected_basin": selected_basin,
		"selected_border": selected_border,
		"selected_furrow": selected_furrow,
		"selected_sprinkler": selected_sprinkler,
		"selected_drip": selected_drip,
		"selected_basin_text": selected_basin_text,
		"selected_border_text": selected_border_text,
		"selected_furrow_text": selected_furrow_text,
		"selected_sprinkler_text": selected_sprinkler_text,
		"selected_drip_text": selected_drip_text,
		"basin_list": basin_list,
		"border_list": border_list,
		"furrow_list": furrow_list,
		"sprinkler_list": sprinkler_list,
		"drip_list": drip_list,
		"select_ses": select_ses,
		"bln_irrigation": bln_irrigation,
		"bln_irrigation_text": bln_irrigation_text,
		"select_irrigation": select_irrigation
	}
	return render(request, 'waissapp/new_irrigation.html', context)

@login_required
def list_basin(request):
	current_user = request.user
	queryset_1 = Basin.objects.filter(author=current_user)
	queryset_2 = Basin.objects.filter(personal=False)
	basins = sorted(chain(queryset_1, queryset_2), key=attrgetter('name'))
	if request.method == 'POST' and 'deleteModal' in request.POST:
		pk=request.POST.get('deleteModal')
		para = Basin.objects.get(id=pk)
		para.delete()
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	context = {
		"basins": basins,
	}
	return render(request, 'waissapp/list_basin.html', context)
@login_required
def list_border(request):
	current_user = request.user
	queryset_1 = Border.objects.filter(author=current_user)
	queryset_2 = Border.objects.filter(personal=False)
	borders = sorted(chain(queryset_1, queryset_2), key=attrgetter('name'))
	if request.method == 'POST' and 'deleteModal' in request.POST:
		pk=request.POST.get('deleteModal')
		para = Border.objects.get(id=pk)
		para.delete()
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	context = {
		"borders": borders,
	}
	return render(request, 'waissapp/list_border.html', context)
@login_required
def list_furrow(request):
	current_user = request.user
	queryset_1 = Furrow.objects.filter(author=current_user)
	queryset_2 = Furrow.objects.filter(personal=False)
	furrows = sorted(chain(queryset_1, queryset_2), key=attrgetter('name'))
	if request.method == 'POST' and 'deleteModal' in request.POST:
		pk=request.POST.get('deleteModal')
		para = Furrow.objects.get(id=pk)
		para.delete()
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	context = {
		"furrows": furrows,
	}
	return render(request, 'waissapp/list_furrow.html', context)
@login_required
def list_sprinkler(request):
	current_user = request.user
	queryset_1 = Sprinkler.objects.filter(author=current_user)
	queryset_2 = Sprinkler.objects.filter(personal=False)
	sprinklers = sorted(chain(queryset_1, queryset_2))
	if request.method == 'POST' and 'deleteModal' in request.POST:
		pk=request.POST.get('deleteModal')
		para = Sprinkler.objects.get(id=pk)
		para.delete()
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	context = {
		"sprinklers": sprinklers,
	}
	return render(request, 'waissapp/list_sprinkler.html', context)
@login_required
def list_drip(request):
	current_user = request.user
	queryset_1 = Drip.objects.filter(author=current_user)
	queryset_2 = Drip.objects.filter(personal=False)
	drips = sorted(chain(queryset_1, queryset_2), key=attrgetter('name'))
	if request.method == 'POST' and 'deleteModal' in request.POST:
		pk=request.POST.get('deleteModal')
		para = Drip.objects.get(id=pk)
		para.delete()
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	context = {
		"drips": drips,
	}
	return render(request, 'waissapp/list_drip.html', context)

def save_all(request,form,template_name):
	data = dict()
	if request.method == 'POST':
		if form.is_valid():
			form.save()
			data['form_is_valid'] = True
			basins = Basin.objects.all()
			data['list_basin'] = render_to_string('waissapp/list_basin_2.html',{'basins':basins})
		else:
			data['form_is_valid'] = False
	context = {
	'form':form
	}
	data['html_form'] = render_to_string(template_name,context,request=request)
	return JsonResponse(data)

def save_all_border(request,form,template_name):
	data = dict()
	if request.method == 'POST':
		if form.is_valid():
			form.save()
			data['form_is_valid'] = True
			borders = Border.objects.all()
			data['list_border'] = render_to_string('waissapp/list_border_2.html',{'borders':borders})
		else:
			data['form_is_valid'] = False
	context = {
	'form':form
	}
	data['html_form'] = render_to_string(template_name,context,request=request)
	return JsonResponse(data)

def save_all_furrow(request,form,template_name):
	data = dict()
	if request.method == 'POST':
		if form.is_valid():
			form.save()
			data['form_is_valid'] = True
			furrows = Furrow.objects.all()
			data['list_furrow'] = render_to_string('waissapp/list_furrow_2.html',{'furrows':furrows})
		else:
			data['form_is_valid'] = False
	context = {
	'form':form
	}
	data['html_form'] = render_to_string(template_name,context,request=request)
	return JsonResponse(data)

def save_all_drip(request,form,template_name):
	data = dict()
	if request.method == 'POST':
		if form.is_valid():
			form.save()
			data['form_is_valid'] = True
			drips = Drip.objects.all()
			data['list_drip'] = render_to_string('waissapp/list_drip_2.html',{'drips':drips})
		else:
			data['form_is_valid'] = False
	context = {
	'form':form
	}
	data['html_form'] = render_to_string(template_name,context,request=request)
	return JsonResponse(data)

def save_all_sprinkler(request,form,template_name):
	data = dict()
	if request.method == 'POST':
		if form.is_valid():
			form.save()
			data['form_is_valid'] = True
			sprinklers = Sprinkler.objects.all()
			data['list_sprinkler'] = render_to_string('waissapp/list_sprinkler_2.html',{'sprinklers':sprinklers})
		else:
			data['form_is_valid'] = False
	context = {
	'form':form
	}
	data['html_form'] = render_to_string(template_name,context,request=request)
	return JsonResponse(data)

@login_required
def edit_basin(request, id):
	basin = get_object_or_404(Basin,id=id)
	if request.method == 'POST':  # data sent by user
		form = BasinForm(request.POST, instance=basin)
	else:
		form = BasinForm(instance=basin)
	return save_all(request, form, 'waissapp/edit_basin.html')

@login_required
def edit_border(request, id):
	border = get_object_or_404(Border,id=id)
	if request.method == 'POST':  # data sent by user
		form = BorderForm(request.POST, instance=border)
	else:
		form = BorderForm(instance=border)
	return save_all_border(request, form, 'waissapp/edit_border.html')
	
@login_required
def edit_furrow(request, id):
	furrow = get_object_or_404(Furrow,id=id)
	if request.method == 'POST':  # data sent by user
		form = FurrowForm(request.POST, instance=furrow)
	else:
		form = FurrowForm(instance=furrow)
	return save_all_furrow(request, form, 'waissapp/edit_furrow.html')

@login_required
def edit_drip(request, id):
	drip = get_object_or_404(Drip,id=id)
	if request.method == 'POST':  # data sent by user
		form = DripForm(request.POST, instance=drip)
	else:
		form = DripForm(instance=drip)
	return save_all_drip(request, form, 'waissapp/edit_drip.html')

@login_required
def edit_sprinkler(request, id):
	sprinkler = get_object_or_404(Sprinkler,id=id)
	if request.method == 'POST':  # data sent by user
		form = SprinklerForm(request.POST, instance=sprinkler)
	else:
		form = SprinklerForm(instance=sprinkler)
	return save_all_sprinkler(request, form, 'waissapp/edit_sprinkler.html')

#Messages
@login_required
def list_msgs(request):
	current_user = request.user
	get_fieldunit = Personnel.objects.filter(author=current_user)
	receivedmsgs = ReceivedMsgs.objects.filter(number__in=get_fieldunit)
	sentmsgs = SentMsgs.objects.filter(number__in=get_fieldunit)

	llist = sorted(chain(receivedmsgs, sentmsgs), key=attrgetter('timestamp'))
	final_list = reversed(llist)

	if request.method == 'POST':  # data sent by user
		form = SentMsgsForm(request.POST)
		if form.is_valid():
			form.save()  # this will save info to database
			return redirect('/messages/')
	else:  # display empty form
		form = SentMsgsForm()

	context = {
		"list": get_fieldunit,
		"joinedlist": final_list,
		"form": form,
	}

	return render(request, 'waissapp/messages.html', context)

@login_required
def delete_msgs(request, pk): #deleteconversation
	para = SentMsgs.objects.get(id=pk)

	if request.method == 'POST':
		para.delete()
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	context = {
		"item":para,
	}
	return render(request, 'waissapp/delete_messages.html', context)

@login_required
def view_msg(request, number):
	current_user = request.user
	get_fieldunit = Personnel.objects.filter(author=current_user)
	receivedmsgs = ReceivedMsgs.objects.filter(number__in=get_fieldunit)
	sentmsgs = SentMsgs.objects.filter(number__in=get_fieldunit)
	llist = sorted(chain(receivedmsgs, sentmsgs), key=attrgetter('timestamp'))
	joined_list = reversed(llist)

	cel_number = Personnel.objects.get(number=number)
	received = cel_number.receivedmsgs_set.all()
	sent = cel_number.sentmsgs_set.all()
	result = sorted(chain(received,sent), key=attrgetter('timestamp'))

	if request.method == 'POST':  # data sent by user
		form = SentMsgsForm(request.POST)
		if form.is_valid():
			form.save()  # this will save info to database
			return redirect('/messages/') #fix this, redirect to request.referer
	else:  # display empty form
		form = SentMsgsForm()

	context = {
		"list": get_fieldunit,
		"number": number,
		"form": form,
		"joined_list": joined_list,
		"result": result,
	}
	return render(request, 'waissapp/view-conversation.html', context)

#MC Readings
@login_required
def new_mc(request):
	DataFormSet = modelformset_factory(MoistureContent, exclude=(), extra=6)
	formset = DataFormSet(queryset=MoistureContent.objects.none())
	if request.method == 'POST':
		formset = DataFormSet(request.POST)
		if formset.is_valid():
			formset.save()
			return redirect('/')
	else:  # display empty form
		formset = DataFormSet(queryset=MoistureContent.objects.none())
	
	context = {
		"formset": formset,
	}

	return render(request, 'waissapp/new_mc.html', context)

def save_all_mc(request,form,template_name):
	data = dict()
	if request.method == 'POST':
		if form.is_valid():
			form.save()
			data['form_is_valid'] = True
			mcs = MoistureContent.objects.all()
			data['list_mc'] = render_to_string('waissapp/list_mc_2.html',{'mcs':mcs})
		else:
			data['form_is_valid'] = False
	context = {
	'form':form
	}
	data['html_form'] = render_to_string(template_name,context,request=request)
	return JsonResponse(data)

@login_required
def add_mc(request):
	if request.method == 'POST':
		form = MCForm(request.POST)
		if form.is_valid():
			form.save()
	else:  # display empty form
		form = MCForm()
	return save_all_mc(request, form, 'waissapp/add_mc.html')

@login_required
def upload_csv(request):
	prompt = {
		'order': 'order: sensor_name, timestamp (format: yyyy-mm-d h:m:ss), value'
	}
	if request.method == "GET":
		return render(request, 'waissapp/upload_csv.html', prompt)
	
	csv_file = request.FILES['file']

	if not csv_file.name.endswith('.csv'):
		messages.error(request, "This is not a csv file.")
	
	data_set = csv_file.read().decode('UTF-8')
	io_string = io.StringIO(data_set)
	next(io_string)
	for column in csv.reader(io_string, delimiter=","):
		_, created = MoistureContent.objects.update_or_create(
			sensor= Sensor.objects.get(name=(column[0])), # returns error: expecting id but return is sensor_name if Sensor.objects.get(name="") is removed; needed for foreignkeys
			timestamp=column[1],
			mc_data=column[2],
		)
		return redirect('/dashboard/')
	context ={}

	return render (request, 'waissapp/upload_csv.html', context)

@login_required
def edit_mc(request, id):
	mc = get_object_or_404(MoistureContent,id=id)
	if request.method == 'POST':  # data sent by user
		form = MCForm(request.POST, instance=mc)
	else:
		form = MCForm(instance=mc)
	return save_all_mc(request, form, 'waissapp/edit_mc.html')

@login_required
def list_mc(request, name):
	sensor_instance = Sensor.objects.get(name=name)
	get_mc = MoistureContent.objects.filter(sensor=sensor_instance)
	mcs = reversed(sorted(get_mc, key=attrgetter('timestamp')))

	if request.method == 'POST':
		pk=request.POST.get('deleteModal')
		para = MoistureContent.objects.get(id=pk)
		para.delete()
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

	context = {
		"mcs": mcs,
	}
	return render(request, 'waissapp/list_mc.html', context)

def save_all_rainfall(request,form,template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            rainfalls = Rainfall.objects.all()
            data['list_rainfall'] = render_to_string('waissapp/list_rainfall_2.html',{'rainfalls':rainfalls})
        else:
            data['form_is_valid'] = False
    context = {
    'form':form
    }
    data['html_form'] = render_to_string(template_name,context,request=request)
    return JsonResponse(data)

@login_required
def add_rainfall(request):
	if request.method == 'POST':  # data sent by user
		form = RainfallForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.author = request.user
			instance.personal = True
			instance.save()
	else:  # display empty form
		form = RainfallForm()
	return save_all_rainfall(request, form, 'waissapp/add_rainfall.html')

@login_required
def edit_rainfall(request, id):
	rainfall = get_object_or_404(Rainfall,id=id)
	if request.method == 'POST':  # data sent by user
		form = BorderForm(request.POST, instance=rainfall)
	else:
		form = BorderForm(instance=rainfall)
	return save_all_rainfall(request, form, 'waissapp/edit_rainfall.html')

@login_required
def list_rainfall(request):
	queryset = Rainfall.objects.all()
	rainfalls = reversed(sorted(queryset, key=attrgetter('timestamp')))

	if request.method == 'POST'and 'deleteModal' in request.POST:
		pk=request.POST.get('deleteModal')
		para = Rainfall.objects.get(id=pk)
		para.delete()
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

	context = {
		"rainfalls": rainfalls,
	}
	return render(request, 'waissapp/list_rainfall.html', context)

@login_required
def delete_rainfall(request, pk):
	para = Rainfall.objects.get(id=pk)
	if request.method == 'POST':
		para.delete()
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	context = {
		"item":para	
	}
	return render(request, 'waissapp/delete_rainfall.html', context)

def save_all_shaded(request,form,template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            shadeds = PercentShaded.objects.all()
            data['list_shaded'] = render_to_string('waissapp/list_shaded_2.html',{'shadeds':shadeds})
        else:
            data['form_is_valid'] = False
    context = {
    'form':form
    }
    data['html_form'] = render_to_string(template_name,context,request=request)
    return JsonResponse(data)

@login_required
def add_shaded(request):
	if request.method == 'POST':  # data sent by user
		form = PercentShadedForm(request.POST)
		if form.is_valid():
			form.save()
	else:  # display empty form
		form = PercentShadedForm()
	return save_all_shaded(request, form, 'waissapp/add_shaded.html')

@login_required
def edit_shaded(request, id):
	shaded = get_object_or_404(PercentShaded, id=id)
	if request.method == 'POST':  # data sent by user
		form = PercentShadedForm(request.POST, instance=shaded)
	else: 
		form = PercentShadedForm(instance=shaded)
	return save_all_shaded(request, form, 'waissapp/edit_shaded.html')

@login_required
def list_shaded(request):
	queryset = PercentShaded.objects.all()
	shadeds = reversed(sorted(queryset, key=attrgetter('date')))

	if request.method == 'POST'and 'deleteModal' in request.POST:
		pk=request.POST.get('deleteModal')
		para = PercentShaded.objects.get(id=pk)
		para.delete()
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

	context = {
		"shadeds": shadeds,
	}
	return render(request, 'waissapp/list_shaded.html', context)

@login_required
def delete_shaded(request, pk):
	para = PercentShaded.objects.get(id=pk)
	if request.method == 'POST':
		para.delete()
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	context = {
		"item":para	
	}
	return render(request, 'waissapp/delete_shaded.html', context)

def save_all_gravi(request,form,template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            gravis = Gravimetric.objects.all()
            data['list_gravi'] = render_to_string('waissapp/list_gravi_2.html',{'gravis':gravis})
        else:
            data['form_is_valid'] = False
    context = {
    'form':form
    }
    data['html_form'] = render_to_string(template_name,context,request=request)
    return JsonResponse(data)

@login_required
def add_gravi(request):
	if request.method == 'POST':  # data sent by user
		form = GravimetricForm(request.POST)
		if form.is_valid():
			form.save()
	else:  # display empty form
		form = GravimetricForm()
	return save_all_gravi(request, form, 'waissapp/add_gravi.html')

@login_required
def edit_gravi(request, id):
	gravi = get_object_or_404(Gravimetric, id=id)
	if request.method == 'POST':  # data sent by user
		form = GravimetricForm(request.POST, instance=gravi)
	else: 
		form = GravimetricForm(instance=gravi)
	return save_all_gravi(request, form, 'waissapp/edit_gravi.html')
@login_required
def list_gravi(request):
	queryset = Gravimetric.objects.all()
	gravis = reversed(sorted(queryset, key=attrgetter('timestamp')))

	if request.method == 'POST'and 'deleteModal' in request.POST:
		pk=request.POST.get('deleteModal')
		para = Gravimetric.objects.get(id=pk)
		para.delete()
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

	context = {
		"gravis": gravis,
	}
	return render(request, 'waissapp/list_gravi.html', context)

@login_required
def delete_gravimetric(request, pk):
	para = Gravimetric.objects.get(id=pk)
	if request.method == 'POST':
		para.delete()
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	context = {
		"item":para	
	}
	return render(request, 'waissapp/delete_gravimetric.html', context)