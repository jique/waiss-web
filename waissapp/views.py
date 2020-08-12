from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Personnel, Farm, FarmSummaries, SensorNumber, MoistureContent, FieldUnit, Soil, IntakeFamily, Crop, FieldUnitSettings, BasinAppEff, BasinComp, BorderComp, FurrowComp, DripComp, SprinklerComp, CalibrationConstant, BasinPara, FurrowPara, BorderPara, DripPara, SprinklerPara
from django.utils import timezone
from datetime import date
import json
from django.urls import reverse
from django import forms
from .forms import PersonnelForm, SoilForm, CalibForm, CropForm, FieldUnitSettingsForm, FarmForm, IntakeFamilyForm, FarmSummariesForm, FieldUnitForm, SensorForm, BasinForm, BorderForm, FurrowForm, SprinklerForm, DripForm, irrigtypeForm, BasinParaForm, FurrowParaForm, BorderParaForm, DripParaForm, SprinklerParaForm
#from django.template import loader


def add_soil(request):
    if request.method == 'POST':  # data sent by user
        form = SoilForm(request.POST)
        if form.is_valid():
            form.save()  # this will save info to database
            return HttpResponse('Soil information added to database')
    else:  # display empty form
        form = SoilForm()

    return render(request, 'waissapp/addsoil.html', {'soil_form': form})

def select_soil(request):
	list = Soil.objects.all()
	return render(request, 'waissapp/select_soil.html', {"Soil":list})

def add_intake(request):
	if request.method == 'POST':  # data sent by user
		form = IntakeFamilyForm(request.POST)
		if form.is_valid():
			form.save()  # this will save info to database
			return HttpResponse('Intake family information added to database')
	else:  # display empty form
		form = IntakeFamilyForm()
	return render(request, 'waissapp/intakefamily.html', {'intakefamily_form': form})

def select_intakefamily(request):
	list = IntakeFamily.objects.all()
	return render(request, 'waissapp/select_intakefamily.html', {"IntakeFamily":list})

def index(request):
	return render(request, 'waissapp/index.html')

def about(request):
	return render(request, 'waissapp/about.html')

def charts(request):
	return render(request, 'waissapp/charts.html')

#where to add new farm 
def farm_account(request):

	if request.method == 'POST':  # data sent by user
		form = FarmForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/farmlist/')
	else:  # display empty form
		form = FarmForm()
	return render(request, 'waissapp/farmaccount.html', {'farm_form': form})

#where to see farm database
def farm_list_view(request):
	queryset = Farm.objects.all()

	context = {
		"farm_list":queryset,
	}
	return render(request, 'waissapp/farmlist.html', context)
	#return render(request, 'waissapp/farmlist.html', locals())

#where to see summary of each farms
def farm_summaries(request):
	if request.method == 'POST':  # data sent by user
		form = FarmSummariesForm(request.POST)
		if form.is_valid():
			form.save()  # this will save info to database
			return HttpResponse('Added to database')
	else:  # display empty form
		form = FarmSummariesForm()
	return render(request, 'waissapp/farmsummaries.html', {'farmsummaries_form': form})

def calib(request):
	if request.method == 'POST':  # data sent by user
		form = CalibForm(request.POST)
		if form.is_valid():
			form.save()  # this will save info to database
			return HttpResponse('Calibration constants added to database')
	else:  # display empty form
		form = CalibForm()

	return render(request, 'waissapp/calib.html', {'calib_form': form})

def select_eqn(request):
	list = CalibrationConstant.objects.all()
	return render(request, 'waissapp/select_calibeqn.html', {"CalibrationConstant":list})

def crop_info(request):
	if request.method == 'POST':  # data sent by user
		form = CropForm(request.POST)
		if form.is_valid():
			form.save()  # this will save info to database
			return HttpResponse('Crop information and constants added to database')
	else:  # display empty form
		form = CropForm()
	return render(request, 'waissapp/cropinfo.html', {'crop_form': form})

def select_crop(request):
	list = Crop.objects.all()
	return render(request, 'waissapp/select_crop.html', {"Crop":list})

def soil_info(request):
	return render(request, 'waissapp/soilinfo.html')

def irrig_calculations(request):
	return render(request, 'waissapp/irrig-calculations.html')

#where to see field unit database
def fieldunit_list_view(request):
	queryset = FieldUnit.objects.all()

	context = {
		"fieldunit_list":queryset,
	}
	return render(request, 'waissapp/fieldunitslist.html', context)

#where to add new field unit
def add_fieldunit(request):
    if request.method == 'POST':  # data sent by user
        form = FieldUnitForm(request.POST)
        if form.is_valid():
            form.save()  # this will save info to database
            return redirect('/fieldunitslist/')
    else:  # display empty form
        form = FieldUnitForm()

    return render(request, 'waissapp/addfieldunit.html', {'fieldunit_form': form})

def add_sensor(request):
    if request.method == 'POST':  # data sent by user
        form = SensorForm(request.POST)
        if form.is_valid():
            form.save()  # this will save info to database
            return redirect('/sensorlist/')
    else:  # display empty form
        form = SensorForm()

    return render(request, 'waissapp/addsensor.html', {'sensor_form': form})

def sensor_list_view(request):
	queryset = SensorNumber.objects.all()

	context = {
		"sensor_list":queryset,
	}
	return render(request, 'waissapp/sensorlist.html', context)

def field_unit_settings(request):
	if request.method == 'POST':  # data sent by user
		form = FieldUnitSettingsForm(request.POST)
		if form.is_valid():
			form.save()  # this will save info to database
			return HttpResponse('Crop information and constants added to database')
	else:  # display empty form
		form = FieldUnitSettingsForm()
	return render(request, 'waissapp/fieldunitsettings.html', {'fieldunitsettings_form': form})

def add_basin(request):
    if request.method == 'POST':  # data sent by user
        form = BasinParaForm(request.POST)
        if form.is_valid():
            form.save()  # this will save info to database
            return redirect('/show-basin-database/')
    else:  # display empty form
        form = BasinParaForm()

    return render(request, 'waissapp/addbasin.html', {'basin_form': form})

def add_border(request):
    if request.method == 'POST':  # data sent by user
        form = BorderParaForm(request.POST)
        if form.is_valid():
            form.save()  # this will save info to database
            return redirect('/show-border-database/')
    else:  # display empty form
        form = BorderParaForm()

    return render(request, 'waissapp/addborder.html', {'border_form': form})

def add_furrow(request):
    if request.method == 'POST':  # data sent by user
        form = FurrowParaForm(request.POST)
        if form.is_valid():
            form.save()  # this will save info to database
            return redirect('/show-furrow-database/')
    else:  # display empty form
        form = FurrowParaForm()

    return render(request, 'waissapp/addfurrow.html', {'furrow_form': form})

def add_sprinkler(request):
    if request.method == 'POST':  # data sent by user
        form = SprinklerParaForm(request.POST)
        if form.is_valid():
            form.save()  # this will save info to database
            return redirect('/show-sprinkler-database/')
    else:  # display empty form
        form = SprinklerParaForm()

    return render(request, 'waissapp/addsprinkler.html', {'sprinkler_form': form})

def add_drip(request):
    if request.method == 'POST':  # data sent by user
        form = DripParaForm(request.POST)
        if form.is_valid():
            form.save()  # this will save info to database
            return redirect('/show-drip-database/')
    else:  # display empty form
        form = DripParaForm()

    return render(request, 'waissapp/adddrip.html', {'drip_form': form})

def choose_irrig(request):
	if request.method == 'POST':
		form = irrigtypeForm(request.POST)
		if form.is_valid():
			irrig_type = form.cleaned_data.get("farm_irrigation")
			if irrig_type == "BASIN":
				return redirect('/add-basin-system/')
			elif irrig_type == "BORDER":
				return redirect('/add-border-system/')
			elif irrig_type == "FURROW":
				return redirect('/add-furrow-system/')
			elif irrig_type == "DRIP":
				return redirect('/add-drip-system/')
			elif irrig_type == "SPRINKLER":
				return redirect('/add-sprinkler-system/')
	else:  # display empty form
		form = irrigtypeForm()
	return render(request, 'waissapp/irriginfo.html', {'irrig_form': form})

def choose_irrig_database(request):
	if request.method == 'POST':
		form = irrigtypeForm(request.POST)
		if form.is_valid():
			irrig_type = form.cleaned_data.get("farm_irrigation")
			if irrig_type == "BASIN":
				return redirect('/show-basin-database/')
			elif irrig_type == "BORDER":
				return redirect('/show-border-database/')
			elif irrig_type == "FURROW":
				return redirect('/show-furrow-database/')
			elif irrig_type == "DRIP":
				return redirect('/show-drip-database/')
			elif irrig_type == "SPRINKLER":
				return redirect('/show-sprinkler-database/')
	else:  # display empty form
		form = irrigtypeForm()
	return render(request, 'waissapp/choose-irrigation-system-type.html', {'irrig_form': form})

def add_personnel(request):
    if request.method == 'POST':  # data sent by user
        form = PersonnelForm(request.POST)
        if form.is_valid():
            form.save()  # this will save info to database
            return redirect('/personnellist/')
    else:  # display empty form
        form = PersonnelForm()

    return render(request, 'waissapp/advisorysettings.html', {'personnel_form': form})

def personnel_list_view(request):
	queryset = Personnel.objects.all()

	context = {
		"personnel_list":queryset,
	}
	return render(request, 'waissapp/personnellist.html', context)

def basin_list(request):
	queryset = BasinPara.objects.all()

	context = {
		"basin_list":queryset,
	}
	return render(request, 'waissapp/listbasin.html', context)

def border_list(request):
	queryset = BorderPara.objects.all()

	context = {
		"border_list":queryset,
	}
	return render(request, 'waissapp/listborder.html', context)

def furrow_list(request):
	queryset = FurrowPara.objects.all()

	context = {
		"furrow_list":queryset,
	}
	return render(request, 'waissapp/listfurrow.html', context)

def sprinkler_list(request):
	queryset = SprinklerPara.objects.all()

	context = {
		"sprinkler_list":queryset,
	}
	return render(request, 'waissapp/listsprinkler.html', context)

def drip_list(request):
	queryset = DripPara.objects.all()

	context = {
		"drip_list":queryset,
	}
	return render(request, 'waissapp/listdrip.html', context)