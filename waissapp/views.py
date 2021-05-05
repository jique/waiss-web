from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import SentMsgs, ReceivedMsgs, Personnel, Farm, Sensor, MoistureContent, FieldUnit, Soil, Crop, CalibrationConstant, WAISSystems, PercentShaded, Rainfall, Gravimetric, Basin, Furrow, Border, Drip, Sprinkler
from django.utils import timezone
import datetime
from datetime import date, datetime
from django import forms
from django.forms import modelformset_factory
from .forms import SentMsgsForm, PersonnelForm, SoilForm, CalibForm, CropForm, FarmForm, FieldUnitForm, SensorForm, MCForm, WAISSystemsForm, BasinForm, DripForm, SprinklerForm, FurrowForm, BorderForm, PercentShadedForm, GravimetricForm
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


@login_required
def index(request):
	receivedmsgs = ReceivedMsgs.objects.all() #for message center
	sentmsgs = SentMsgs.objects.all()
	llist = sorted(chain(receivedmsgs, sentmsgs), key=attrgetter('timestamp'))
	reversed_list =reversed(llist)
	
	current_user = request.user
	
	form = WAISSystems.objects.filter(author=current_user) # for_dropdown_select_options
	
	if request.method == 'POST':  # for sending the selected WAISS_system by the user
		selected_system = request.POST['selected_system']
		selected_system = WAISSystems.objects.get(name=selected_system)
	else:
		if form.exists():
			selected_system = WAISSystems.objects.filter(author=current_user).latest()
		else:
			return redirect ('/new_farm/')
		

	crop = selected_system.crop # getting crop variables
	crop_transplanted = crop.date_transplanted
	crop_growingperiod = (crop.growingperiod)
	crop_mad = float(crop.mad)

	soil = selected_system.soil  # getting soil variables
	soil_fc = float(soil.fc/100)
	soil_pwp = float(soil.pwp/100)

	calib = selected_system.calib  # getting calibration variables
	calib_eqn = calib.calib_equation

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

	gravimetric_data = Gravimetric.objects.all().filter(fieldunit=fieldunit) #for gravimetric data
	sorted_gravimetric = sorted(gravimetric_data, key=attrgetter('timestamp'))
	gravimetric_collection = [] 

	for p in sorted_gravimetric: # for creating list that has the same index of the mc data
		p_time = p.timestamp
		p_amount = float(p.mc_data)
		j = len(gravimetric_collection)
		for i, m in enumerate(mc_list, start=1):
			m_time = m.timestamp
			if p_time == m_time:
				z = i-j-1
				for x in range(0, z):
					gravimetric_collection.append(0.0)
				gravimetric_collection.append(p_amount)
				break
	MC_TO_IRRIGATE = round((((soil_fc - soil_pwp)* crop_mad) + soil_pwp)*100, 2) # mc to initiate irrigation advisory
	mci_1 = float(mc_1.latest().mc_data)
	mci_2 = float(mc_2.latest().mc_data)
	mci_3 = float(mc_3.latest().mc_data)
	
	def calculateMC(mc_value): # Convert analog reading to MCv
		float(mc_value)
		if calib_eqn == "linear":
			calib_coeff_a = float(calib.coeff_a)
			calib_coeff_b = float(calib.coeff_b)
			mc_return = calib_coeff_a * (mc_value)+ calib_coeff_b
		if calib_eqn == "quadratic":
			calib_coeff_a = float(calib.coeff_a)
			calib_coeff_b = float(calib.coeff_b)
			calib_coeff_c = float(calib.coeff_c)
			mc_return = calib_coeff_a * (mc_value)**2 + calib_coeff_b*(mc_value) + calib_coeff_c
		if calib_eqn == "exponential":
			calib_coeff_a = float(calib.coeff_a)
			calib_coeff_b = float(calib.coeff_b)
			mc_return = calib_coeff_a*math.exp(calib_coeff_b*mc_value)
		if calib_eqn == "logarithmic":
			calib_coeff_a = float(calib.coeff_a)
			calib_coeff_b = float(calib.coeff_b)
			mc_return = calib_coeff_a*math.log(mc_value) + calib_coeff_b
		if calib_eqn == "symmetrical sigmoidal":
			calib_coeff_a = float(calib.coeff_a)
			calib_coeff_b = float(calib.coeff_b)
			calib_coeff_c = float(calib.coeff_c)
			calib_coeff_d = float(calib.coeff_d)
			calib_coeff_m = float(calib.coeff_m)
			mc_return = calib_coeff_d + (calib_coeff_a - calib_coeff_d)/(1.0 + (mc_value/calib_coeff_c)**calib_coeff_b)
		if calib_eqn == "asymmetrical sigmoidal":
			calib_coeff_a = float(calib.coeff_a)
			calib_coeff_b = float(calib.coeff_b)
			calib_coeff_c = float(calib.coeff_c)
			calib_coeff_d = float(calib.coeff_d)
			calib_coeff_m = float(calib.coeff_m)
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
		return drz
	
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
			mc_ave = ((mc_a*depth_1) + (mc_b*(depth_2-depth_1)) + (mc_c*(depth_3-depth_2)))/(depth_3)
		return round(mc_ave, 2)
	
	mc_ave_collection = []

	for (drz, mc_a, mc_b, mc_c) in zip(drz_collection, mc_collection_1, mc_collection_2, mc_collection_3):
		mc_ave_collection.append(calculateMC_AVE(drz, mc_a, mc_b, mc_c))

	mc_ave = calculateMC_AVE(drz, mc_a, mc_b, mc_c)

	def calculateFn(x, y): #Calculate net application depth (Fn)
		if y > MC_TO_IRRIGATE:
			net_application_depth = 0
		else:
			net_application_depth = float((soil_fc - y/100)*x)
		return round(net_application_depth)

	Fn_collection = []
	
	for (x, y) in zip(drz_collection, mc_ave_collection):
		Fn_collection.append(calculateFn(x, y))
	
	net_application_depth = calculateFn(x, y)

	#IRRIGATION SYSTEM

	basin = selected_system.basin
	border = selected_system.border
	furrow = selected_system.furrow
	drip = selected_system.drip
	sprinkler = selected_system.sprinkler

	if furrow != None or basin != None or border != None:
		intake_family = soil.intake_family
		cons_c = 7.0
		rate = 0.05
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
	if basin != None:
		irrigation = selected_system.basin
		irrigation_q = irrigation.discharge
		if net_application_depth == 0:
			irrigation_period = 0
			total_volume = 0
		else:
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

			inflow_time = ((net_application_depth * basin_length)/(600.0*ea*unit_discharge))
			net_opportunity_time = ((net_application_depth - cons_c)/cons_a)**(1.0/cons_b)
			advanced_time = (net_opportunity_time * R)
			
			print(inflow_time, advanced_time)
			if inflow_time >= advanced_time:
				irrigation_period = (inflow_time)
			else:
				irrigation_period = (advanced_time)
			
			total_volume = irrigation_period * unit_discharge*60*1000

	#FURROW
	if furrow != None:
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
	if border != None:
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
	if sprinkler != None:
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
		intake_family = None
	#END
	area_shaded = 0
	q = 0
	#DRIP
	if drip != None:
		area_shaded = PercentShaded.objects.all().filter(crop=crop).latest().area_shaded
		irrigation = selected_system.drip
		q = float(irrigation.discharge)
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
		intake_family = None
		irrigation_q = q
		
	#FOR DISPLAY
	net_application_depth = round(net_application_depth, 2)
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
		"soil_fc": soil_fc,
		"soil_pwp": soil_pwp,
		"intake_family": intake_family,
		"irrigation_q": irrigation_q,
		"basin": basin,
		"border": border,
		"furrow": furrow,
		"drip": drip,
		"sprinkler": sprinkler,
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
		"gravimetric_collection": gravimetric_collection,
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
	}
	return render(request, 'waissapp/index.html', context)

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

def about_calc(request):
	return render(request, 'waissapp/about_calc.html')
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

@login_required
def add_system(request):
	if request.method == 'POST':  # data sent by user
		form = WAISSystemsForm(request.POST)
		if form.is_valid():
			new_system = form.save(commit=False)
			new_system.author = request.user
			new_system.personal = True
			new_system.save()
			return redirect('/')
	else:  # display empty form
		form = WAISSystemsForm()
	
	context = {
		"form": form,
	}
	return render(request, 'waissapp/add_system.html', context)

def list_system(request):
	current_user = request.user
	queryset = WAISSystems.objects.filter(author=current_user)
	context = {
		"list":queryset,
	}
	return render(request, 'waissapp/list_system.html', context)

@login_required
def edit_system(request, pk):
	para = WAISSystems.objects.get(id=pk)
	form = WAISSystemsForm(instance=para)

	if request.method == 'POST':  # data sent by user
		form = WAISSystemsForm(request.POST, instance=para)
		if form.is_valid():
			return redirect('/')

	context = {
		"form":form,
		"item":para,
	}
	return render(request, 'waissapp/edit_system.html', context)

@login_required
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
@login_required
def add_calib(request):
	if request.method == 'POST':  # data sent by user
		form = CalibForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.author = request.user
			instance.personal = True
			instance.save()
			return redirect('/list_calib/')
	else:  # display empty form
		form = CalibForm()
	return render(request, 'waissapp/add_calib.html', {'calib_form': form})

def list_calib(request):
	current_user = request.user
	queryset_1 = CalibrationConstant.objects.filter(author=current_user)
	queryset_2 = CalibrationConstant.objects.filter(personal=False)
	new_list = sorted(chain(queryset_1, queryset_2), key=attrgetter('timestamp'))
	
	context = {
		"calib_list":new_list,
	}
	return render(request, 'waissapp/list_calib.html', context)

@login_required
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

@login_required
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

@login_required
def add_crop(request):
	if request.method == 'POST':  # data sent by user
		form = CropForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.author = request.user
			instance.personal = True
			instance.save()
			return redirect('/list_crop/')
	else:  # display empty form
		form = CropForm()

	return render(request, 'waissapp/add_crop.html', {'form': form})

def list_crop(request):
	current_user = request.user
	queryset_1 = Crop.objects.filter(author=current_user)
	queryset_2 = Crop.objects.filter(personal=False)
	new_list = sorted(chain(queryset_1, queryset_2), key=attrgetter('timestamp'))
	context = {
		"crop_list":new_list,
	}
	return render(request, 'waissapp/list_crop.html', context)

@login_required
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

@login_required
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
@login_required
def new_soil(request):
	if request.method == 'POST':  # data sent by user
		form = SoilForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.author = request.user
			instance.personal = True
			instance.save()
			return redirect('/new_irrigation/')
	else:  # display empty form
		form = SoilForm()

	return render(request, 'waissapp/new_soil.html', {'soil_form': form})

@login_required
def add_soil(request):
	if request.method == 'POST':  # data sent by user
		form = SoilForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.author = request.user
			instance.personal = True
			instance.save()
			return redirect('/list_soil/')
	else:  # display empty form
		form = SoilForm()

	return render(request, 'waissapp/add_soil.html', {'soil_form': form})

def list_soil(request):
	current_user = request.user
	queryset_1 = Soil.objects.filter(author=current_user)
	queryset_2 = Soil.objects.filter(personal=False)
	new_list = sorted(chain(queryset_1, queryset_2), key=attrgetter('timestamp'))
	
	context = {
		"soil_list":new_list,
	}
	return render(request, 'waissapp/list_soil.html', context)

@login_required
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

@login_required
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
@login_required
def new_fieldunit(request):
	if request.method == 'POST':  # data sent by user
		form = FieldUnitForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.author = request.user
			instance.personal = True
			instance.save()
			return redirect('/new_calib/')
	else:  # display empty form
		form = FieldUnitForm()

	return render(request, 'waissapp/new_fieldunit.html', {'fieldunit_form': form})

@login_required
def add_fieldunit(request):
	if request.method == 'POST':  # data sent by user
		form = FieldUnitForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.author = request.user
			instance.personal = True
			instance.save()
			return redirect('/list_fieldunit/')
	else:  # display empty form
		form = FieldUnitForm()

	return render(request, 'waissapp/add_fieldunit.html', {'fieldunit_form': form})

def list_fieldunit(request):
	current_user = request.user
	queryset_1 = FieldUnit.objects.filter(author=current_user)
	queryset_2 = FieldUnit.objects.filter(personal=False)
	new_list = chain(queryset_1, queryset_2)
	
	context = {
		"fieldunit_list":new_list,
	}
	return render(request, 'waissapp/list_fieldunit.html', context)

@login_required
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

@login_required
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

@login_required
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
	current_user = request.user
	get_fieldunit = FieldUnit.objects.filter(author=current_user)
	queryset_1 = Sensor.objects.filter(fieldunit__in=get_fieldunit)
	queryset_2 = CalibrationConstant.objects.filter(personal=False)
	new_list = chain(queryset_1, queryset_2)

	context = {
		"sensor_list":new_list,
	}

	return render(request, 'waissapp/list_sensor.html', context)

@login_required
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

@login_required
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
@login_required
def new_farm(request):
	if request.method == 'POST':  # data sent by user
		form = FarmForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.author = request.user
			instance.personal = True
			instance.save()
			return redirect('/new_personnel/')
	else:  # display empty form
		form = FarmForm()
	
	context = {
		"farm_form":form,
	}

	return render(request, 'waissapp/new_farm.html', context)

@login_required
def add_farm(request):
	if request.method == 'POST':  # data sent by user
		form = FarmForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.author = request.user
			instance.personal = True
			instance.save()
			return redirect('/list_farm/')
	else:  # display empty form
		form = FarmForm()
	return render(request, 'waissapp/add_farm.html', {'farm_form': form})

@login_required
def list_farm(request):
	current_user = request.user
	queryset_1 = Farm.objects.filter(author=current_user)
	queryset_2 = Farm.objects.filter(personal=False)
	new_list = chain(queryset_1, queryset_2)
	
	context = {
		"farm_list":new_list,
	}
	return render(request, 'waissapp/list_farm.html', context)

@login_required
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

@login_required
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
			return redirect('/list_personnel/')
	else:  # display empty form
		form = PersonnelForm()
		
	return render(request, 'waissapp/add_personnel.html', {'personnel_form': form})

def list_personnel(request):
	current_user = request.user
	queryset_1 = Personnel.objects.filter(author=current_user)
	queryset_2 = Personnel.objects.filter(personal=False)
	new_list = chain(queryset_1, queryset_2)
	context = {
		"personnel_list": new_list,
	}
	return render(request, 'waissapp/list_personnel.html', context)

@login_required
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

@login_required
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

@login_required
def add_basin(request):
	if request.method == 'POST':  # data sent by user
		form = BasinForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.author = request.user
			instance.personal = True
			instance.save()
			return redirect('/list_basin/')
	else:  # display empty form
		form = BasinForm()

	return render(request, 'waissapp/add_basin.html', {'irrigation_form': form})

@login_required
def add_furrow(request):
	if request.method == 'POST':  # data sent by user
		form = FurrowForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.author = request.user
			instance.personal = True
			instance.save()
			return redirect('/list_basin/')
	else:  # display empty form
		form = FurrowForm()

	return render(request, 'waissapp/add_furrow.html', {'irrigation_form': form})

@login_required
def add_border(request):
	if request.method == 'POST':  # data sent by user
		form = BorderForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.author = request.user
			instance.personal = True
			instance.save()
			return redirect('/list_border/')
	else:  # display empty form
		form = BorderForm()

	return render(request, 'waissapp/add_border.html', {'irrigation_form': form})

@login_required
def add_drip(request):
	if request.method == 'POST':  # data sent by user
		form = DripForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.author = request.user
			instance.personal = True
			instance.save()
			return redirect('/list_drip/')
	else:  # display empty form
		form = DripForm()

	return render(request, 'waissapp/add_drip.html', {'irrigation_form': form})

@login_required
def add_sprinkler(request):
	if request.method == 'POST':  # data sent by user
		form = SprinklerForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.author = request.user
			instance.personal = True
			instance.save()
			return redirect('/list_sprinkler/')
	else:  # display empty form
		form = SprinklerForm()

	return render(request, 'waissapp/add_sprinkler.html', {'irrigation_form': form})

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

@login_required
def delete_basin(request, pk):
	para = Basin.objects.get(id=pk)
	if request.method == 'POST':
		para.delete()
		return redirect('/list_basin/')
	context = {
		"item":para	
	}
	return render(request, 'waissapp/delete_basin.html', context)

@login_required
def delete_border(request, pk):
	para = Border.objects.get(id=pk)
	if request.method == 'POST':
		para.delete()
		return redirect('/list_border/')
	context = {
		"item":para	
	}
	return render(request, 'waissapp/delete_border.html', context)

@login_required
def delete_furrow(request, pk):
	para = Furrow.objects.get(id=pk)
	if request.method == 'POST':
		para.delete()
		return redirect('/list_furrow/')
	context = {
		"item":para	
	}
	return render(request, 'waissapp/delete_furrow.html', context)

@login_required
def delete_drip(request, pk):
	para = Drip.objects.get(id=pk)
	if request.method == 'POST':
		para.delete()
		return redirect('/list_drip/')
	context = {
		"item":para	
	}
	return render(request, 'waissapp/delete_drip.html', context)

@login_required
def delete_sprinkler(request, pk):
	para = Sprinkler.objects.get(id=pk)
	if request.method == 'POST':
		para.delete()
		return redirect('/list_sprinkler/')
	context = {
		"item":para	
	}
	return render(request, 'waissapp/delete_sprinkler.html', context)

def list_basin(request):
	current_user = request.user
	queryset_1 = Basin.objects.filter(author=current_user)
	queryset_2 = Basin.objects.filter(personal=False)
	new_list = chain(queryset_1, queryset_2)
	context = {
		"list": new_list,
	}
	return render(request, 'waissapp/list_basin.html', context)

def list_border(request):
	current_user = request.user
	queryset_1 = Border.objects.filter(author=current_user)
	queryset_2 = Border.objects.filter(personal=False)
	new_list = chain(queryset_1, queryset_2)
	context = {
		"list": new_list,
	}
	return render(request, 'waissapp/list_border.html', context)

def list_furrow(request):
	current_user = request.user
	queryset_1 = Furrow.objects.filter(author=current_user)
	queryset_2 = Furrow.objects.filter(personal=False)
	new_list = chain(queryset_1, queryset_2)
	context = {
		"list": new_list,
	}
	return render(request, 'waissapp/list_furrow.html', context)

def list_sprinkler(request):
	current_user = request.user
	queryset_1 = Sprinkler.objects.filter(author=current_user)
	queryset_2 = Sprinkler.objects.filter(personal=False)
	new_list = chain(queryset_1, queryset_2)
	context = {
		"list": new_list,
	}
	return render(request, 'waissapp/list_sprinkler.html', context)

def list_drip(request):
	current_user = request.user
	queryset_1 = Drip.objects.filter(author=current_user)
	queryset_2 = Drip.objects.filter(personal=False)
	new_list = chain(queryset_1, queryset_2)
	context = {
		"list": new_list,
	}
	return render(request, 'waissapp/list_drip.html', context)

@login_required
def edit_basin(request, pk):
	para = Basin.objects.get(id=pk)
	form = BasinForm(instance=para)

	if request.method == 'POST':  # data sent by user
		form = BasinForm(request.POST, instance=para)
		if form.is_valid():
			form.save()  # this will save info to database
			return redirect('/list_basin/')

	context = {
		"form":form,
		"item": para,
	}
	return render(request, 'waissapp/edit_basin.html', context)

@login_required
def edit_border(request, pk):
	para = Border.objects.get(id=pk)
	form = BorderForm(instance=para)

	if request.method == 'POST':  # data sent by user
		form = BorderForm(request.POST, instance=para)
		if form.is_valid():
			form.save()  # this will save info to database
			return redirect('/list_border/')

	context = {
		"form":form,
		"item": para,
	}
	return render(request, 'waissapp/edit_border.html', context)

@login_required
def edit_furrow(request, pk):
	para = Furrow.objects.get(id=pk)
	form = FurrowForm(instance=para)

	if request.method == 'POST':  # data sent by user
		form = FurrowForm(request.POST, instance=para)
		if form.is_valid():
			form.save()  # this will save info to database
			return redirect('/list_furrow/')

	context = {
		"form":form,
		"item": para,
	}
	return render(request, 'waissapp/edit_furrow.html', context)

@login_required
def edit_drip(request, pk):
	para = Drip.objects.get(id=pk)
	form = DripForm(instance=para)

	if request.method == 'POST':  # data sent by user
		form = DripForm(request.POST, instance=para)
		if form.is_valid():
			form.save()  # this will save info to database
			return redirect('/list_drip/')

	context = {
		"form": form,
		"item": para,
	}
	return render(request, 'waissapp/edit_drip.html', context)

@login_required
def edit_sprinkler(request, pk):
	para = Sprinkler.objects.get(id=pk)
	form = SprinklerForm(instance=para)

	if request.method == 'POST':  # data sent by user
		form = SprinklerForm(request.POST, instance=para)
		if form.is_valid():
			form.save()  # this will save info to database
			return redirect('/list_sprinkler/')

	context = {
		"form":form,
		"item": para,
	}
	return render(request, 'waissapp/edit_sprinkler.html', context)

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
		return redirect('/messages/')
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

@login_required
def add_mc(request):
	DataFormSet = modelformset_factory(MoistureContent, exclude=(), extra=3)
	formset = DataFormSet(queryset=MoistureContent.objects.none())
	if request.method == 'POST':
		formset = DataFormSet(request.POST)
		if formset.is_valid():
			formset.save()
			return redirect('/add_mc/')
	else:  # display empty form
		formset = DataFormSet(queryset=MoistureContent.objects.none())
	
	context = {
		"formset": formset,
	}
	return render(request, 'waissapp/add_mc.html', context)

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
def edit_mc(request, name):
	para = MoistureContent.objects.get(id=name)
	form = MCForm(instance=para)

	if request.method == 'POST':  # data sent by user
		form = MCForm(request.POST, instance=para)
		if form.is_valid():
			form.save()  # this will save info to database
			return redirect('/')

	context = {
		"form":form,
		"item": para,
	}
	return render(request, 'waissapp/edit_mc.html', context)

def list_mc(request, name):
	sensor_instance = Sensor.objects.get(name=name)
	get_mc = MoistureContent.objects.filter(sensor=sensor_instance)
	reversed_list = reversed(sorted(get_mc, key=attrgetter('timestamp')))

	context = {
		"list": reversed_list,
	}
	return render(request, 'waissapp/list_mc.html', context)

@login_required
def delete_mc(request, pk):
	para = MoistureContent.objects.get(id=pk)
	if request.method == 'POST':
		para.delete()
		return redirect('/list_sensor/')
	context = {
		"item":para	
	}
	return render(request, 'waissapp/delete_mc.html', context)

@login_required
def add_rainfall(request):
	RainfallFormSet = modelformset_factory(Rainfall, exclude=(), extra=1)
	formset = RainfallFormSet(queryset=Rainfall.objects.none())
	queryset = Rainfall.objects.all()
	reversed_list = reversed(sorted(queryset, key=attrgetter('timestamp')))

	if request.method == 'POST':
		formset = RainfallFormSet(request.POST)
		if formset.is_valid():
			formset.save()
			return redirect('/add_rainfall/')
	else:  # display empty form
		formset = RainfallFormSet(queryset=Rainfall.objects.none())
	
	context = {
		"formset": formset,
		"list": reversed_list,
	}
	return render(request, 'waissapp/add_rainfall.html', context)

@login_required
def edit_rainfall(request, name):
	para = Rainfall.objects.get(id=name)
	form = RainfallForm(instance=para)

	if request.method == 'POST':  # data sent by user
		form = RainfallForm(request.POST, instance=para)
		if form.is_valid():
			form.save()  # this will save info to database
			return redirect('/')

	context = {
		"form":form,
		"item": para,
	}
	return render(request, 'waissapp/edit_rainfall.html', context)

@login_required
def delete_rainfall(request, pk):
	para = Rainfall.objects.get(id=pk)
	if request.method == 'POST':
		para.delete()
		return redirect('/add_rainfall/')
	context = {
		"item":para	
	}
	return render(request, 'waissapp/delete_rainfall.html', context)

@login_required
def add_shaded(request):
	PercentShadedFormSet = modelformset_factory(PercentShaded, exclude=(), extra=1)
	formset = PercentShadedFormSet(queryset=PercentShaded.objects.none())
	queryset = PercentShaded.objects.all()
	reversed_list = reversed(sorted(queryset, key=attrgetter('date')))
	if request.method == 'POST':
		formset = PercentShadedFormSet(request.POST)
		if formset.is_valid():
			formset.save()
			return redirect('/add_shaded/')
	else:  # display empty form
		formset = PercentShadedFormSet(queryset=PercentShaded.objects.none())
	
	context = {
		"formset": formset,
		"list": reversed_list,
	}
	
	return render(request, 'waissapp/add_shaded.html', context)

@login_required
def edit_shaded(request, pk):
	para = PercentShaded.objects.get(id=pk)
	form = PercentShadedForm(instance=para)

	if request.method == 'POST':  # data sent by user
		form = PercentShadedForm(request.POST, instance=para)
		if form.is_valid():
			form.save()  # this will save info to database
			return redirect('/')

	context = {
		"form":form,
		"item": para,
	}
	return render(request, 'waissapp/edit_shaded.html', context)

@login_required
def delete_shaded(request, pk):
	para = PercentShaded.objects.get(id=pk)
	if request.method == 'POST':
		para.delete()
		return redirect('/add_shaded/')
	context = {
		"item":para	
	}
	return render(request, 'waissapp/delete_shaded.html', context)

@login_required
def add_gravimetric(request):
	GravimetricFormSet = modelformset_factory(Gravimetric, exclude=(), extra=1)
	formset = GravimetricFormSet(queryset=Gravimetric.objects.none())
	queryset = Gravimetric.objects.all()
	reversed_list = reversed(sorted(queryset, key=attrgetter('timestamp')))
	if request.method == 'POST':
		formset = GravimetricFormSet(request.POST)
		if formset.is_valid():
			formset.save()
			return redirect('/add_gravimetric/')
	else:  # display empty form
		formset = GravimetricFormSet(queryset=Gravimetric.objects.none())
	
	context = {
		"formset": formset,
		"list": reversed_list,
	}
	
	return render(request, 'waissapp/add_gravimetric.html', context)

@login_required
def edit_gravimetric(request, pk):
	para = Gravimetric.objects.get(id=pk)
	form = GravimetricForm(instance=para)
	if request.method == 'POST':  # data sent by user
		form = GravimetricForm(request.POST, instance=para)
		if form.is_valid():
			form.save()  # this will save info to database
			return redirect('/')
	context = {
		"form":form,
		"item": para,
	}
	return render(request, 'waissapp/edit_gravimetric.html', context)

@login_required
def delete_gravimetric(request, pk):
	para = Gravimetric.objects.get(id=pk)
	if request.method == 'POST':
		para.delete()
		return redirect('/add_gravimetric/')
	context = {
		"item":para	
	}
	return render(request, 'waissapp/delete_gravimetric.html', context)