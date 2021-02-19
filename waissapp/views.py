from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import SentMsgs, ReceivedMsgs, Personnel, Farm, Sensor, MoistureContent, FieldUnit, Soil, IntakeFamily, Crop, CalibrationConstant, IrrigationParameters, WAISSystems
from django.utils import timezone
import datetime
from datetime import date, datetime
import json
from django.urls import reverse
from django import forms
from django.template import RequestContext
from django.forms import modelformset_factory
from .forms import SentMsgsForm, PersonnelForm, SoilForm, CalibForm, CropForm, FarmForm, FieldUnitForm, IrrigationParametersForm, SensorForm, MCForm, SystemForm, WAISSystemsForm
from django.db import transaction, IntegrityError
from itertools import chain
from operator import attrgetter

def index(request):
	receivedmsgs = ReceivedMsgs.objects.all()
	sentmsgs = SentMsgs.objects.all()
	llist = sorted(chain(receivedmsgs, sentmsgs), key=attrgetter('timestamp'))
	reversed_list =reversed(llist)

	system = WAISSystems.objects.all()
	#para = WAISSystems.objects.get(id=pk)
	#form = WAISSystemsForm(instance=para)

	if request.method == 'POST':  # data sent by user
		form = WAISSystemsForm(request.POST, instance=para)
		if form.is_valid():
			form.save()  # this will save info to database
			return redirect('/')
	
	context = {
		"final_list": reversed_list,
		"system": system,
		#"form":form,
		#"item":para,
	}
	return render(request, 'waissapp/index.html', context)

def load_page(request):
	return render(request, 'waissapp/load_page.html')

def computation_option(request):
	return render(request, 'waissapp/simp_advanced.html')

def register(request):
	context={}
	return render(request, 'waissapp/registration/register.html', context)

def login(request):
	context={}
	return render(request, 'waissapp/registration/login.html', context)

def about(request):
	return render(request, 'waissapp/about.html')

def about_calc(request):
	return render(request, 'waissapp/about_calc.html')
#WAISSYSTEMS

def new_system(request):
	if request.method == 'POST':  # data sent by user
		form = WAISSystemsForm(request.POST)
		if form.is_valid():
			form.save()  # this will save info to database
	else:  # display empty form
		form = WAISSystemsForm()
	
	context = {
		"form": form,
	}
	return render(request, 'waissapp/new_system.html', context)

def add_system(request):
	if request.method == 'POST':  # data sent by user
		form = WAISSystemsForm(request.POST)
		if form.is_valid():
			form.save()  # this will save info to database
	else:  # display empty form
		form = WAISSystemsForm()
	
	context = {
		"form": form,
	}
	return render(request, 'waissapp/add_system.html', context)

def list_system(request):
	queryset = WAISSystems.objects.all()
	context = {
		"list":queryset,
	}
	return render(request, 'waissapp/list_system.html', context)

def edit_system(request, pk):
	para = WAISSystems.objects.get(id=pk)
	form = WAISSystemsForm(instance=para)

	if request.method == 'POST':  # data sent by user
		form = WAISSystemsForm(request.POST, instance=para)
		if form.is_valid():
			form.save()  # this will save info to database
			return redirect('/')

	context = {
		"form":form,
		"item":para,
	}
	return render(request, 'waissapp/edit_system.html', context)

def delete_system(request, pk):
	para = WAISSystems.objects.get(id=pk)
	if request.method == 'POST':
		para.delete()
		return redirect('/show-intakefamily-database/')
	context = {
		"item":para	
	}
	return render(request, 'waissapp/delete_system.html', context)

#CALIB
def new_calib(request):
	if request.method == 'POST':  # data sent by user
		form = CalibForm(request.POST)
		if form.is_valid():
			form.save()  # this will save info to database
			return redirect('/choose-irrigation/')
	else:  # display empty form
		form = CalibForm()
	return render(request, 'waissapp/new_calib.html', {'calib_form': form})

def add_calib(request):
	if request.method == 'POST':  # data sent by user
		form = CalibForm(request.POST)
		if form.is_valid():
			form.save()  # this will save info to database
			return redirect('/show-calib-database/')
	else:  # display empty form
		form = CalibForm()
	return render(request, 'waissapp/add_calib.html', {'calib_form': form})

def list_calib(request):
	queryset = CalibrationConstant.objects.all()
	context = {
		"calib_list":queryset,
	}
	return render(request, 'waissapp/list_calib.html', context)

def edit_calib(request, pk):
	para = CalibrationConstant.objects.get(id=pk)
	form = CalibForm(instance=para)

	if request.method == 'POST':  # data sent by user
		form = CalibForm(request.POST, instance=para)
		if form.is_valid():
			form.save()  # this will save info to database
			return redirect('/show-calib-database/')

	context = {
		"calib_form":form,
		"item":para,
	}
	return render(request, 'waissapp/edit_calib.html', context)

def delete_calib(request, pk):
	para = CalibrationConstant.objects.get(id=pk)
	if request.method == 'POST':
		para.delete()
		return redirect('/list_calib/')
	context = {
		"item":para	
	}
	return render(request, 'waissapp/delete_calib.html', context)
#END#CALIB_PARAMETERS

#CROP_PARAMETERS
def new_crop(request):
	if request.method == 'POST':  # data sent by user
		form = CropForm(request.POST)
		if form.is_valid():
			form.save()  # this will save info to database
			return redirect('/new_soil/')
	else:  # display empty form
		form = CropForm()
	return render(request, 'waissapp/new_crop.html', {'crop_form': form})

def add_crop(request):
	if request.method == 'POST':  # data sent by user
		form = CropForm(request.POST)
		if form.is_valid():
			form.save()  # this will save info to database
			return redirect('/list_crop/')
	else:  # display empty form
		form = CropForm()

	return render(request, 'waissapp/add_crop.html', {'form': form})

def list_crop(request):
	queryset = Crop.objects.all()
	context = {
		"crop_list":queryset,
	}
	return render(request, 'waissapp/list_crop.html', context)

def edit_crop(request, pk):
	para = Crop.objects.get(id=pk)
	form = CropForm(instance=para)

	if request.method == 'POST':  # data sent by user
		form = CropForm(request.POST, instance=para)
		if form.is_valid():
			form.save()  # this will save info to database
			return redirect('/list_crop/')

	context = {
		"crop_form":form,
		"item": para,
	}
	return render(request, 'waissapp/edit_crop.html', context)

def delete_crop(request, pk):
	para = Crop.objects.get(id=pk)
	if request.method == 'POST':
		para.delete()
		return redirect('/list_crop/')
	context = {
		"item":para	
	}
	return render(request, 'waissapp/delete_crop.html', context)
#END#CROP_PARAMETERS

#SOIL_PARAMETERS
def new_soil(request):
    if request.method == 'POST':  # data sent by user
        form = SoilForm(request.POST)
        if form.is_valid():
            form.save()  # this will save info to database
            return redirect('/new_fieldunit/')
    else:  # display empty form
        form = SoilForm()

    return render(request, 'waissapp/new_soil.html', {'soil_form': form})

def add_soil(request):
    if request.method == 'POST':  # data sent by user
        form = SoilForm(request.POST)
        if form.is_valid():
            form.save()  # this will save info to database
            return redirect('/list-soil/')
    else:  # display empty form
        form = SoilForm()

    return render(request, 'waissapp/add_soil.html', {'soil_form': form})

def list_soil(request):
	queryset = Soil.objects.all()

	context = {
		"soil_list":queryset,
	}
	return render(request, 'waissapp/list_soil.html', context)

def edit_soil(request, pk):
	para = Soil.objects.get(id=pk)
	form = SoilForm(instance=para)

	if request.method == 'POST':  # data sent by user
		form = SoilForm(request.POST, instance=para)
		if form.is_valid():
			form.save()  # this will save info to database
			return redirect('/list_soil/')

	context = {
		"soil_form":form,
		"item":para,
	}
	return render(request, 'waissapp/edit_soil.html', context)

def delete_soil(request, pk):
	para = Soil.objects.get(id=pk)
	if request.method == 'POST':
		para.delete()
		return redirect('/list_soil/')
	context = {
		"item":para	
	}
	return render(request, 'waissapp/delete_soil.html', context)
#END#SOIL_PARAMETERS

#FIELDUNIT_PARAMETERS
def new_fieldunit(request):
    if request.method == 'POST':  # data sent by user
        form = FieldUnitForm(request.POST)
        if form.is_valid():
            form.save()  # this will save info to database
            return redirect('/new_sensor/')
    else:  # display empty form
        form = FieldUnitForm()

    return render(request, 'waissapp/new_fieldunit.html', {'fieldunit_form': form})

def add_fieldunit(request):
    if request.method == 'POST':  # data sent by user
        form = FieldUnitForm(request.POST)
        if form.is_valid():
            form.save()  # this will save info to database
            return redirect('/list_fieldunit/')
    else:  # display empty form
        form = FieldUnitForm()

    return render(request, 'waissapp/add_fieldunit.html', {'fieldunit_form': form})

def list_fieldunit(request):
	queryset = FieldUnit.objects.all()

	context = {
		"fieldunit_list":queryset,
	}
	return render(request, 'waissapp/list_fieldunit.html', context)

def edit_fieldunit(request, pk):
	para = FieldUnit.objects.get(id=pk)
	form = FieldUnitForm(instance=para)

	if request.method == 'POST':  # data sent by user
		form = FieldUnitForm(request.POST, instance=para)
		if form.is_valid():
			form.save()  # this will save info to database
			return redirect('/list_fieldunit/')

	context = {
		"fieldunit_form":form,
		"item":para,
	}
	return render(request, 'waissapp/edit_fieldunit.html', context)

def delete_fieldunit(request, pk):
	para = FieldUnit.objects.get(id=pk)
	if request.method == 'POST':
		para.delete()
		return redirect('/list_fieldunit/')
	context = {
		"item":para	
	}
	return render(request, 'waissapp/delete_fieldunit.html', context)
#END#FIELDUNIT_PARAMETERS

#SENSOR_PARAMETERS
def new_sensor(request):
	SensorFormSet = modelformset_factory(Sensor, exclude=(), extra=3)
	form = SensorFormSet(queryset=Sensor.objects.none())
	if request.method == 'POST':
		form = SensorFormSet(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/new_mc/')
	else:  # display empty form
		form = SensorFormSet(queryset=Sensor.objects.none())

	return render(request, 'waissapp/new_sensor.html', {'form':form})

def add_sensor(request):
	SensorFormSet = modelformset_factory(Sensor, exclude=(), extra=3)
	form = SensorFormSet(queryset=Sensor.objects.none())
	if request.method == 'POST':
		form = SensorFormSet(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/new_mc/')
	else:  # display empty form
		form = SensorFormSet(queryset=Sensor.objects.none())
	
	return render(request, 'waissapp/add_sensor.html', {'sensor_form': form})

def list_sensor(request):
	queryset = Sensor.objects.all()

	context = {
		"sensor_list":queryset,
	}
	return render(request, 'waissapp/list_sensor.html', context)

def edit_sensor(request, pk):
	para = Sensor.objects.get(id=pk)
	form = SensorForm(instance=para)

	if request.method == 'POST':  # data sent by user
		form = SensorForm(request.POST, instance=para)
		if form.is_valid():
			form.save()  # this will save info to database
			return redirect('/list_sensor/')

	context = {
		"sensor_form":form,
		"item": para,
	}
	return render(request, 'waissapp/edit_sensor.html', context)

def delete_sensor(request, pk):
	para = Sensor.objects.get(id=pk)
	if request.method == 'POST':
		para.delete()
		return redirect('/list_sensor/')
	context = {
		"item":para	
	}
	return render(request, 'waissapp/delete_sensor.html', context)
#END#SENSOR_PARAMETERS

#FARM_PARAMETERS
def new_farm(request):
	if request.method == 'POST':  # data sent by user
		form = FarmForm(request.POST)
		if form.is_valid():
			form.save()  # this will save info to database
	else:  # display empty form
		form = FarmForm()
	
	context = {
		"farm_form":form,
	}

	return render(request, 'waissapp/new_farm.html', context)

def add_farm(request):
	if request.method == 'POST':  # data sent by user
		form = FarmForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/list_farm/')
	else:  # display empty form
		form = FarmForm()
	return render(request, 'waissapp/add_farm.html', {'farm_form': form})

def list_farm(request):
	queryset = Farm.objects.all()

	context = {
		"farm_list":queryset,
	}
	return render(request, 'waissapp/list_farm.html', context)

def edit_farm(request, pk):
	para = Farm.objects.get(id=pk)
	form = FarmForm(instance=para)

	if request.method == 'POST':  # data sent by user
		form = FarmForm(request.POST, instance=para)
		if form.is_valid():
			form.save()  # this will save info to database
			return redirect('/list_farm/')

	context = {
		"farm_form":form,
		"item": para,
	}
	return render(request, 'waissapp/edit_farm.html', context)

def delete_farm(request, pk):
	para = Farm.objects.get(id=pk)
	if request.method == 'POST':
		para.delete()
		return redirect('/list_farm/')
	context = {
		"item":para	
	}
	return render(request, 'waissapp/delete_farm.html', context)
#END#FARM_PARAMETERS

#PERSONNEL_PARAMETERS
def new_personnel(request):
    if request.method == 'POST':  # data sent by user
        form = PersonnelForm(request.POST)
        if form.is_valid():
            form.save()  # this will save info to database
            return redirect('/new_crop/')
    else:  # display empty form
        form = PersonnelForm()

    return render(request, 'waissapp/new_personnel.html', {'personnel_form': form})

def add_personnel(request):
    if request.method == 'POST':  # data sent by user
        form = PersonnelForm(request.POST)
        if form.is_valid():
            form.save()  # this will save info to database
            return redirect('/list_personnel/')
    else:  # display empty form
        form = PersonnelForm()

    return render(request, 'waissapp/add_personnel.html', {'personnel_form': form})

def list_personnel(request):
	queryset = Personnel.objects.all()
	context = {
		"personnel_list":queryset,
	}
	return render(request, 'waissapp/list_personnel.html', context)

def edit_personnel(request, pk):
	para = Personnel.objects.get(id=pk)
	form = PersonnelForm(instance=para)

	if request.method == 'POST':  # data sent by user
		form = PersonnelForm(request.POST, instance=para)
		if form.is_valid():
			form.save()  # this will save info to database
			return redirect('/list_personnel/')

	context = {
		"personnel_form":form,
		"item": para,
	}
	return render(request, 'waissapp/edit_personnel.html', context)

def delete_personnel(request, pk):
	para = Personnel.objects.get(id=pk)
	if request.method == 'POST':
		para.delete()
		return redirect('/list_personnel/')
	context = {
		"item":para	
	}
	return render(request, 'waissapp/delete_personnel.html', context)
#END_OF_PERSONNEL_PARAMETERS

#IRRIGATION_SYSTEM_PARAMETERS
def new_irrigation(request):
    if request.method == 'POST':  # data sent by user
        form = IrrigationParametersForm(request.POST)
        if form.is_valid():
            form.save()  # this will save info to database
            return redirect('/new_irrigation/')
    else:  # display empty form
        form = IrrigationParametersForm()

    return render(request, 'waissapp/new_irrigation.html', {'irrigation_form': form})

def add_irrigation(request):
    if request.method == 'POST':  # data sent by user
        form = IrrigationParametersForm(request.POST)
        if form.is_valid():
            form.save()  # this will save info to database
            return redirect('/list_irrigation/')
    else:  # display empty form
        form = IrrigationParametersForm()

    return render(request, 'waissapp/add_irrigation.html', {'irrigation_form': form})

def list_irrigation(request):
	queryset = IrrigationParameters.objects.all()

	context = {
		"basin_list":queryset,
	}
	return render(request, 'waissapp/list_irrigation.html', context)

def edit_irrigation(request, pk):
	para = IrrigationParameters.objects.get(id=pk)
	form = IrrigationParametersForm(instance=para)

	if request.method == 'POST':  # data sent by user
		form = IrrigationParametersForm(request.POST, instance=para)
		if form.is_valid():
			form.save()  # this will save info to database
			return redirect('/list_irrigation/')

	context = {
		"irrigation_form":form,
		"item":para,
	}
	return render(request, 'waissapp/edit_irrigation.html', context)

def delete_irrigation(request, pk):
	para = IrrigationParameters.objects.get(id=pk)
	if request.method == 'POST':
		para.delete()
		return redirect('/list_irrigation/')
	context = {
		"item":para	
	}
	return render(request, 'waissapp/delete_irrigation.html', context)

def basin_calc(request):
	if request.method == 'POST':  # data sent by user
		form = FarmForm(request.POST)
		if form.is_valid():
			form.save()  # this will save info to database
	else:  # display empty form
		form = FarmForm()
	
	context = {
		"farm_form":form,
	}

	return render(request, 'waissapp/sys_basin.html', context)

#Messages
def list_msgs(request):
	receivedmsgs = ReceivedMsgs.objects.all()
	sentmsgs = SentMsgs.objects.all()
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
		"joinedlist": final_list,
		"form": form,
	}

	return render(request, 'waissapp/messages.html', context)

def delete_msgs(request, pk): #deleteconversation
	para2 = SentMsgs.objects.get(id=pk)

	if request.method == 'POST':
		para2.delete()
		return redirect('/messages/')
	context = {
		"item":para2,
	}
	return render(request, 'waissapp/delete_messages.html', context)

def view_msg(request, number):
	receivedmsgs = ReceivedMsgs.objects.all()
	sentmsgs = SentMsgs.objects.all()
	llist = sorted(chain(receivedmsgs, sentmsgs), key=attrgetter('timestamp'))
	joined_list = reversed(llist)

	number = number
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
		"number": number,
		"form": form,
		"joined_list": joined_list,
		"result": result,
	}
	return render(request, 'waissapp/view-conversation.html', context)

#MC Readings
def new_mc(request):
	DataFormSet = modelformset_factory(MoistureContent, exclude=(), extra=3)
	form = DataFormSet(queryset=MoistureContent.objects.none())
	if request.method == 'POST':
		form = DataFormSet(request.POST)
		if form.is_valid():
			form.save()
		return redirect('/dashboard/')
	else:
		form = DataFormSet(queryset=MoistureContent.objects.none())

	return render(request, 'waissapp/new_mc.html', {'form': form})

def add_mc(request):
	DataFormSet = modelformset_factory(MoistureContent, exclude=(), extra=3)
	form = DataFormSet(queryset=MoistureContent.objects.none())
	if request.method == 'POST':
		form = DataFormSet(request.POST)
		if form.is_valid():
			form.save()
		return redirect('/dashboard/')
	else:
		form = DataFormSet(queryset=MoistureContent.objects.none())

	return render(request, 'waissapp/add_mc.html', {'form': form})

def edit_mc(request, pk):
	para = MoistureContent.objects.get(id=pk)
	form = MCForm(instance=para)

	if request.method == 'POST':  # data sent by user
		form = MCForm(request.POST, instance=para)
		if form.is_valid():
			form.save()  # this will save info to database
			return redirect('/list_mc/')

	context = {
		"sensor_form":form,
		"item": para,
	}
	return render(request, 'waissapp/edit_mc.html', context)

def list_mc(request, name):
	data = Sensor.objects.all()
	name = name
	get_sensor = MoistureContent.objects.get(sensor=name)
	get_mc = get_sensor.data_set.all()

	context = {
		"list": get_mc,
	}
	return render(request, 'waissapp/list_mc.html', context)

def delete_mc(request, pk):
	para = MoistureContent.objects.get(id=pk)
	if request.method == 'POST':
		para.delete()
		return redirect('/list_mc/')
	context = {
		"item":para	
	}
	return render(request, 'waissapp/delete_mc.html', context)
