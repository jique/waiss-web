from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from .models import SentMsgs, ReceivedMsgs, Personnel, Farm, Sensor, MoistureContent, FieldUnit, Soil, Crop, CalibrationConstant, WAISSystems, PercentShaded, Rainfall, Gravimetric, Basin, Furrow, Border, Drip, Sprinkler
import datetime
from datetime import date, datetime
from django import forms
from django.forms import modelformset_factory
from .forms import SentMsgsForm, PersonnelForm, SoilForm, CalibForm, CropForm, FarmForm, FieldUnitForm, SensorForm, MCForm, WAISSystemsForm, BasinForm, DripForm, SprinklerForm, FurrowForm, BorderForm, PercentShadedForm, GravimetricForm, RainfallForm
from itertools import chain
from operator import attrgetter
import math
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
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
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()  # this will save info to database
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			return redirect ('/new_farm/')
	else:  # display empty form
		form = UserCreationForm
	context = {
		"form" : form,
	}
	return render(request, 'registration/register.html', context)

@login_required
def profile(request):
	user = request.user
	profile = User.objects.filter(username=user)
	context = {
		"form" : profile,
	}
	return render(request, 'registration/profile.html', context)

def about(request):
	return render(request, 'waissapp/about.html')

def sarai_header(request):
	return render(request, 'waissapp/sarai-header.html')


def about_calc(request):
	return render(request, 'waissapp/about_calc.html')

def options(request):
	return render(request, 'waissapp/simp_advanced.html')
#WAISSYSTEMS

@login_required
def new_system(request):
	if request.method == 'POST':  # data sent by user
		form = WAISSystemsForm(request.POST)
		if form.is_valid():
			new_system = form.save(commit=False)
			new_system.author = request.user
			new_system.personal = True
			new_system.save()
			return redirect('/new_sensor/')
	else:  # display empty form
		form = WAISSystemsForm()
	
	context = {
		"form": form,
	}
	return render(request, 'waissapp/new_system.html', context)

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

#CALIB
@login_required
def new_calib(request):
	if request.method == 'POST':  # data sent by user
		form = CalibForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.author = request.user
			instance.personal = True
			instance.save()
			return redirect('/new_system/')
	else:  # display empty form
		form = CalibForm()
	return render(request, 'waissapp/new_calib.html', {'calib_form': form})

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
	calibs = sorted(chain(queryset_1, queryset_2), key=attrgetter('timestamp'))

	#delete
	if request.method == 'POST' and 'deleteModal' in request.POST:
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
	if request.method == 'POST':  # data sent by user
		form = CropForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.author = request.user
			instance.personal = True
			instance.save()
			return redirect('/new_soil/')
	else:  # display empty form
		form = CropForm()
	return render(request, 'waissapp/new_crop.html', {'crop_form': form})

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

def list_crop(request):
	current_user = request.user
	queryset_1 = Crop.objects.filter(author=current_user)
	queryset_2 = Crop.objects.filter(personal=False)
	crops = sorted(chain(queryset_1, queryset_2), key=attrgetter('timestamp'))

	if request.method == 'POST' and 'deleteModal' in request.POST:
		pk=request.POST.get('deleteModal')
		para = Crop.objects.get(id=pk)
		para.delete()
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
	if request.method == 'POST':  # data sent by user
		form = SoilForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.author = request.user
			instance.personal = True
			instance.save()
			return redirect('/new_calib/')
	else:  # display empty form
		form = SoilForm()

	return render(request, 'waissapp/new_soil.html', {'soil_form': form})

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
	soils = sorted(chain(queryset_1, queryset_2), key=attrgetter('timestamp'))
	
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
	if request.method == 'POST':  # data sent by user
		form = FieldUnitForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.author = request.user
			instance.personal = True
			instance.save()
			return redirect('/new_sensor/')
	else:  # display empty form
		form = FieldUnitForm()

	return render(request, 'waissapp/new_fieldunit.html', {'fieldunit_form': form})

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
	fieldunits = chain(queryset_1, queryset_2)
	
	if request.method == 'POST' and 'deleteModal' in request.POST:
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
	return save_all_fieldunit(request, form, 'waissapp/add_fieldunit.html')
#END#FIELDUNIT_PARAMETERS

#SENSOR_PARAMETERS
@login_required
def new_sensor(request):
	SensorFormSet = modelformset_factory(Sensor, exclude=(), extra=3)
	formset = SensorFormSet(queryset=Sensor.objects.none())
	if request.method == 'POST':
		formset = SensorFormSet(request.POST)
		if formset.is_valid():
			formset.save()
			return redirect('/new_mc/')
	else:  # display empty form
		formset = SensorFormSet(queryset=Sensor.objects.none())
	
	context = {
		"formset": formset,
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
	queryset_1 = Sensor.objects.filter(fieldunit__in=get_fieldunit)
	queryset_2 = CalibrationConstant.objects.filter(personal=False)
	sensors = chain(queryset_1, queryset_2)

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
	return save_all_sensor(request, form, 'waissapp/add_sensor.html')

#END#SENSOR_PARAMETERS

#FARM_PARAMETERS
@login_required
def new_farm(request):
	if request.method == 'POST' and 'btnform2' in request.POST:  # data sent by user
		form = FarmForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.author = request.user
			instance.personal = True
			instance.save()
			return redirect('/new_personnel/')
	else:  # display empty form
		form = FarmForm()

	return render(request, 'waissapp/new_farm.html', {'farm_form': form})

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
	queryset_1 = Farm.objects.filter(author=current_user)
	queryset_2 = Farm.objects.filter(personal=False)
	farms = chain(queryset_1, queryset_2)

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
	if request.method == 'POST':  # data sent by user
		form = PersonnelForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.author = request.user
			instance.personal = True
			instance.save()
			return redirect('/new_crop/')
	else:  # display empty form
		form = PersonnelForm()

	return render(request, 'waissapp/new_personnel.html', {'personnel_form': form})

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
	personnels = chain(queryset_1, queryset_2)

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
			instance.author = request.user
			instance.personal = True
			instance.save()
	else:  # display empty form
		form = SprinklerForm()
	return save_all_sprinkler(request, form, 'waissapp/add_sprinkler.html')

@login_required
def new_irrigation(request):
	return render(request, 'waissapp/new_irrigation.html')

@login_required
def new_basin(request):
	if request.method == 'POST':  # data sent by user
		form = BasinForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.author = request.user
			instance.personal = True
			instance.save()
			return redirect('/new_fieldunit/')
	else:  # display empty form
		form = BasinForm()

	return render(request, 'waissapp/new_basin.html', {'form': form})

@login_required
def new_furrow(request):
	if request.method == 'POST':  # data sent by user
		form = FurrowForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.author = request.user
			instance.personal = True
			instance.save()
			return redirect('/new_fieldunit/')
	else:  # display empty form
		form = FurrowForm()

	return render(request, 'waissapp/new_furrow.html', {'irrigation_form': form})

@login_required
def new_border(request):
	if request.method == 'POST':  # data sent by user
		form = BorderForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.author = request.user
			instance.personal = True
			instance.save()
			return redirect('/new_fieldunit/')
	else:  # display empty form
		form = BorderForm()

	return render(request, 'waissapp/new_border.html', {'irrigation_form': form})

@login_required
def new_drip(request):
	if request.method == 'POST':  # data sent by user
		form = DripForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.author = request.user
			instance.personal = True
			instance.save()
			return redirect('/new_fieldunit/')
	else:  # display empty form
		form = DripForm()

	return render(request, 'waissapp/new_drip.html', {'irrigation_form': form})

@login_required
def new_sprinkler(request):
	if request.method == 'POST':  # data sent by user
		form = SprinklerForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.author = request.user
			instance.personal = True
			instance.save()
			return redirect('/list_new_fieldunit/')
	else:  # display empty form
		form = SprinklerForm()

	return render(request, 'waissapp/new_sprinkler.html', {'irrigation_form': form})

def list_basin(request):
	current_user = request.user
	queryset_1 = Basin.objects.filter(author=current_user)
	queryset_2 = Basin.objects.filter(personal=False)
	basins = chain(queryset_1, queryset_2)

	if request.method == 'POST' and 'deleteModal' in request.POST:
		pk=request.POST.get('deleteModal')
		para = Basin.objects.get(id=pk)
		para.delete()
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

	context = {
		"basins": basins,
	}
	return render(request, 'waissapp/list_basin.html', context)

def list_border(request):
	current_user = request.user
	queryset_1 = Border.objects.filter(author=current_user)
	queryset_2 = Border.objects.filter(personal=False)
	borders = chain(queryset_1, queryset_2)

	if request.method == 'POST' and 'deleteModal' in request.POST:
		pk=request.POST.get('deleteModal')
		para = Border.objects.get(id=pk)
		para.delete()
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

	context = {
		"borders": borders,
	}
	return render(request, 'waissapp/list_border.html', context)

def list_furrow(request):
	current_user = request.user
	queryset_1 = Furrow.objects.filter(author=current_user)
	queryset_2 = Furrow.objects.filter(personal=False)
	furrows = chain(queryset_1, queryset_2)

	if request.method == 'POST' and 'deleteModal' in request.POST:
		pk=request.POST.get('deleteModal')
		para = Furrow.objects.get(id=pk)
		para.delete()
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

	context = {
		"furrows": furrows,
	}
	return render(request, 'waissapp/list_furrow.html', context)

def list_sprinkler(request):
	current_user = request.user
	queryset_1 = Sprinkler.objects.filter(author=current_user)
	queryset_2 = Sprinkler.objects.filter(personal=False)
	sprinklers = chain(queryset_1, queryset_2)

	if request.method == 'POST' and 'deleteModal' in request.POST:
		pk=request.POST.get('deleteModal')
		para = Sprinkler.objects.get(id=pk)
		para.delete()
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

	context = {
		"sprinklers": sprinklers,
	}
	return render(request, 'waissapp/list_sprinkler.html', context)

def list_drip(request):
	current_user = request.user
	queryset_1 = Drip.objects.filter(author=current_user)
	queryset_2 = Drip.objects.filter(personal=False)
	drips = chain(queryset_1, queryset_2)

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
		form = Sprinkler(instance=sprinkler)
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

	context ={}

	return render (request, 'waissapp/upload_csv.html', context)

@login_required
def edit_mc(request, id):
	mc = get_object_or_404(MoistureContent,id=id)
	if request.method == 'POST':  # data sent by user
		form = MCForm(request.POST, instance=mc)
	else:
		form = MCForm(instance=mc)
	return save_all_mc(request, form, 'waissapp/add_mc.html')

def list_mc(request, name):
	sensor_instance = Sensor.objects.get(name=name)
	get_mc = MoistureContent.objects.filter(sensor=sensor_instance)
	mcs = reversed(sorted(get_mc, key=attrgetter('timestamp')))

	if request.method == 'POST':
		pk=request.POST.get('id')
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