from django.shortcuts import render, redirect
from .models import SentMsgs, ReceivedMsgs, Personnel, Farm, Sensor, MoistureContent, FieldUnit, Soil, Crop, CalibrationConstant, IrrigationParameters, WAISSystems, PercentShaded, Rainfall
from django.utils import timezone
import datetime
from datetime import date, datetime
from django import forms
from django.forms import modelformset_factory
from .forms import SentMsgsForm, PersonnelForm, SoilForm, CalibForm, CropForm, FarmForm, FieldUnitForm, IrrigationParametersForm, SensorForm, MCForm, WAISSystemsForm
from itertools import chain
from operator import attrgetter
import math

def index(request):
	receivedmsgs = ReceivedMsgs.objects.all() #for message center
	sentmsgs = SentMsgs.objects.all()
	llist = sorted(chain(receivedmsgs, sentmsgs), key=attrgetter('timestamp'))
	reversed_list =reversed(llist)

	form = WAISSystems.objects.all() # for_dropdown_select_options

	if request.method == 'POST':  # for sending the selected WAISS_system by the user
		selected_system = request.POST['selected_system']
		selected_system = WAISSystems.objects.get(name=selected_system)
	else:
		selected_system = WAISSystems.objects.latest() # to do: change to last selected

	crop = selected_system.crop # getting crop variables
	crop_transplanted = crop.date_transplanted
	crop_growingperiod = (crop.growingperiod)
	crop_mad = float(crop.mad)

	soil = selected_system.soil  # getting soil variables
	soil_fc = float(soil.fc)/100
	soil_pwp = float(soil.pwp)/100

	irrigation = selected_system.irrigation  # getting irrigation variables
	irrigation_type = irrigation.irrigation_system_type
	irrigation_q = irrigation.discharge

	calib = selected_system.calib  # getting calibration variables
	calib_eqn = calib.calib_equation
	calib_coeff_a = float(calib.coeff_a)
	calib_coeff_b = float(calib.coeff_b)
	calib_coeff_c = float(calib.coeff_c)
	calib_coeff_d = float(calib.coeff_d)
	calib_coeff_m = float(calib.coeff_m)

	fieldunit = selected_system.fieldunit  # getting fieldunit variables
	sensor_1 = Sensor.objects.all().filter(fieldunit=fieldunit)[:1]  # getting sensors
	sensor_2 = Sensor.objects.all().filter(fieldunit=fieldunit)[1:2]
	sensor_3 = Sensor.objects.all().filter(fieldunit=fieldunit)[2:3]

	mc_1 = MoistureContent.objects.all().filter(sensor=sensor_1) # getting mc analog readings
	mc_2 = MoistureContent.objects.all().filter(sensor=sensor_2)
	mc_3 = MoistureContent.objects.all().filter(sensor=sensor_3)

	mc_1_sorted = sorted(mc_1, key=attrgetter('timestamp')) # sorting mc analog readings based on inputted datetime
	mc_2_sorted = sorted(mc_2, key=attrgetter('timestamp'))
	mc_3_sorted = sorted(mc_3, key=attrgetter('timestamp'))

	mc_list = list(mc_1_sorted)	# for inserting rainfall data on the graph
	rainfall = Rainfall.objects.all().filter(fieldunit=fieldunit)
	sorted_rainfall = sorted(rainfall, key=attrgetter('timestamp'))

	rainfall_collection = []

	for p in sorted_rainfall: # for creating list that has the same index of the mc data
		p_time = p.timestamp
		p_amount = float(p.amount)
		j = len(rainfall_collection)
		for i, m in enumerate(mc_list, start=1):
			m_time = m.timestamp
			if p_time == m_time:
				z = i-j-1
				for x in range(0, z):
					rainfall_collection.append(0.0)
				rainfall_collection.append(p_amount)
				break

	MC_TO_IRRIGATE = round((((soil_fc - soil_pwp)* crop_mad) + soil_pwp)*100, 2) # mc to initiate irrigation advisory
	
	mci_1 = float(mc_1.latest().mc_data)
	mci_2 = float(mc_2.latest().mc_data)
	mci_3 = float(mc_3.latest().mc_data)
	
	def calculateMC(mc_value): # Convert analog reading to MCv
		float(mc_value)
		if calib_eqn == "linear":
			mc_return = calib_coeff_a * (mc_value)+ calib_coeff_b
		if calib_eqn == "quadratic":
			mc_return = calib_coeff_a * (mc_value)**2 + calib_coeff_b*(mc_value) + calib_coeff_c
		if calib_eqn == "exponential":
			mc_return = calib_coeff_a*math.exp(calib_coeff_b*mc_value)
		if calib_eqn == "logarithmic":
			mc_return = calib_coeff_a*math.log(mc_value) + calib_coeff_b
		if calib_eqn == "symmetrical sigmoidal":
			mc_return = calib_coeff_d + (calib_coeff_a - calib_coeff_d)/(1.0 + (mc_value/calib_coeff_c)**calib_coeff_b)
		if calib_eqn == "asymmetrical sigmoidal":
			mc_return = calib_coeff_d + (calib_coeff_a - calib_coeff_d)/(1.0 + (mc_value/calib_coeff_c)**calib_coeff_b)**calib_coeff_m
		return round(mc_return, 2)

	mc_collection_1 = [] #lists for the spline graph
	mc_collection_2 = []
	mc_collection_3 = []
	series_fc = []
	series_pwp = []
	series_mc_ave = []

	for mc_obj in mc_1_sorted:
		mc_value = float(mc_obj.mc_data)
		mc_collection_1.append(calculateMC(mc_value))
		series_fc.append(round(soil_fc*100, 2))
		series_pwp.append(round(soil_pwp*100, 2))
	
	for mc_obj in mc_2_sorted:
		mc_value = float(mc_obj.mc_data)
		mc_collection_2.append(calculateMC(mc_value))
	
	for mc_obj in mc_3_sorted:
		mc_value = float(mc_obj.mc_data)
		mc_collection_3.append(calculateMC(mc_value))

	mci_1 = calculateMC(mci_1)
	mci_2 = calculateMC(mci_2)
	mci_3 = calculateMC(mci_3)

	depth_1 = float(sensor_1.get().depth)*1000
	depth_2 = float(sensor_2.get().depth)*1000
	depth_3 = float(sensor_3.get().depth)*1000

	crop_model = crop.root_growth_model # for computation of the actual depth of rootzone
	crop_drz = float(crop.drz)
	crop_ro = float(crop.root_ini)
	def calculateDRZ(crop_dat):
		if crop_model == "Borg-Grimes Model": # Borg-Grimes Model
			sine = 0.5*(math.sin(math.radians(3.03*(crop_dat/crop_growingperiod)-1.47)))
			drz = round((float(crop_drz - crop_ro)*(0.5 + sine))*1000, 0) #convert to mm
		if crop_model == "User-Defined": # User-Defined
			eqnform = crop.eqnform
			if eqnform == "linear":
				a = float(crop.root_a)
				b = float(crop.root_b)
				drz = a*crop_dat + b
			if eqnform =="quadratic":
				a = float(crop.root_a)
				b = float(crop.root_b)
				c = float(crop.root_c)
				drz = a*(crop_dat**b) + b
		if crop_model == "Inverse Kc": # Inverse Kc
			kc_ini = float(crop.kc_ini)
			kc_mid = float(crop.kc_mid)
			kc_end = float(crop.kc_end)
			cc_1 = float(crop.kc_cc_1)
			cc_2 = float(crop.kc_cc_2)
			cc_3 = float(crop.kc_cc_3)
			maturity = float((crop_dat/crop_growingperiod)*100)
			if maturity <= cc_2:
				Kc_adj = kc_ini + (kc_mid - kc_ini)*(maturity)/(cc_2)
			if maturity > cc_2:
				Kc_adj = kc_mid
			krz = float((Kc_adj - kc_ini)/(kc_mid - kc_ini))
			drz = float(crop_ro + krz*(crop_drz - crop_ro))*1000
		return round(drz)
	
	drz_collection = []

	for mc_obj in mc_1_sorted:
		mc_date = mc_obj.timestamp.date()
		crop_dat = ((mc_date - crop_transplanted).days)
		drz_collection.append(calculateDRZ(crop_dat))

	drz = calculateDRZ(crop_dat)

	def calculateMC_AVE(drz, mc_a, mc_b, mc_c): #Calculating average MCv
		if drz <= depth_1:
			mc_ave = mc_a
		if drz > depth_1 and drz <= depth_2:
			mc_ave = ((mc_a*depth_1) + (mc_b*(drz-depth_1)))/(drz)
		else:
			mc_ave = ((mc_a*depth_1) + (mc_b*(depth_2-depth_1)) + (mc_c*(drz-depth_2)))/(drz)
		return round(mc_ave, 2)
	
	mc_ave_collection = []

	for (drz, mc_a, mc_b, mc_c) in zip(drz_collection, mc_collection_1, mc_collection_2, mc_collection_3):
		mc_ave_collection.append(calculateMC_AVE(drz, mc_a, mc_b, mc_c))

	mc_ave = calculateMC_AVE(drz, mc_a, mc_b, mc_c)

	def calculateFn(x, y): #Calculate net application depth (Fn)
		net_application_depth = round(((soil_fc - y/100)*x))
		return net_application_depth

	Fn_collection = []
	
	for (x, y) in zip(drz_collection, mc_ave_collection):
		Fn_collection.append(calculateFn(x, y))
	
	net_application_depth = calculateFn(x, y)
	#IRRIGATION SYSTEM
	if irrigation_type == "furrow" or "basin" or "border":
		intake_family = soil.intake_family
		cons_c = 7.0
		if intake_family == "clay_005":
			rate = 0.05
		if intake_family == "clay_01":
			rate = 0.1
		if intake_family == "clay_015":
			rate = 0.15
		if intake_family == "clay_loam_02":
			rate = 0.2
		if intake_family == "clay_loam_025":
			rate = 0.25
		if intake_family == "clay_loam_03":
			rate = 0.3
		if intake_family == "silty_035":
			rate = 0.35
		if intake_family == "silty_04":
			rate = 0.4
		if intake_family == "silty_loam_045":
			rate = 0.45
		if intake_family == "silty_loam_05":
			rate = 0.5
		if intake_family == "silty_loam_06":
			rate = 0.6
		if intake_family == "silty_loam_07":
			rate = 0.7
		if intake_family == "sandy_loam_08":
			rate = 0.8
		if intake_family == "sandy_loam_09":
			rate = 0.9
		if intake_family == "sandy_loam_10":
			rate = 1.0
		if intake_family == "sandy_15":
			rate = 1.5
		if intake_family == "sandy_20":
			rate = 2.0
		cons_a = -0.1831*rate**2 + 1.4917*rate + 0.486
		cons_b = 0.0524*math.log(rate) + 0.7822
		cons_f = 1.7926*rate + 7.0715
		cons_g = 0.0003*rate + 0.00009
	#BASIN
	ea = 0
	if irrigation_type == "basin":
		unit_discharge =  float(irrigation_q/1000)
		basin_length = float(irrigation.basin_length)
		ea = float(irrigation.ea)

		if ea == 95:
			R = 0.16
		if ea == 90:
			R = 0.28
		if ea == 85:
			R =	0.4
		if ea == 80:
			R = 0.58
		if ea == 75:
			R = 0.8
		if ea == 70:
			R = 1.08
		if ea == 0.65:
			R = 1.45
		if ea == 60:
			R = 1.9
		if ea == 0.55:
			R = 2.45
		if ea == 50:
			R = 3.2

		inflow_time = round(((net_application_depth * basin_length)/(600.0*ea*unit_discharge)),2)
		net_opportunity_time = ((net_application_depth - cons_c)/cons_a)**(1.0/cons_b)
		advanced_time = round((net_opportunity_time * R),2)
		
		if inflow_time >= advanced_time:
			irrigation_period = (inflow_time)
		else:
			irrigation_period = (advanced_time)
		
		total_volume = irrigation_period * unit_discharge*60*1000

	#FURROW
	if irrigation_type == "furrow":
		slope = float(irrigation.area_slope)
		furrow_spacing = float(irrigation.furrow_spacing)
		furrow_length = float(irrigation.furrow_length)
		mannings_coeff = float(irrigation.mannings_coeff)
		discharge = float(irrigation_q)
		bln_open = irrigation.bln_furrow_type
		P_adj = 0.265*(discharge*mannings_coeff/slope**0.5)**0.425 + 0.227
		net_opportunity_time = (((net_application_depth*(furrow_spacing/P_adj))-cons_c)/cons_a)**(1/cons_b)

		if bln_open:
			irrigation_period = net_opportunity_time
		else:
			beta = (cons_g * furrow_length)/(discharge*slope**0.5)
			advanced_time = (furrow_length*(math.e)**beta)/cons_f
			irrigation_period = net_opportunity_time + advanced_time

		irrigation_period = round((irrigation_period), 2)
		total_volume = irrigation_period * discharge * 60

	#BORDER
	if irrigation_type == "border":
		intake_family = soil.intake_family
		So = float(irrigation.area_slope)
		Fn = net_application_depth
		n = irrigation.mannings_coeff
		Tn = ((Fn - cons_c)/cons_a)**(1/cons_b)
		Qu = irrigation.discharge
		if slope <= 0.004:
			Tl = ((Qu**0.2)*n)/120*[So+[(0.0094*n*Qu**0.175/[(Tn**0.88)*(So**0.5)])**1.6]]
		if slope > 0.004:
			Tl = (Qu**0.2)*(n**1.2)/(120*So**1.6)
		irrigation_period = Tn - Tl
	#SPRINKLER
	if irrigation_type == "sprinkler":
		Sl = float(irrigation.sprinkler_spacing)
		Sm = float(irrigation.lateral_spacing)
		ea = float(irrigation.ea)/100
		if irrigation.bln_sprinkler_discharge == "Yes":
			d = float(irrigation.nozzle_diameter)
			P = float(irrigation.operating_pressure)
			C = float(irrigation.discharge_coefficient)
			q = 0.1109543178 * C * d**2 * P**0.5 #original equation in english system q=28.95Cd^2P^0.5 (gpm, in, psi)
		else:
			q = float(irrigation_q)
		
		Etcrop = float(crop.peak_Etcrop)
		irrigation_interval = round(net_application_depth/Etcrop)
		gross_application_depth = net_application_depth/ea
		#if discharge is known
		application_rate = q*3600/(Sl*Sm) #mm/hr
		irrigation_period = round((gross_application_depth/application_rate)*60,2) #(min) time of operation
		total_volume = round(q * irrigation_period * 60)
	#END
	area_shaded = 0
	q = 0
	#DRIP
	if irrigation_type == "drip":
		area_shaded = PercentShaded.objects.all().filter(crop=crop).latest().area_shaded
		q = float(irrigation.emitter_discharge)
		bln_single_lateral = irrigation.bln_single_lateral
		bln_ii = irrigation.bln_ii
		Np = float(irrigation.emitters_per_plant)
		Se = float(irrigation.emitter_spacing)
		Sp = float(irrigation.plant_spacing)
		So = float(irrigation.row_spacing)
		w = float(irrigation.wetted_dia)
		eu = float(irrigation.EU)
		Etcrop = float(crop.peak_Etcrop)
		transpiration_ratio = float(crop.transpiration_ratio)
		Pd = float(area_shaded/100)
		
		if bln_single_lateral:
			Pw = (Np*Se*w/(Sp*So))
		else:
			Se = 0.8*Se
			Pw = (Np*Se*(Se + w)/(2*Sp*So))

		net_application_depth = net_application_depth * Pw
		gross_application_depth = net_application_depth*transpiration_ratio/eu

		if bln_ii:
			irrigation_interval = float(irrigation.irrigation_interval)
		else:
			Td = Etcrop*(Pd + 0.15*(1 - Pd))
			irrigation_interval = net_application_depth/Td
		gross_volume_per_plant = (gross_application_depth*Sp*So/irrigation_interval) #(L/day)
		irrigation_period = (gross_volume_per_plant/(Np*q))*24*60
		total_volume = gross_volume_per_plant
		
	#FOR DISPLAY
	net_application_depth = round(net_application_depth)
	irrigation_period = round(irrigation_period)
	soil_fc = soil.fc
	soil_pwp = soil.pwp
	crop_mad = round(crop.mad * 100)
	total_volume = round((total_volume/1000),4)
	context = {
		"final_list": reversed_list,
		"form": form,
		"selected_system": selected_system,
		"crop": crop,
		"soil": soil,
		"soil_fc":soil_fc,
		"soil_pwp": soil_pwp,
		"intake_family": intake_family,
		"irrigation": irrigation,
		"irrigation_type": irrigation_type,
		"irrigation_q": irrigation_q,
		"ea": ea,
		"crop_transplanted": crop_transplanted,
		"crop_growingperiod": crop_growingperiod,
		"crop_dat": crop_dat,
		"crop_mad": crop_mad,
		"calib": calib,
		"calib_eqn": calib_eqn,
		"calib_coeff_a": calib.coeff_a,
		"calib_coeff_b": calib.coeff_b,
		"calib_coeff_c": calib.coeff_c,
		"calib_coeff_d": calib.coeff_d,
		"calib_coeff_m": calib.coeff_m,
		"fieldunit": fieldunit,
		"s1": sensor_1,
		"s2": sensor_2,
		"s3": sensor_3,
		"mc_1": mc_collection_1,
		"mc_time_1": mc_1_sorted,
		"mc_2": mc_collection_2,
		"mc_3": mc_collection_3,
		"series_fc": series_fc,
		"series_pwp": series_pwp,
		"rainfall": rainfall_collection,
		"mc_ave_collection": mc_ave_collection,
		"Fn_collection": Fn_collection,
		"MC_TO_IRRIGATE": MC_TO_IRRIGATE,
		"drz": drz,
		"mci_1": mci_1,
		"depth_1": depth_1,
		"mc_ave": mc_ave,
		"net_application_depth": net_application_depth,
		"irrigation_period":irrigation_period,
		"total_volume": total_volume,
		"area_shaded": area_shaded,
		"emitter_discharge": q
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
			return redirect('/dashboard/')
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
			return redirect('/dashboard/')
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
			return redirect('/dashboard/')

	context = {
		"form":form,
		"item":para,
	}
	return render(request, 'waissapp/edit_system.html', context)

def delete_system(request, pk):
	para = WAISSystems.objects.get(id=pk)
	if request.method == 'POST':
		para.delete()
		return redirect('/list_system/')
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
			return redirect('/list_calib/')
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
			return redirect('/list_calib/')

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
            return redirect('/list_soil/')
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
	formset = SensorFormSet(queryset=Sensor.objects.none())
	if request.method == 'POST':
		formset = SensorFormSet(request.POST)
		if formset.is_valid():
			formset.save()
			return redirect('/list_sensor/')
	else:  # display empty form
		formset = SensorFormSet(queryset=Sensor.objects.none())
	
	context = {
		"formset": formset,
	}

	return render(request, 'waissapp/new_sensor.html', context)

def add_sensor(request):
	SensorFormSet = modelformset_factory(Sensor, exclude=(), extra=3)
	formset = SensorFormSet(queryset=Sensor.objects.none())
	if request.method == 'POST':
		formset = SensorFormSet(request.POST)
		if formset.is_valid():
			formset.save()
			return redirect('/list_sensor/')
	else:  # display empty form
		formset = SensorFormSet(queryset=Sensor.objects.none())
	
	context = {
		"formset": formset,
	}
	
	return render(request, 'waissapp/add_sensor.html', context)

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
	para = SentMsgs.objects.get(id=pk)

	if request.method == 'POST':
		para.delete()
		return redirect('/messages/')
	context = {
		"item":para,
	}
	return render(request, 'waissapp/delete_messages.html', context)

def view_msg(request, number):
	receivedmsgs = ReceivedMsgs.objects.all()
	sentmsgs = SentMsgs.objects.all()
	llist = sorted(chain(receivedmsgs, sentmsgs), key=attrgetter('timestamp'))
	joined_list = reversed(llist)
	cel_number = Personnel.objects.get(first_name=number)
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
	formset = DataFormSet(queryset=MoistureContent.objects.none())
	if request.method == 'POST':
		formset = DataFormSet(request.POST)
		if formset.is_valid():
			formset.save()
			return redirect('/dashboard/')
	else:  # display empty form
		formset = DataFormSet(queryset=MoistureContent.objects.none())
	
	context = {
		"formset": formset,
	}

	return render(request, 'waissapp/new_mc.html', context)

def add_mc(request):
	DataFormSet = modelformset_factory(MoistureContent, exclude=(), extra=6)
	formset = DataFormSet(queryset=MoistureContent.objects.none())
	if request.method == 'POST':
		formset = DataFormSet(request.POST)
		if formset.is_valid():
			formset.save()
			return redirect('/dashboard/')
	else:  # display empty form
		formset = DataFormSet(queryset=MoistureContent.objects.none())
	
	context = {
		"formset": formset,
	}
	return render(request, 'waissapp/add_mc.html', context)

def edit_mc(request, name):
	para = MoistureContent.objects.get(id=name)
	form = MCForm(instance=para)

	if request.method == 'POST':  # data sent by user
		form = MCForm(request.POST, instance=para)
		if form.is_valid():
			form.save()  # this will save info to database
			return redirect('/dashboard/')

	context = {
		"form":form,
		"item": para,
	}
	return render(request, 'waissapp/edit_mc.html', context)

def list_mc(request, name):
	sensor_instance = Sensor.objects.get(name=name)
	get_mc = MoistureContent.objects.filter(sensor=sensor_instance)

	context = {
		"list": get_mc,
	}
	return render(request, 'waissapp/list_mc.html', context)

def delete_mc(request, pk):
	para = MoistureContent.objects.get(id=pk)
	if request.method == 'POST':
		para.delete()
		return redirect('/list_sensor/')
	context = {
		"item":para	
	}
	return render(request, 'waissapp/delete_mc.html', context)
