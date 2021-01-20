from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import SentMsgs, ReceivedMsgs, Personnel, Farm, Sensor, MoistureContent, FieldUnit, Soil, IntakeFamily, Crop, CalibrationConstant, IrrigationParameters
from django.utils import timezone
import datetime
from datetime import date, datetime
import json
from django.urls import reverse
from django import forms
from django.template import RequestContext
from django.forms import modelformset_factory
from .forms import SentMsgsForm, PersonnelForm, SoilForm, CalibForm, CropForm, FarmForm, IntakeFamilyForm, FieldUnitForm, IrrigationParametersForm, SensorForm, MCForm
from django.db import transaction, IntegrityError
from itertools import chain
from operator import attrgetter

def index(request):
	if request.method == 'POST':  # data sent by user
		form = FarmForm(request.POST)
		if form.is_valid():
			form.save()  # this will save info to database
	else:  # display empty form
		form = FarmForm()
	
	context = {
		"farm_form":form,
	}
	return render(request, 'waissapp/index.html', context)

def load_page(request):
	return render(request, 'waissapp/load_page.html')

def computation_option(request):
	return render(request, 'waissapp/simp_advanced.html')

def irrig_type(request):
	return render(request, 'waissapp/irrig_type.html')

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

#INTAKE_FAMILY_PARAMETERS
def add_intakefamily(request):
	if request.method == 'POST':  # data sent by user
		form = IntakeFamilyForm(request.POST)
		if form.is_valid():
			form.save()  # this will save info to database
			return redirect('/show-intakefamily-database/')
	else:  # display empty form
		form = IntakeFamilyForm()
	return render(request, 'waissapp/add_intakefamily.html', {'intakefamily_form': form})

def list_intakefamily(request):
	queryset = IntakeFamily.objects.all()
	context = {
		"intakefamily_list":queryset,
	}
	return render(request, 'waissapp/list_intakefamily.html', context)

def editIntakeFamily(request, pk):
	para = IntakeFamily.objects.get(id=pk)
	form = IntakeFamilyForm(instance=para)

	if request.method == 'POST':  # data sent by user
		form = IntakeFamilyForm(request.POST, instance=para)
		if form.is_valid():
			form.save()  # this will save info to database
			return redirect('/show-intakefamily-database/')

	context = {
		"intakefamily_form":form,
		"item":para,
	}
	return render(request, 'waissapp/edit_intakefamily.html', context)

def deleteIntakeFamily(request, pk):
	para = IntakeFamily.objects.get(id=pk)
	if request.method == 'POST':
		para.delete()
		return redirect('/show-intakefamily-database/')
	context = {
		"item":para	
	}
	return render(request, 'waissapp/delete_intakefamily.html', context)
#END#INTAKE_FAMILY_PARAMETERS

#CALIB_PARAMETERS
def newcalib(request):
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

def editCalib(request, pk):
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

def deleteCalib(request, pk):
	para = CalibrationConstant.objects.get(id=pk)
	if request.method == 'POST':
		para.delete()
		return redirect('/show-calib-database/')
	context = {
		"item":para	
	}
	return render(request, 'waissapp/delete_calib.html', context)
#END#CALIB_PARAMETERS

#CROP_PARAMETERS
def newcrop(request):
	if request.method == 'POST':  # data sent by user
		form = CropForm(request.POST)
		if form.is_valid():
			form.save()  # this will save info to database
			return redirect('/newsoil/')
	else:  # display empty form
		form = CropForm()
	return render(request, 'waissapp/new_crop.html', {'crop_form': form})

def add_crop(request):
	if request.method == 'POST':  # data sent by user
		form = CropForm(request.POST)
		if form.is_valid():
			form.save()  # this will save info to database
			next = request.POST.get('next', '/')
			return HttpResponseRedirect(next)
	else:  # display empty form
		form = CropForm()
	return render(request, 'waissapp/add_crop.html', {'crop_form': form})

def list_crop(request):
	queryset = Crop.objects.all()
	context = {
		"crop_list":queryset,
	}
	return render(request, 'waissapp/list_crop.html', context)

def editCrop(request, pk):
	para = Crop.objects.get(id=pk)
	form = CropForm(instance=para)

	if request.method == 'POST':  # data sent by user
		form = CropForm(request.POST, instance=para)
		if form.is_valid():
			form.save()  # this will save info to database
			return redirect('/show-crop-database/')

	context = {
		"crop_form":form,
	}
	return render(request, 'waissapp/edit_crop.html', context)

def deleteCrop(request, pk):
	para = Crop.objects.get(id=pk)
	if request.method == 'POST':
		para.delete()
		return redirect('/show-crop-database/')
	context = {
		"item":para	
	}
	return render(request, 'waissapp/delete_crop.html', context)
#END#CROP_PARAMETERS

#SOIL_PARAMETERS
def newsoil(request):
    if request.method == 'POST':  # data sent by user
        form = SoilForm(request.POST)
        if form.is_valid():
            form.save()  # this will save info to database
            return redirect('/newfieldunit/')
    else:  # display empty form
        form = SoilForm()

    return render(request, 'waissapp/new_soil.html', {'soil_form': form})

def add_soil(request):
    if request.method == 'POST':  # data sent by user
        form = SoilForm(request.POST)
        if form.is_valid():
            form.save()  # this will save info to database
            return redirect('/show-soil-database/')
    else:  # display empty form
        form = SoilForm()

    return render(request, 'waissapp/addsoil.html', {'soil_form': form})

def list_soil(request):
	queryset = Soil.objects.all()

	context = {
		"soil_list":queryset,
	}
	return render(request, 'waissapp/list_soil.html', context)

def editSoil(request, pk):
	para = Soil.objects.get(id=pk)
	form = SoilForm(instance=para)

	if request.method == 'POST':  # data sent by user
		form = SoilForm(request.POST, instance=para)
		if form.is_valid():
			form.save()  # this will save info to database
			return redirect('/show-soil-database/')

	context = {
		"soil_form":form,
	}
	return render(request, 'waissapp/edit_soil.html', context)

def deleteSoil(request, pk):
	para = Soil.objects.get(id=pk)
	if request.method == 'POST':
		para.delete()
		return redirect('/show-soil-database/')
	context = {
		"item":para	
	}
	return render(request, 'waissapp/delete_soil.html', context)
#END#SOIL_PARAMETERS

#FIELDUNIT_PARAMETERS
def newfieldunit(request):
    if request.method == 'POST':  # data sent by user
        form = FieldUnitForm(request.POST)
        if form.is_valid():
            form.save()  # this will save info to database
            return redirect('/newsensor/')
    else:  # display empty form
        form = FieldUnitForm()

    return render(request, 'waissapp/new_fieldunit.html', {'fieldunit_form': form})

def add_fieldunit(request):
    if request.method == 'POST':  # data sent by user
        form = FieldUnitForm(request.POST)
        if form.is_valid():
            form.save()  # this will save info to database
            return redirect('/show-fieldunit-database/')
    else:  # display empty form
        form = FieldUnitForm()

    return render(request, 'waissapp/add_fieldunit.html', {'fieldunit_form': form})

def fieldunit_list_view(request):
	queryset = FieldUnit.objects.all()

	context = {
		"fieldunit_list":queryset,
	}
	return render(request, 'waissapp/list_fieldunit.html', context)

def editFieldUnit(request, pk):
	para = FieldUnit.objects.get(id=pk)
	form = FieldUnitForm(instance=para)

	if request.method == 'POST':  # data sent by user
		form = FieldUnitForm(request.POST, instance=para)
		if form.is_valid():
			form.save()  # this will save info to database
			return redirect('/show-fieldunit-database/')

	context = {
		"fieldunit_form":form,
	}
	return render(request, 'waissapp/edit_fieldunit.html', context)

def deleteFieldUnit(request, pk):
	para = FieldUnit.objects.get(id=pk)
	if request.method == 'POST':
		para.delete()
		return redirect('/show-fieldunit-database/')
	context = {
		"item":para	
	}
	return render(request, 'waissapp/delete_fieldunit.html', context)
#END#FIELDUNIT_PARAMETERS

#SENSOR_PARAMETERS
def create_sensor_model_form(request):
	SensorFormSet = modelformset_factory(Sensor, exclude=(), extra=3)
	form = SensorFormSet(queryset=Sensor.objects.none())
	if request.method == 'POST':
		form = SensorFormSet(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/newdata/')
	else:  # display empty form
		form = SensorFormSet(queryset=Sensor.objects.none())

	return render(request, 'waissapp/new_sensor.html', {'form':form})

def newdata(request):
	DataFormSet = modelformset_factory(MoistureContent, exclude=(), extra=3)
	form = DataFormSet(queryset=MoistureContent.objects.none())
	if request.method == 'POST':
		form = DataFormSet(request.POST)
		if form.is_valid():
			form.save()
		return redirect('/dashboard/')
	else:
		form = DataFormSet(queryset=MoistureContent.objects.none())

	return render(request, 'waissapp/new_data.html', {'form': form})

def add_data(request):
	DataFormSet = modelformset_factory(MoistureContent, exclude=(), extra=3)
	form = DataFormSet(queryset=MoistureContent.objects.none())
	if request.method == 'POST':
		form = DataFormSet(request.POST)
		if form.is_valid():
			form.save()
		return redirect('/dashboard/')
	else:
		form = DataFormSet(queryset=MoistureContent.objects.none())

	return render(request, 'waissapp/add_data.html', {'form': form})

def add_sensor(request):
	SensorFormSet = modelformset_factory(Sensor, exclude=(), extra=3)
	form = SensorFormSet(queryset=Sensor.objects.none())
	if request.method == 'POST':
		form = SensorFormSet(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/newdata/')
	else:  # display empty form
		form = SensorFormSet(queryset=Sensor.objects.none())
	
	return render(request, 'waissapp/add_sensor.html', {'sensor_form': form})

def sensor_list_view(request):
	queryset = Sensor.objects.all()

	context = {
		"sensor_list":queryset,
	}
	return render(request, 'waissapp/list_sensor.html', context)

def editSensor(request, pk):
	para = Sensor.objects.get(id=pk)
	form = SensorForm(instance=para)

	if request.method == 'POST':  # data sent by user
		form = SensorForm(request.POST, instance=para)
		if form.is_valid():
			form.save()  # this will save info to database
			return redirect('/show-sensor-database/')

	context = {
		"sensor_form":form,
	}
	return render(request, 'waissapp/edit_sensor.html', context)

def deleteSensor(request, pk):
	para = Sensor.objects.get(id=pk)
	if request.method == 'POST':
		para.delete()
		return redirect('/show-sensor-database/')
	context = {
		"item":para	
	}
	return render(request, 'waissapp/delete_sensor.html', context)
#END#SENSOR_PARAMETERS

#FARM_PARAMETERS
def newintakefamily(request):
	if request.method == 'POST':  # data sent by user
		form = IntakeFamilyForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/choose-irrigation/')
	else:  # display empty form
		form = IntakeFamilyForm()
	return render(request, 'waissapp/new_intakefamily.html', {'intakefamily_form': form})

def farm_account(request):
	if request.method == 'POST':  # data sent by user
		form = FarmForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/show-farm-database/')
	else:  # display empty form
		form = FarmForm()
	return render(request, 'waissapp/add_farm.html', {'farm_form': form})

def farm_list_view(request):
	queryset = Farm.objects.all()

	context = {
		"farm_list":queryset,
	}
	return render(request, 'waissapp/list_farm.html', context)

def editFarm(request, pk):
	para = Farm.objects.get(id=pk)
	form = FarmForm(instance=para)

	if request.method == 'POST':  # data sent by user
		form = FarmForm(request.POST, instance=para)
		if form.is_valid():
			form.save()  # this will save info to database
			return redirect('/show-farm-database/')

	context = {
		"farm_form":form,
	}
	return render(request, 'waissapp/edit_farm.html', context)

def deleteFarm(request, pk):
	para = Farm.objects.get(id=pk)
	if request.method == 'POST':
		para.delete()
		return redirect('/show-farm-database/')
	context = {
		"item":para	
	}
	return render(request, 'waissapp/delete_farm.html', context)
#END#FARM_PARAMETERS

#PERSONNEL_PARAMETERS
def newpersonnel(request):
    if request.method == 'POST':  # data sent by user
        form = PersonnelForm(request.POST)
        if form.is_valid():
            form.save()  # this will save info to database
            return redirect('/newcrop/')
    else:  # display empty form
        form = PersonnelForm()

    return render(request, 'waissapp/new_personnel.html', {'personnel_form': form})

def add_personnel(request):
    if request.method == 'POST':  # data sent by user
        form = PersonnelForm(request.POST)
        if form.is_valid():
            form.save()  # this will save info to database
            return redirect('/show-personnel-database/')
    else:  # display empty form
        form = PersonnelForm()

    return render(request, 'waissapp/add_personnel.html', {'personnel_form': form})

def personnel_list_view(request):
	queryset = Personnel.objects.all()

	context = {
		"personnel_list":queryset,
	}
	return render(request, 'waissapp/list_personnel.html', context)

def editPersonnel(request, pk):
	para = Personnel.objects.get(id=pk)
	form = PersonnelForm(instance=para)

	if request.method == 'POST':  # data sent by user
		form = PersonnelForm(request.POST, instance=para)
		if form.is_valid():
			form.save()  # this will save info to database
			return redirect('/show-personnel-database/')

	context = {
		"personnel_form":form,
	}
	return render(request, 'waissapp/edit_personnel.html', context)

def deletePersonnel(request, pk):
	para = Personnel.objects.get(id=pk)
	if request.method == 'POST':
		para.delete()
		return redirect('/show-personnel-database/')
	context = {
		"item":para	
	}
	return render(request, 'waissapp/delete_personnel.html', context)
#END_OF_PERSONNEL_PARAMETERS

#IRRIGATION_SYSTEM

#BASIN_IRRIGATION_SYSTEM_PARAMETERS
def newbasin(request):
    if request.method == 'POST':  # data sent by user
        form = IrrigationParametersForm(request.POST)
        if form.is_valid():
            form.save()  # this will save info to database
            return redirect('/add-farm/')
    else:  # display empty form
        form = IrrigationParametersForm()

    return render(request, 'waissapp/new_basin.html', {'irrigation_form': form})

def addbasin(request):
    if request.method == 'POST':  # data sent by user
        form = IrrigationParametersForm(request.POST)
        if form.is_valid():
            form.save()  # this will save info to database
            return redirect('/add-farm/')
    else:  # display empty form
        form = IrrigationParametersForm()

    return render(request, 'waissapp/add_basin.html', {'irrigation_form': form})

def basin_list(request):
	queryset = IrrigationParameters.objects.all()

	context = {
		"basin_list":queryset,
	}
	return render(request, 'waissapp/listbasin.html', context)

def editBasin(request, pk):
	para = IrrigationParameters.objects.get(id=pk)
	form = IrrigationParametersForm(instance=para)

	if request.method == 'POST':  # data sent by user
		form = IrrigationParametersForm(request.POST, instance=para)
		if form.is_valid():
			form.save()  # this will save info to database
			return redirect('/show-basin-database/')

	context = {
		"irrigation_form":form,
	}
	return render(request, 'waissapp/edit_basin.html', context)

def deleteIrrigation(request, pk):
	para = IrrigationParameters.objects.get(id=pk)
	if request.method == 'POST':
		para.delete()
		return redirect('/show-basin-database/')
	context = {
		"item":para	
	}
	return render(request, 'waissapp/delete_irrigation.html', context)

#BORDER_IRRIGATION
def newborder(request):
    if request.method == 'POST':  # data sent by user
        form = IrrigationParametersForm(request.POST)
        if form.is_valid():
            form.save()  # this will save info to database
            return redirect('/add-farm/')
    else:  # display empty form
        form = IrrigationParametersForm()

    return render(request, 'waissapp/new_border.html', {'irrigation_form': form})

def add_border(request):
    if request.method == 'POST':  # data sent by user
        form = IrrigationParametersForm(request.POST)
        if form.is_valid():
            form.save()  # this will save info to database
            return redirect('/add-farm/')
    else:  # display empty form
        form = IrrigationParametersForm()

    return render(request, 'waissapp/add_border.html', {'irrigation_form': form})

def border_list(request):
	queryset = IrrigationParameters.objects.all()

	context = {
		"border_list":queryset,
	}
	return render(request, 'waissapp/listborder.html', context)

def editBorder(request, pk):
	para = IrrigationParameters.objects.get(id=pk)
	form = IrrigationParametersForm(instance=para)

	if request.method == 'POST':  # data sent by user
		form = IrrigationParametersForm(request.POST, instance=para)
		if form.is_valid():
			form.save()  # this will save info to database
			return redirect('/show-border-database/')

	context = {
		"irrigation_form":form,
	}
	return render(request, 'waissapp/edit_border.html', context)

#END_OF_BORDER_IRRIGATION

#FURROW_IRRIGATION
def newfurrow(request):
    if request.method == 'POST':  # data sent by user
        form = IrrigationParametersForm(request.POST)
        if form.is_valid():
            form.save()  # this will save info to database
            return redirect('/calculate-furrow-system/')
    else:  # display empty form
        form = IrrigationParametersForm()

    return render(request, 'waissapp/new_furrow.html', {'irrigation_form': form})

def add_furrow(request):
    if request.method == 'POST':  # data sent by user
        form = IrrigationParametersForm(request.POST)
        if form.is_valid():
            form.save()  # this will save info to database
            return redirect('/show-furrow-database/')
    else:  # display empty form
        form = IrrigationParametersForm()

    return render(request, 'waissapp/add_furrow.html', {'irrigation_form': form})

def furrow_list(request):
	queryset = IrrigationParameters.objects.all()

	context = {
		"furrow_list":queryset,
	}
	return render(request, 'waissapp/listfurrow.html', context)

def editFurrow(request, pk):
	para = IrrigationParameters.objects.get(id=pk)
	form = IrrigationParametersForm(instance=para)

	if request.method == 'POST':  # data sent by user
		form = IrrigationParametersForm(request.POST, instance=para)
		if form.is_valid():
			form.save()  # this will save info to database
			return redirect('/show-furrow-database/')

	context = {
		"irrigation_form":form,
	}
	return render(request, 'waissapp/edit_furrow.html', context)
#END_OF_FURROW_IRRIGATION

#DRIP_IRRIGATION
def newdrip(request):
    if request.method == 'POST':  # data sent by user
        form = IrrigationParametersForm(request.POST)
        if form.is_valid():
            form.save()  # this will save info to database
            return redirect('/calculate-drip-system/')
    else:  # display empty form
        form = IrrigationParametersForm()

    return render(request, 'waissapp/new_drip.html', {'irrigation_form': form})

def add_drip(request):
    if request.method == 'POST':  # data sent by user
        form = IrrigationParametersForm(request.POST)
        if form.is_valid():
            form.save()  # this will save info to database
            return redirect('/show-drip-database/')
    else:  # display empty form
        form = IrrigationParametersForm()

    return render(request, 'waissapp/add_drip.html', {'irrigation_form': form})

def drip_list(request):
	queryset = IrrigationParameters.objects.all()

	context = {
		"drip_list":queryset,
	}
	return render(request, 'waissapp/listdrip.html', context)

def editDrip(request, pk):
	para = IrrigationParameters.objects.get(id=pk)
	form = IrrigationParametersForm(instance=para)

	if request.method == 'POST':  # data sent by user
		form = IrrigationParametersForm(request.POST, instance=para)
		if form.is_valid():
			form.save()  # this will save info to database
			return redirect('/show-drip-database/')

	context = {
		"irrigation_form":form,
	}
	return render(request, 'waissapp/edit_drip.html', context)

#END_OF_DRIP_IRRIGATION

#SPRINKLER_IRRIGATION
def newsprinkler(request):
    if request.method == 'POST':  # data sent by user
        form = IrrigationParametersForm(request.POST)
        if form.is_valid():
            form.save()  # this will save info to database
            return redirect('/calculate-sprinkler-system/')
    else:  # display empty form
        form = IrrigationParametersForm()

    return render(request, 'waissapp/new_sprinkler.html', {'irrigation_form': form})

def add_sprinkler(request):
    if request.method == 'POST':  # data sent by user
        form = IrrigationParametersForm(request.POST)
        if form.is_valid():
            form.save()  # this will save info to database
            return redirect('/show-sprinkler-database/')
    else:  # display empty form
        form = IrrigationParametersForm()

    return render(request, 'waissapp/add_sprinkler.html', {'irrigation_form': form})

def sprinkler_list(request):
	queryset = IrrigationParameters.objects.all()

	context = {
		"sprinkler_list":queryset,
	}
	return render(request, 'waissapp/listsprinkler.html', context)

def editSprinkler(request, pk):
	para = IrrigationParameters.objects.get(id=pk)
	form = IrrigationParametersForm(instance=para)

	if request.method == 'POST':  # data sent by user
		form = IrrigationParametersForm(request.POST, instance=para)
		if form.is_valid():
			form.save()  # this will save info to database
			return redirect('/show-sprinkler-database/')

	context = {
		"irrigation_form":form,
	}
	return render(request, 'waissapp/edit_sprinkler.html', context)

#END_OF_SPRINKLER_IRRIGATION

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

def send_message(request):
	if request.method == 'POST':  # data sent by user
		form = SentMsgsForm(request.POST)
		if form.is_valid():
			form.save()  # this will save info to database
			return redirect('/messages/')
	else:  # display empty form
		form = SentMsgsForm()
	return render(request, 'waissapp/send-message.html', {'sendmsg_form': form})

def list_msgs(request):
	receivedmsgs = ReceivedMsgs.objects.all()
	sentmsgs = SentMsgs.objects.all()
	llist = sorted(chain(receivedmsgs, sentmsgs), key=attrgetter('timestamp'))
	final_list = reversed(llist)

	context = {
		"joinedlist": final_list
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
	return render(request, 'waissapp/messages_delete.html', context)

def view_msg(request, number):
	receivedmsgs = ReceivedMsgs.objects.all()
	sentmsgs = SentMsgs.objects.all()

	number = number 
	cel_number = Personnel.objects.get(number=number)
	received = cel_number.receivedmsgs_set.all()
	sent = cel_number.sentmsgs_set.all()

	llist = sorted(chain(receivedmsgs, sentmsgs), key=attrgetter('timestamp'))
	final_list = reversed(llist)
	result = sorted(chain(received,sent), key=attrgetter('timestamp'))

	if request.method == 'POST':  # data sent by user
		form = SentMsgsForm(request.POST)
		if form.is_valid():
			form.save()  # this will save info to database
			return redirect('/view-conversation/')
	else:  # display empty form
		form = SentMsgsForm()

	context = {
		"number": number,
		"cel_number": cel_number,
		"sent": sent,
		"received": received,
		"form": form,
		"final_list": final_list,
		"result": result
	}
	return render(request, 'waissapp/view-conversation.html', context)

def newfarm(request):
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

def newirrigation(request):
	form = IrrigationParametersForm(request.POST)
	if request.method == 'POST':  # data sent by user
		if form.is_valid():
			form.save()  # this will save info to database
			request.POST.get('name')
			return redirect('/add-farm/')
		else:  # display empty form
			form = IrrigationParametersForm()

	return render(request, 'waissapp/new_irrigation.html', {'irrigation_form': form})