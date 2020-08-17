from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Personnel, Farm, FarmSummaries, SensorNumber, MoistureContent, FieldUnit, Soil, IntakeFamily, Crop, FieldUnitSettings, BasinAppEff, BasinComp, BorderComp, FurrowComp, DripComp, SprinklerComp, CalibrationConstant, BasinPara, FurrowPara, BorderPara, DripPara, SprinklerPara
from django.utils import timezone
from datetime import date
import json
from django.urls import reverse
from django import forms
from .forms import PersonnelForm, SoilForm, CalibForm, CropForm, FieldUnitSettingsForm, FarmForm, IntakeFamilyForm, FarmSummariesForm, FieldUnitForm, SensorForm, BasinForm, BorderForm, FurrowForm, SprinklerForm, DripForm, irrigtypeForm, BasinParaForm, FurrowParaForm, BorderParaForm, DripParaForm, SprinklerParaForm
from django.views.generic.edit import UpdateView
#from django.template import loader

#INTAKE_FAMILY_PARAMETERS
def add_intakefamily(request):
	if request.method == 'POST':  # data sent by user
		form = IntakeFamilyForm(request.POST)
		if form.is_valid():
			form.save()  # this will save info to database
			return HttpResponse('Intake family information added to database')
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

def index(request):
	return render(request, 'waissapp/index.html')

def about(request):
	return render(request, 'waissapp/about.html')

def charts(request):
	return render(request, 'waissapp/charts.html')

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

#CALIB_PARAMETERS
def add_calib(request):
	if request.method == 'POST':  # data sent by user
		form = CalibForm(request.POST)
		if form.is_valid():
			form.save()  # this will save info to database
			return HttpResponse('Calibration constants added to database')
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

#CROP_PARAMETERS
def add_crop(request):
	if request.method == 'POST':  # data sent by user
		form = CropForm(request.POST)
		if form.is_valid():
			form.save()  # this will save info to database
			return HttpResponse('Crop information and constants added to database')
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

#SOIL_PARAMETERS
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


def irrig_calculations(request):
	return render(request, 'waissapp/irrig-calculations.html')

#FIELDUNIT_PARAMETERS
def add_fieldunit(request):
    if request.method == 'POST':  # data sent by user
        form = FieldUnitForm(request.POST)
        if form.is_valid():
            form.save()  # this will save info to database
            return redirect('/list_fieldunit/')
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

#SENSOR_PARAMETERS
def add_sensor(request):
    if request.method == 'POST':  # data sent by user
        form = SensorForm(request.POST)
        if form.is_valid():
            form.save()  # this will save info to database
            return redirect('/sensorlist/')
    else:  # display empty form
        form = SensorForm()

    return render(request, 'waissapp/add_sensor.html', {'sensor_form': form})

def sensor_list_view(request):
	queryset = SensorNumber.objects.all()

	context = {
		"sensor_list":queryset,
	}
	return render(request, 'waissapp/list_sensor.html', context)

def editSensor(request, pk):
	para = SensorNumber.objects.get(id=pk)
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
	para = SensorNumber.objects.get(id=pk)
	if request.method == 'POST':
		para.delete()
		return redirect('/show-sensor-database/')
	context = {
		"item":para	
	}
	return render(request, 'waissapp/delete_sensor.html', context)

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

#SETTINGS_PARAMETERS
def add_settings(request):
	if request.method == 'POST':  # data sent by user
		form = FieldUnitSettingsForm(request.POST)
		if form.is_valid():
			form.save()  # this will save info to database
			return redirect('/show-settings-database/')
	else:  # display empty form
		form = FieldUnitSettingsForm()
	return render(request, 'waissapp/add_settings.html', {'settings_form': form})

def list_settings(request):
	queryset = FieldUnitSettings.objects.all()

	context = {
		"settings_list":queryset,
	}
	return render(request, 'waissapp/list_settings.html', context)

def editSettings(request, pk):
	para = FieldUnitSettings.objects.get(id=pk)
	form = FieldUnitSettingsForm(instance=para)

	if request.method == 'POST':  # data sent by user
		form = FieldUnitSettingsForm(request.POST, instance=para)
		if form.is_valid():
			form.save()  # this will save info to database
			return redirect('/show-settings-database/')

	context = {
		"settings_form":form,
	}
	return render(request, 'waissapp/edit_settings.html', context)

def deleteSettings(request, pk):
	para = FieldUnitSettings.objects.get(id=pk)
	if request.method == 'POST':
		para.delete()
		return redirect('/show-settings-database/')
	context = {
		"item":para	
	}
	return render(request, 'waissapp/delete_settings.html', context)

#FARM_PARAMETERS
def farm_account(request):

	if request.method == 'POST':  # data sent by user
		form = FarmForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/list_farm/')
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

#PERSONNEL_PARAMETERS
def add_personnel(request):
    if request.method == 'POST':  # data sent by user
        form = PersonnelForm(request.POST)
        if form.is_valid():
            form.save()  # this will save info to database
            return redirect('/list_personnel/')
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

def editDrip(request, pk):
	para = DripPara.objects.get(id=pk)
	form = DripParaForm(instance=para)

	if request.method == 'POST':  # data sent by user
		form = DripParaForm(request.POST, instance=para)
		if form.is_valid():
			form.save()  # this will save info to database
			return redirect('/show-drip-database/')

	context = {
		"drip_form":form,
	}
	return render(request, 'waissapp/edit_drip.html', context)

def deleteDrip(request, pk):
	para = DripPara.objects.get(id=pk)
	if request.method == 'POST':
		para.delete()
		return redirect('/show-drip-database/')
	context = {
		"item":para	
	}
	return render(request, 'waissapp/delete_drip.html', context)
	
def editSprinkler(request, pk):
	para = SprinklerPara.objects.get(id=pk)
	form = SprinklerParaForm(instance=para)

	if request.method == 'POST':  # data sent by user
		form = SprinklerParaForm(request.POST, instance=para)
		if form.is_valid():
			form.save()  # this will save info to database
			return redirect('/show-sprinkler-database/')

	context = {
		"sprinkler_form":form,
	}
	return render(request, 'waissapp/edit_sprinkler.html', context)

def deleteSprinkler(request, pk):
	para = SprinklerPara.objects.get(id=pk)
	if request.method == 'POST':
		para.delete()
		return redirect('/show-sprinkler-database/')
	context = {
		"item":para	
	}
	return render(request, 'waissapp/delete_sprinkler.html', context)

def editBorder(request, pk):
	para = BorderPara.objects.get(id=pk)
	form = BorderParaForm(instance=para)

	if request.method == 'POST':  # data sent by user
		form = BorderParaForm(request.POST, instance=para)
		if form.is_valid():
			form.save()  # this will save info to database
			return redirect('/show-border-database/')

	context = {
		"border_form":form,
	}
	return render(request, 'waissapp/edit_border.html', context)

def deleteBorder(request, pk):
	para = BorderPara.objects.get(id=pk)
	if request.method == 'POST':
		para.delete()
		return redirect('/show-border-database/')
	context = {
		"item":para	
	}
	return render(request, 'waissapp/delete_border.html', context)

def editFurrow(request, pk):
	para = FurrowPara.objects.get(id=pk)
	form = FurrowParaForm(instance=para)

	if request.method == 'POST':  # data sent by user
		form = FurrowParaForm(request.POST, instance=para)
		if form.is_valid():
			form.save()  # this will save info to database
			return redirect('/show-furrow-database/')

	context = {
		"furrow_form":form,
	}
	return render(request, 'waissapp/edit_furrow.html', context)

def deleteFurrow(request, pk):
	para = FurrowPara.objects.get(id=pk)
	if request.method == 'POST':
		para.delete()
		return redirect('/show-furrow-database/')
	context = {
		"item":para	
	}
	return render(request, 'waissapp/delete_furrow.html', context)

def editBasin(request, pk):
	para = BasinPara.objects.get(id=pk)
	form = BasinParaForm(instance=para)

	if request.method == 'POST':  # data sent by user
		form = BasinParaForm(request.POST, instance=para)
		if form.is_valid():
			form.save()  # this will save info to database
			return redirect('/show-basin-database/')

	context = {
		"basin_form":form,
	}
	return render(request, 'waissapp/edit_basin.html', context)

def deleteBasin(request, pk):
	para = BasinPara.objects.get(id=pk)
	if request.method == 'POST':
		para.delete()
		return redirect('/show-basin-database/')
	context = {
		"item":para	
	}
	return render(request, 'waissapp/delete_basin.html', context)