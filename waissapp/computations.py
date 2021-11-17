from django.shortcuts import render, redirect
from .models import SentMsgs, ReceivedMsgs, Sensor, MoistureContent, WAISSystems, PercentShaded, Rainfall, Gravimetric
from itertools import chain
from operator import attrgetter
import math
from django.contrib.auth.decorators import login_required
import datetime
from datetime import datetime
import pytz
import operator

@login_required
def index(request):
	receivedmsgs = ReceivedMsgs.objects.all() #for message center
	sentmsgs = SentMsgs.objects.all()
	msgs_list = sorted(chain(receivedmsgs, sentmsgs), key=attrgetter('timestamp'))
	reversed_list =reversed(msgs_list)
	
	current_user = request.user
	form = WAISSystems.objects.filter(author=current_user) # for_dropdown_select_options
	
	if request.method == 'POST' and 'dashboard_submit' in request.POST:  # for sending the selected WAISS_system by the user
		selected_system = request.POST['dashboard_submit']
		selected_system = WAISSystems.objects.get(name=selected_system)
	else:
		if form.exists():
			selected_system = WAISSystems.objects.filter(author=current_user).latest()
		else:
			return redirect ('/new_farm/')

	crop = selected_system.crop # getting crop variables
	crop_id = selected_system.crop.id
	crop_transplanted = selected_system.date_transplanted
	crop_growingperiod = (crop.growingperiod)
	crop_mad = float(crop.mad)

	soil = selected_system.soil  # getting soil variables
	soil_fc = float(soil.fc/100)
	soil_pwp = float(soil.pwp/100)

	calib = selected_system.calib  # getting calibration variables
	calib_eqn = calib.calib_equation

	fieldunit = selected_system.fieldunit  # getting fieldunit variables
	
	query_sensors = Sensor.objects.all().filter(fieldunit=fieldunit)
	num_sensors = len(query_sensors) #get number of sensors

	sensor_2 = None #for single sensor fieldunit
	sensor_3 = None
	
	error_msg_no_sensor_data = ""
	error_msg_excess_sensor_data = ""

	if num_sensors == 1:
		sensor_1 = Sensor.objects.all().filter(fieldunit=fieldunit)[:1]
		mc_1 = MoistureContent.objects.all().filter(sensor=sensor_1) # getting mc analog readings
		mc_1_sorted = sorted(mc_1, key=operator.attrgetter('date', 'time')) # sorting mc analog readings based on inputted datetime
	if num_sensors == 2:
		sensor_1 = Sensor.objects.all().filter(fieldunit=fieldunit)[:1]  # getting sensors
		sensor_2 = Sensor.objects.all().filter(fieldunit=fieldunit)[1:2]
		mc_1 = MoistureContent.objects.all().filter(sensor=sensor_1) # getting mc analog readings
		mc_2 = MoistureContent.objects.all().filter(sensor=sensor_2)
		mc_1_sorted = sorted(mc_1, key=operator.attrgetter('date', 'time')) # sorting mc analog readings based on inputted datetime
		mc_2_sorted = sorted(mc_2, key=operator.attrgetter('date', 'time'))
	if num_sensors == 3:
		sensor_1 = Sensor.objects.all().filter(fieldunit=fieldunit)[:1]  # getting sensors
		sensor_2 = Sensor.objects.all().filter(fieldunit=fieldunit)[1:2]
		sensor_3 = Sensor.objects.all().filter(fieldunit=fieldunit)[2:3]
		mc_1 = MoistureContent.objects.all().filter(sensor=sensor_1) # getting mc analog readings
		mc_2 = MoistureContent.objects.all().filter(sensor=sensor_2)
		mc_3 = MoistureContent.objects.all().filter(sensor=sensor_3)
		mc_1_sorted = sorted(mc_1, key=operator.attrgetter('date', 'time')) # sorting mc analog readings based on inputted datetime
		mc_2_sorted = sorted(mc_2, key=operator.attrgetter('date', 'time'))
		mc_3_sorted = sorted(mc_3, key=operator.attrgetter('date', 'time'))
	if num_sensors == 0:
		error_msg_no_sensor_data = "Please add sensors!"
	else: 
		error_msg_excess_sensor_data = "Number of sensors is should be between 1 and 3 only. Please recheck your your database and delete the extra sensor."

	rainfall = Rainfall.objects.all().filter(fieldunit=fieldunit)
	sorted_rainfall = sorted(rainfall, key=operator.attrgetter('date', 'time'))

	mc_collection_1 = [] #lists for the spline graph
	mc_collection_2 = []
	mc_collection_3 = []
	rainfall_collection = []

	#CORRECT BUT TOO SLOW
	#mc_raw_1 = [] #lists for the spline graph #makesure same date & time each mc data
	#mc_raw_2 = []
	#mc_raw_3 = []
	#mc_list_date = []
	#for p in mc_1_sorted:
	#		mc_raw_1.append(p.mc_data)
	#		mc_list_date.append(p.date)
	#	mc_list = mc_raw_1
	#if num_sensors == 2:
	#	for p in mc_1_sorted:
	#			if p.time == m.time and p.date == m.date:
	#				mc_raw_1.append(p.mc_data)
	#				mc_raw_2.append(m.mc_data)
	#				mc_list_date.append(p.date)
	#				break
	#	mc_list = mc_raw_1
	#if num_sensors == 3:
	#	for p in mc_1_sorted:
	#		for m in mc_2_sorted:
	#			for s in mc_3_sorted:
	#				if p.time == m.time == s.time and p.date == m.date == s.date:
	#					mc_raw_1.append(p.mc_data)
	#					mc_raw_2.append(m.mc_data)
	#					mc_raw_3.append(s.mc_data)
	#					mc_list_date.append(p.date)
	#					break	
	#	mc_list = mc_raw_1

	for p in sorted_rainfall: # for creating list that has the same index of the mc data
		j = len(rainfall_collection)
		for i, m in enumerate(mc_list, start=1):
			m_time = m.time.replace(second=0)
			if p.time == m_time and p.date == m.date:
				z = i-j-1
				for x in range(0, z):
					rainfall_collection.append(0.0)
				rainfall_collection.append(p.amount)
				break

	gravimetric_data = Gravimetric.objects.all().filter(fieldunit=fieldunit) #for gravimetric data
	sorted_gravimetric = sorted(gravimetric_data, key=operator.attrgetter('date', 'time'))
	gravimetric_collection = [] 

	for p in sorted_gravimetric: # for creating list that has the same index of the mc data
		j = len(gravimetric_collection)
		for i, m in enumerate(mc_list, start=1):
			m_time = m.time.replace(second=0)
			if p.time == m_time and p.date == m.date:
				z = i-j-1
				for x in range(0, z):
					gravimetric_collection.append(0.0)
				gravimetric_collection.append(p.mc_data)
				break
	MC_TO_IRRIGATE = round((((soil_fc - soil_pwp)* crop_mad) + soil_pwp)*100, 2) # threshold mc to initiate irrigation advisory
	mci_1 = 0
	mci_2 = 0
	mci_3 = 0
	if len(mc_1) == 0:
		depth_1 = ""
		depth_2	= ""
		depth_3	= ""
		pass
	else: # take consideration the no. of sensors in the field unit
		if num_sensors == 1:
			mci_1 = float(mc_1.latest().mc_data)
			depth_1 = float(sensor_1.get().depth)*1000
		if num_sensors == 2:
			mci_1 = float(mc_1.latest().mc_data)
			mci_2 = float(mc_2.latest().mc_data)
			sensor_1d = float(sensor_1.get().depth)*1000
			sensor_2d = float(sensor_2.get().depth)*1000
			if sensor_1d < sensor_2d:
				depth_1 = sensor_1d
				depth_2 = sensor_2d
			else:
				depth_1 = sensor_2d
				depth_2 = sensor_1d
		if num_sensors == 3:
			mci_1 = float(mc_1.latest().mc_data)
			mci_2 = float(mc_2.latest().mc_data)
			mci_3 = float(mc_3.latest().mc_data)
			sensor_1d = float(sensor_1.get().depth)*1000
			sensor_2d = float(sensor_2.get().depth)*1000
			sensor_3d = float(sensor_3.get().depth)*1000
			s_list = sorted(list([sensor_1d, sensor_2d, sensor_3d]))
			depth_1 = float(s_list[0])
			depth_2 = float(s_list[1])
			depth_3 = float(s_list[2])
			print(depth_1, depth_2, depth_3)
	
	def calculateMC(mc_value): # Convert analog reading to MCv using calibration constants
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
			mc_return = calib_coeff_d + (calib_coeff_a - calib_coeff_d)/(1.0 + (mc_value/calib_coeff_c)**calib_coeff_b)
		if calib_eqn == "asymmetrical sigmoidal":
			calib_coeff_a = float(calib.coeff_a)
			calib_coeff_b = float(calib.coeff_b)
			calib_coeff_c = float(calib.coeff_c)
			calib_coeff_d = float(calib.coeff_d)
			calib_coeff_m = float(calib.coeff_m)
			mc_return = calib_coeff_d + (calib_coeff_a - calib_coeff_d)/(1.0 + (mc_value/calib_coeff_c)**calib_coeff_b)**calib_coeff_m
		return round(mc_return, 2)

	series_fc = []
	series_pwp = []

	if num_sensors == 1: #Calculating MCv(%) from raw data using the calibration constants
		for mc_obj in mc_1_sorted:
			mc_value = float(mc_obj.mc_data)
			mc_collection_1.append(calculateMC(mc_value))
			series_fc.append(round(soil_fc*100, 2))
			series_pwp.append(round(soil_pwp*100, 2))
		mci_1 = calculateMC(mci_1)
	if num_sensors == 2:
		for mc_obj in mc_1_sorted:
			mc_value = float(mc_obj.mc_data)
			mc_collection_1.append(calculateMC(mc_value))
			series_fc.append(round(soil_fc*100, 2))
			series_pwp.append(round(soil_pwp*100, 2))
		for mc_obj in mc_2_sorted:
			mc_value = float(mc_obj.mc_data)
			mc_collection_2.append(calculateMC(mc_value))
		mci_1 = calculateMC(mci_1)
		mci_2 = calculateMC(mci_2)
	if num_sensors ==3:
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

	crop_model = crop.root_growth_model # for computation of the actual depth of rootzone
	crop_drz = float(crop.drz)
	crop_ro = float(crop.root_ini)

	def calculateDRZ(crop_dat): # GETTING THE CURRENT ROOT DEPTH #
		if crop_model == "Borg-Grimes Model": # Borg-Grimes Model
			sine = 0.5*(math.sin(math.radians(3.03*(crop_dat/crop_growingperiod)-1.47)))
			drz = round((float(crop_drz - crop_ro)(0.5 + sine))*1000, 0) #converted to MM, check for errors later
		if crop_model == "User-Defined": # User-Defined
			eqnform = crop.eqnform
			if eqnform == "linear":
				a = float(crop.root_a)
				b = float(crop.root_b)
				drz = a*crop_dat + b #MM
			if eqnform =="quadratic":
				a = float(crop.root_a)
				b = float(crop.root_b)
				c = float(crop.root_c)
				drz = a*(crop_dat**b) + c #MM
		if crop_model == "Inverse Kc": # Inverse Kc
			kc_ini = float(crop.kc_ini)
			kc_mid = float(crop.kc_mid)
			kc_end = float(crop.kc_end)
			cc_1 = float(crop.kc_cc_1)
			cc_2 = float(crop.kc_cc_2)
			cc_3 = float(crop.kc_cc_3)
			maturity = float((crop_dat/crop_growingperiod)*100)
			if maturity <= cc_1:
				Kc = kc_ini
			if maturity > cc_1 and maturity <= cc_2:
				Kc = kc_ini + ((kc_mid - kc_ini)/(cc_2-cc_1))*(maturity-cc_1)
			if maturity > cc_2:
				Kc = kc_mid + ((kc_end - kc_mid)/(100-cc_3))*(maturity-cc_3)
			if maturity < cc_2:
				Kc_adj = kc_ini + (kc_mid - kc_ini)*(maturity)/(cc_2)
			else: 
				Kc_adj =  kc_mid
			krz = float((Kc_adj - Kc)/(kc_mid - Kc))
			drz = float(crop_ro + krz*(crop_drz - crop_ro))*1000 #MM
		return round(drz)
	
	drz_collection = []

	intake_family = soil.intake_family
	irrigation_q = ""
	basin = selected_system.basin
	border = selected_system.border
	furrow = selected_system.furrow
	drip = selected_system.drip
	sprinkler = selected_system.sprinkler

	if furrow != None or basin != None or border != None: #Common values used by surface irrigation (e.g. basin, border, furrow)
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
		cons_a = round(-0.1831*rate**2 + 1.4917*rate + 0.486, 4)
		cons_b = round(0.0524*math.log(rate) + 0.7822, 3)
		cons_f = round(1.7926*rate + 7.0715, 2)
		cons_g = round (0.0003*rate + 0.00009, 7)
	if basin != None:
		irrigation_q = basin.discharge
	if furrow != None:
		irrigation_q = furrow.discharge
	if border != None:
		irrigation_q = border.discharge
		Qu = float(irrigation_q)
	if sprinkler != None:
		irrigation_q = sprinkler.discharge
	if drip != None:
		irrigation_q = drip.ave_discharge

	ea = ""
	crop_dat = 0
	mc_ave_collection = []
	Fn_collection = []
	drz = ""
	mci_1 = ""
	mci_2 = ""
	mci_3 = ""
	mc_ave = ""
	net_application_depth = 0
	irrigation_period = 0
	total_volume = 0
	area_shaded = 0

	if len(mc_1) > 0: # getting date from data of sensor 1
		for mc_obj in mc_1_sorted:
			mc_date = mc_obj.date
			crop_dat = ((mc_date - crop_transplanted).days)
			drz_collection.append(calculateDRZ(crop_dat))

		drz = calculateDRZ(crop_dat)

		def calculateMC_AVE_1(mc_a): # for fieldunit with 1 sensor only
			mc_ave = mc_a
			return round(mc_ave, 2)

		def calculateMC_AVE_2(drz, mc_a, mc_b): # for fieldunit with 2 sensors
			if drz <= depth_1:
				mc_ave = mc_a
			if drz > depth_1 and drz <= depth_2:
				mc_ave = ((mc_a*depth_1) + (mc_b*(drz-depth_1)))/(drz)
			else:
				mc_ave = ((mc_a*depth_1) + (mc_b*(depth_2-depth_1)))/depth_2
			return round(mc_ave, 2)

		def calculateMC_AVE_3(drz, mc_a, mc_b, mc_c): # for fieldunit with 3 sensors
			if drz <= depth_1:
				mc_ave = mc_a
			if drz > depth_1 and drz <= depth_2:
				mc_ave = ((mc_a*depth_1) + (mc_b*(drz-depth_1)))/(drz)
			else:
				mc_ave = ((mc_a*depth_1) + (mc_b*(depth_2-depth_1)) + (mc_c*(depth_3-depth_2)))/(depth_3)
			return round(mc_ave, 2)

		if num_sensors == 1:
			for (drz, mc_a) in zip(drz_collection, mc_collection_1):
				mc_ave = calculateMC_AVE_1(mc_a)
				mc_ave_collection.append(calculateMC_AVE_1(mc_a))
		if num_sensors == 2:
			for (drz, mc_a, mc_b) in zip(drz_collection, mc_collection_1, mc_collection_2):
				mc_ave = calculateMC_AVE_2(drz, mc_a, mc_b)
				mc_ave_collection.append(calculateMC_AVE_2(drz, mc_a, mc_b))
		if num_sensors == 3:
			for (drz, mc_a, mc_b, mc_c) in zip(drz_collection, mc_collection_1, mc_collection_2, mc_collection_3):
				mc_ave = calculateMC_AVE_3(drz, mc_a, mc_b, mc_c)
				mc_ave_collection.append(calculateMC_AVE_3(drz, mc_a, mc_b, mc_c))

		def calculateFn(x, y): #Calculate net application depth (Fn)
			if y > MC_TO_IRRIGATE:
				net_application_depth = 0
			else:
				net_application_depth = float((soil_fc - y/100)*x)
			return round(net_application_depth)

		
		for (x, y) in zip(drz_collection, mc_ave_collection):
			Fn_collection.append(calculateFn(x, y))
		
		net_application_depth = calculateFn(x, y)

		#IRRIGATION SYSTEM
		#BASIN
		if basin != None:
			if net_application_depth <= 0:
				irrigation_period = 0
				total_volume = 0
			else:
				unit_discharge =  float(irrigation_q/1000)
				basin_length = float(basin.basin_length)
				ea = float(basin.ea)

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
			slope = float(furrow.area_slope)
			furrow_spacing = float(furrow.furrow_spacing)
			furrow_length = float(furrow.furrow_length)
			mannings_coeff = float(furrow.mannings_coeff)
			discharge = float(irrigation_q)
			bln_open = furrow.bln_furrow_type
			P_adj = round(0.265*(discharge*mannings_coeff/slope**0.5)**0.425 + 0.227, 4)

			if net_application_depth <= 0:
				net_opportunity_time = 0
				advanced_time = 0
				irrigation_period = 0
			else:
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
			So = float(border.area_slope)
			Fn = float(net_application_depth)
			n = float(border.mannings_coeff)
			y = Fn - cons_c
			if y > 0:
				Tn = float(((y)/cons_a)**(1/cons_b))
			else:
				Tn = 0.0001 #JUST TO REMOVE FLOAT DIVISION ZERO
			if So <= 0.004:
				Tl = ((Qu**float(0.2))*n)/120*(So+((float(0.0094)*n*Qu**float(0.175)/((Tn**float(0.88))*(So**float(0.5))))**float(1.6)))
			if So > 0.004:
				Tl = (Qu**0.2)*(n**1.2)/(120*So**1.6)
			irrigation_period = Tn - Tl

		#SPRINKLER
		if sprinkler != None:
			Sl = float(sprinkler.sprinkler_spacing)
			Sm = float(sprinkler.lateral_spacing)
			ea = float(sprinkler.ea)/100
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
		#DRIP
		if drip != None:
			area_shaded = len(PercentShaded.objects.filter(fieldunit=fieldunit))
			if area_shaded == 0:
				area_shaded = float(10)
			else:
				area_shaded = PercentShaded.objects.filter(fieldunit=fieldunit).latest().area_shaded
			q = float(drip.ave_discharge)
			bln_single_lateral = drip.bln_single_lateral
			bln_ii = drip.bln_ii
			Np = float(drip.emitters_per_plant)
			Se = float(drip.emitter_spacing)
			Sp = float(drip.plant_spacing)
			So = float(drip.row_spacing)
			w = float(drip.wetted_dia)
			eu = float(drip.EU)
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
			if bln_ii == "yes":
				irrigation_interval = float(drip.irrigation_interval)
			else:
				Td = Etcrop*(Pd + 0.15*(1 - Pd))
				irrigation_interval = net_application_depth/Td
				if irrigation_interval <= 1:
					irrigation_interval = 1
			gross_volume_per_plant = (gross_application_depth*Sp*So/irrigation_interval) #(L/day)
			irrigation_period = (gross_volume_per_plant/(Np*q))*24*60
			total_volume = gross_volume_per_plant
			intake_family = None
		# No Irrigation Data #
		if furrow == None and basin == None and border == None and drip==None and sprinkler==None:
			farm = selected_system.farm
			farm_area = float(farm.farm_area)
			total_volume = net_application_depth * farm_area * float(0.20) #[Assumption]
		
	#FOR DISPLAY
		net_application_depth = round(net_application_depth, 2)
		irrigation_period = round(irrigation_period)
		total_volume = round(total_volume)
	soil_fc = soil.fc
	soil_pwp = soil.pwp
	crop_mad = round(crop.mad * 100)
	
	today= datetime.utcnow().replace(tzinfo=pytz.utc)

	context = {
		"today": today,
		"num_sensors": num_sensors,
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
		"crop_id": crop_id,
	}
	return render(request, 'waissapp/index.html', context)