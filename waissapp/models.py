from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


#SITE VALUES
class Personnel(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=11, null=True, blank=True)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)
    
    class Meta:
        verbose_name_plural = "Site: Personnel"
        ordering = ('last_name',)

#SITE VALUES
class Farm(models.Model):
    farm_name = models.CharField(max_length=20)
    province = models.CharField(max_length=50, null="True", blank="True")
    municipality = models.CharField(max_length=50, null="True", blank="True")
    brgy = models.CharField(max_length=50, verbose_name="Barangay", null="True", blank="True")
    lat = models.DecimalField(max_digits=9, decimal_places=6, verbose_name="Latitude (deg)", null="True", blank="True")
    longi = models.DecimalField(max_digits=9, decimal_places=6, verbose_name="Longitude (deg)", null="True", blank="True")

    class Meta:
        verbose_name_plural = "Site: Farms"
        ordering = ('farm_name',)

    def __str__(self):
        return self.farm_name
    
#SITE VALUES
class FieldUnit(models.Model):
    name = models.CharField(max_length=25, null=True, blank=True, verbose_name="Field Unit Name")
    class Meta:
        verbose_name_plural = "Site: Field Units"
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Site: Field Units"
        db_table = "fieldunits"

class SensorNumber(models.Model):
    fieldunit = models.ForeignKey (FieldUnit, related_name="fieldunits", on_delete=models.CASCADE, null=True, blank=True)
    sensor_name = models.CharField(max_length=30, verbose_name="Sensor Name", null=True)
    depth = models.DecimalField(max_digits=6, decimal_places=4, verbose_name="Depth, m")
    
    def __str__(self):
        return self.sensor_name

    class Meta:
        verbose_name_plural = "Site: Sensors"
        db_table = "sensors"

class MoistureContent(models.Model):
    fieldunit = models.ForeignKey(FieldUnit, on_delete=models.CASCADE, null=True, blank=True)
    sensor_name = models.ForeignKey(SensorNumber, on_delete=models.CASCADE, null=True, blank=True)
    raw_data = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Analog Reading", null=True)
    timestamp = models.DateTimeField(verbose_name='Time Measured', null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Site: Sensor Readings"
        get_latest_by = "timestamp"

class FieldUnitSettings(models.Model):
    fieldunit = models.ForeignKey (FieldUnit, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=30, verbose_name="Settings Name", null=True, blank=True)
    usk = models.CharField(verbose_name="Unique Security Key", max_length=8)
    fieldunitstatus = models.BooleanField(verbose_name="Field Unit Status", default=True)
    withirrigation = models.BooleanField(verbose_name="With Irrigation (?)", default=True)
    automaticthreshold = models.BooleanField(verbose_name="Automatic Threshold (?)", default=True)
    servernumber = PhoneNumberField(null=True, blank=True, unique=True)
    fieldunitnumber = PhoneNumberField(null=True, blank=True, unique=True)
    numberofsamples = models.DecimalField(max_digits=3, decimal_places=0, verbose_name="No. of Samples", null=True)
    sensorintegrationtime = models.TimeField(verbose_name="Sensor Integration Time")
    timestart = models.TimeField(verbose_name='Starting Time', null=True, blank=True)
    timestop = models.TimeField(verbose_name='Stopping Time', null=True, blank=True)
    delay = models.TimeField(verbose_name='Sending Delay', null=True, blank=True)
    clockcorrection = models.TimeField(verbose_name='Clock Correction', null=True, blank=True)

    class Meta:
        verbose_name_plural = "Site: Field Unit Settings"

#DATABASE
class Soil(models.Model):
    farm_name = models.ForeignKey(Farm, on_delete=models.CASCADE, null=True, blank=True)
    fieldunit = models.ForeignKey (FieldUnit, on_delete=models.CASCADE, null=True, blank=True)
    soiltype = models.CharField(max_length=25, verbose_name="Soil Type")
    fc = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="Field Capacity, %", null=True)
    pwp = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Permanent Wilting Point, %", null=True)
    As = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Apparent Specific Density, %", null=True)
    source = models.CharField(max_length=30, verbose_name="Data Source", null=True)
    def __str__(self):
        return self.soiltype

    class Meta:
        verbose_name_plural = "Database: Soil"
        ordering = ('soiltype',)

class CalibrationConstant(models.Model):
    calib_name = models.CharField(max_length=25, verbose_name="Calibration Name", null=True, blank=True)
    

    LINEAR = 'LIN'
    QUADRATIC = 'QUA'
    SYMMETRICAL_SIGMOIDAL = 'SSIG'
    ASYMMETRICAL_SIGMOIDAL = 'ASSIG'
    EXPONENTIAL = 'EXP'
    POWER = 'POW'
    LOGARITHMIC = 'LOG'

    CALIBRATION_EQUATION_CHOICES = [
        (LINEAR, 'Linear'),
        (QUADRATIC, 'Quadratic'),
        (SYMMETRICAL_SIGMOIDAL, 'Symmetrical Sigmoidal'),
        (ASYMMETRICAL_SIGMOIDAL, 'Asymmetrical Sigmoidal'),
        (EXPONENTIAL, 'Exponential'),
        (POWER, 'Power'),
        (LOGARITHMIC, 'Logarithmic'),
    ]

    calib_equation = models.CharField(
        max_length=5,
        choices=CALIBRATION_EQUATION_CHOICES,
        default=LINEAR,
        verbose_name="Equation Form"
    )

    calib_coeff_a = models.DecimalField(max_digits=20, decimal_places=4, verbose_name=" a", null=True, blank=True)
    calib_coeff_b = models.DecimalField(max_digits=20, decimal_places=4, verbose_name=" b", null=True, blank=True)
    calib_coeff_c = models.DecimalField(max_digits=20, decimal_places=4, verbose_name=" c", null=True, blank=True)
    calib_coeff_d = models.DecimalField(max_digits=20, decimal_places=4, verbose_name=" d", null=True, blank=True)
    calib_coeff_m = models.DecimalField(max_digits=20, decimal_places=4, verbose_name=" m", null=True, blank=True)
    date_tested = models.DateTimeField(verbose_name='Date Calibrated', null=True, blank=True)
    tested_by = models.CharField(max_length=30, verbose_name="Tested By", null=True, blank=True)

    def __str__(self):
        return self.calib_name
        
    class Meta:
        verbose_name_plural = "Site: Calibration Equation Constants"

#DATABASE
class IntakeFamily(models.Model):
    farm_name = models.ForeignKey(Farm, on_delete=models.CASCADE, verbose_name="Farm", null=True, blank=True)
    fieldunit = models.ForeignKey (FieldUnit, on_delete=models.CASCADE, verbose_name="Field Unit", null=True, blank=True)
    soil = models.ForeignKey(Soil, on_delete=models.CASCADE, verbose_name="Soil", null=True, blank=True)
    
    intakefamily = models.CharField(max_length=20, unique=True)
    coeff_a = models.DecimalField(max_digits=5, decimal_places=4, verbose_name=" a", null=True)
    coeff_b = models.DecimalField(max_digits=4, decimal_places=3, verbose_name=" b", null=True)
    coeff_c = models.DecimalField(max_digits=1, decimal_places=0, verbose_name=" c", null=True)
    coeff_f = models.DecimalField(max_digits=4, decimal_places=2, verbose_name=" f", null=True)
    coeff_g = models.DecimalField(max_digits=9, decimal_places=7, verbose_name=" g", null=True)
    source = models.CharField(max_length=30, verbose_name="Data Source", null=True)

    def __str__(self):
        return self.intakefamily

    class Meta:
        verbose_name_plural = "Database: Intake Families"

#DATABASE
class Crop(models.Model):
    crop = models.CharField(max_length=20, unique=True)
    date_transplanted = models.DateField(verbose_name='Date Transplanted', null=True, blank=True)
    growingperiod = models.DecimalField(max_digits=5, decimal_places=0, verbose_name="Growing Period, days", null=True, blank=True)
    mad = models.DecimalField(max_digits=3, decimal_places=2, verbose_name="Management Allowable Deficit", null=True, blank=True)
    drz = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Depth of Rootzone, m", null=True)
    kc_ini = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Kc (ini)", null=True, blank=True)
    kc_mid = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Kc (mid)", null=True, blank=True)
    kc_end = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Kc (end)", null=True, blank=True)
    kc_cc_1 = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Kc curve cutoff (1)", null=True, blank=True)
    kc_cc_2 = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Kc curve cutoff (2)", null=True, blank=True)
    kc_cc_3 = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Kc curve cutoff (3)", null=True, blank=True)

    CHOICES = [
        ("linear", 'linear'),
        ("quadratic", 'quadratic'),
    ]

    eqnform = models.CharField(choices=CHOICES, max_length=20, verbose_name="Equation Form", null=True, blank=True)                          
    root_a = models.DecimalField(max_digits=15, decimal_places=5, verbose_name=" a", null=True, blank=True)
    root_b = models.DecimalField(max_digits=15, decimal_places=5, verbose_name=" b", null=True, blank=True)
    root_c = models.DecimalField(max_digits=15, decimal_places=5, verbose_name=" c", null=True, blank=True)
    
    root_ini = models.DecimalField(max_digits=15, decimal_places=5, verbose_name="Root Depth during Transplant (m)", null=True, blank=True)
    def __str__(self):
        return self.crop

    class Meta:
        verbose_name_plural = "Database: Crop"
        ordering = ('crop',)


#SITE VALUES


class BasinPara(models.Model):
    basin_name = models.CharField(max_length=30, verbose_name="Basin Irrigation System Filename", null=True, blank=True)
    discharge = models.DecimalField(max_digits=20, decimal_places=4, verbose_name="Unit Discharge (lps)", null=True, blank=True)
    basin_length = models.DecimalField(max_digits=20, decimal_places=4, verbose_name="Basin Length (m)", null=True, blank=True)
    
    #this has database, pwede na tanggalin pag nalagay na sa views.py ang values ng R
    EFF_CHOICES = [
        (50, '50'),
        (55, '55'),
        (60, '60'),
        (70, '70'),
        (75, '75'),
        (80, '80'),
        (85, '85'),
        (90, '90'),
        (95, '95'),
    ]

    ea = models.DecimalField(choices=EFF_CHOICES, max_digits=5, decimal_places=2, verbose_name="Application Efficiency (%)", help_text="Application efficiency is the fraction of the irrigation water that is used by the crop. Provided there are no runoff losses, the application efficiency (%) is the required irrigation depth (mm), divided by the average applied irrigation depth (mm), multiplied by 100%.", null=True)
    class Meta:
        verbose_name_plural = "Irrigation System: Basin"
    def __str__(self):
        return self.basin_name

class BorderPara(models.Model):
    border_name = models.CharField(max_length=30, verbose_name="System Name", null=True, blank=True)
    discharge = models.DecimalField(max_digits=20, decimal_places=4, verbose_name="Unit Discharge (lps)", null=True, blank=True)
    border_width = models.DecimalField(max_digits=20, decimal_places=4, verbose_name="Border Width (m)", null=True, blank=True)
    num_of_border_strips = models.DecimalField(max_digits=20, decimal_places=4, verbose_name="Number of Borders", null=True, blank=True)
    mannings_coeff = models.DecimalField(max_digits=20, decimal_places=4, verbose_name="Manning's coefficient", null=True, blank=True)
    area_slope = models.DecimalField(max_digits=20, decimal_places=4, verbose_name="Slope", null=True, blank=True)
    
    #this has database
    EFF_CHOICES = [
        (50, '50'),
        (55, '55'),
        (60, '60'),
        (70, '70'),
        (75, '75'),
        (80, '80'),
        (85, '85'),
        (90, '90'),
        (95, '95'),
    ]

    ea = models.DecimalField(choices=EFF_CHOICES, max_digits=5, decimal_places=2, verbose_name="Application Efficiency (%)", null=True, blank=True)
    flow_rate_per_strip = models.DecimalField(max_digits=20, decimal_places=4, verbose_name="Flow rate per border strip (lps)", null=True, blank=True)
    total_flow_rate = models.DecimalField(max_digits=20, decimal_places=4, verbose_name="Total flow rate (lps)", null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Irrigation System: Border"
    def __str__(self):
        return self.border_name

class FurrowPara(models.Model):
    name = models.CharField(max_length=30, verbose_name="System Name", null=True, blank=True)
    bln_furrow_type = models.BooleanField (verbose_name="It is an open-ended furrow.")
    discharge = models.DecimalField(max_digits=20, decimal_places=4, verbose_name="Unit Discharge (lps)", null=True, blank=True)
    area_slope = models.DecimalField(max_digits=20, decimal_places=4, verbose_name="Slope", null=True, blank=True)
    #p_adjusted = models.DecimalField(max_digits=20, decimal_places=4, verbose_name="P adjusted (m)", null=True) #doublecheck details
    #just insert in js computation
    class Meta:
        verbose_name_plural = "Irrigation System: Furrow"
    def __str__(self):
        return self.name

class DripPara(models.Model):
    name = models.CharField(max_length=30, verbose_name="System Name", null=True, blank=True)
    bln_single_lateral = models.BooleanField (verbose_name="Is a Single Straight Lateral type.")
    #if bln_single_lateral is true
    emitters_per_plant = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="No. of Emitters per Plant", null=True, blank=True)
    emitter_spacing = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Emitter Spacing (m)", null=True, blank=True)
    #if bln_single_lateral is false
    plant_spacing = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Plant spacing (m)", null=True, blank=True)
    row_spacing = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Row spacing (m)", null=True, blank=True)
    wetted_dia = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Wetted diameter (m)", null=True, blank=True)
    #
    EU = models.DecimalField(max_digits=3, decimal_places=3, verbose_name="Design Emission Uniformity", null=True, blank=True)
    irrigation_interval = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Irrigation Interval (days)", null=True, blank=True)
    class Meta:
        verbose_name_plural = "Irrigation System: Drip"
    def __str__(self):
        return self.name

class SprinklerPara(models.Model):
    name = models.CharField(max_length=30, verbose_name="System Name", null=True, blank=True)
    farm_area = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Farm area (sq.m)", null=True, blank=True)
    area_irrigated_at_a_time = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Area irrigated at a time (sq.m)", null=True, blank=True)
    lateral_spacing = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Lateral spacing (m)", null=True, blank=True)
    sprinkler_spacing = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Sprinkler spacing (m)", null=True, blank=True)
    num_of_sprinklers = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Number of sprinklers", null=True, blank=True)
    ea = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Application Efficiency", null=True, blank=True)
    sprinkler_discharge = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Sprinkler Discharge (lps)", null=True, blank=True)
    class Meta:
        verbose_name_plural = "Irrigation System: Sprinkler"
    def __str__(self):
        return self.name

class FarmSummaries(models.Model):
    name = models.CharField(max_length=30, verbose_name="System", unique="True", null=True, blank=True)
    farm_name = models.ForeignKey(Farm, on_delete=models.CASCADE, verbose_name="Farm", null=True, blank=True)
    fieldunit = models.ForeignKey (FieldUnit, on_delete=models.CASCADE, verbose_name="Field Unit", null=True, blank=True)
    farm_manager = models.ForeignKey(Personnel, on_delete=models.CASCADE, verbose_name="Manager", null=True, blank=True)
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, null=True, blank=True)
    soil = models.ForeignKey(Soil, on_delete=models.CASCADE, null=True, blank=True)
    intakefamily = models.ForeignKey(IntakeFamily, on_delete=models.CASCADE, verbose_name="Intake Family", null=True, blank=True)
    calib_eqn = models.ForeignKey(CalibrationConstant, on_delete=models.CASCADE, verbose_name="Calibration", null=True, blank=True)
    basin_sys = models.ForeignKey(BasinPara, on_delete=models.CASCADE, verbose_name="Irrigation", null=True, blank=True)
    border_sys = models.ForeignKey(BorderPara, on_delete=models.CASCADE, verbose_name="Irrigation", null=True, blank=True)
    furrow_sys = models.ForeignKey(FurrowPara, on_delete=models.CASCADE, verbose_name="Irrigation", null=True, blank=True)
    sprinkler_sys = models.ForeignKey(SprinklerPara, on_delete=models.CASCADE, verbose_name="Irrigation", null=True, blank=True)
    drip_sys = models.ForeignKey(DripPara, on_delete=models.CASCADE, verbose_name="Irrigation", null=True, blank=True)
    settings = models.ForeignKey(FieldUnitSettings, on_delete=models.CASCADE, verbose_name="Settings", null=True, blank=True)

    class Meta:
        verbose_name_plural = "Site: Farm Summaries"
    def __str__(self):
        return self.name
    
class BasinComp(models.Model):
    system = models.ForeignKey (FarmSummaries, on_delete=models.CASCADE, null=True, blank=True)                  
    eff_adv_ratio = models.DecimalField(max_digits=3, decimal_places=2, verbose_name="R", null=True)
    net_app_depth = models.DecimalField(max_digits=20, decimal_places=4, verbose_name="Net Application Depth (mm)", null=True)
    net_opp_time = models.DecimalField(max_digits=20, decimal_places=4, verbose_name="Net Opportunity Time (mins)", null=True)
    inflow_time = models.DecimalField(max_digits=20, decimal_places=4, verbose_name="Inflow Time (mins)", null=True)
    advance_time = models.DecimalField(max_digits=20, decimal_places=4, verbose_name="Advance Time (mins)", null=True)
    irrigation_period = models.DecimalField(max_digits=20, decimal_places=4, verbose_name="Irrigation Period (mins)", null=True)

    class Meta:
        verbose_name_plural = "Computation: Basin"

class BorderComp(models.Model):
    system = models.ForeignKey (FarmSummaries, on_delete=models.CASCADE, null=True, blank=True)  
    
    net_app_depth = models.DecimalField(max_digits=20, decimal_places=4, verbose_name="Net Application Depth (mm)", null=True)
    net_opp_time = models.DecimalField(max_digits=20, decimal_places=4, verbose_name="Net Opportunity Time (mins)", null=True)
    lag_time = models.DecimalField(max_digits=20, decimal_places=4, verbose_name="Lag Time (mins)", null=True)
    inflow_time = models.DecimalField(max_digits=20, decimal_places=4, verbose_name="Inflow Time (mins)", null=True)
    irrigation_period = models.DecimalField(max_digits=20, decimal_places=4, verbose_name="Irrigation Period (mins)", null=True)
    
    class Meta:
        verbose_name_plural = "Computation: Border"

class FurrowComp(models.Model):
    system = models.ForeignKey (FarmSummaries, on_delete=models.CASCADE, null=True, blank=True)  
    
    net_app_depth = models.DecimalField(max_digits=20, decimal_places=4, verbose_name="Net Application Depth (mm)", null=True)
    net_opp_time = models.DecimalField(max_digits=20, decimal_places=4, verbose_name="Net Opportunity Time (mins)", null=True)
    advance_time = models.DecimalField(max_digits=20, decimal_places=4, verbose_name="Advance Time (mins)", null=True)
    #if bln_furrow_type is true, irrigation period is equal to net opportunity time
    irrigation_period = models.DecimalField(max_digits=20, decimal_places=4, verbose_name="Irrigation Period (mins)", null=True)
    class Meta:
        verbose_name_plural = "Computation: Furrow"

class SprinklerComp(models.Model):
    system = models.ForeignKey (FarmSummaries, on_delete=models.CASCADE, null=True, blank=True)  

    name = models.CharField(max_length=30, verbose_name="System Name", null=True, blank=True)
    farm_area = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Farm area (sq.m)", null=True)
    area_irrigated_at_a_time = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Area irrigated at a time (sq.m)", null=True)
    lateral_spacing = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Lateral spacing (m)", null=True)
    sprinkler_spacing = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Sprinkler spacing (m)", null=True)
    num_of_sprinklers = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Number of sprinklers", null=True)
    ea = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Application Efficiency", null=True)
    #Is operating pressure known?
    bln_operating_pressure = models.BooleanField (verbose_name="Is the operating pressure known?")
    #If yes, then
    operating_pressure = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Operating Pressure (kPa)", null=True)
    nozzle_dia = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Nozzle diameter (mm)", help_text="Fill-out only if operating pressure is known.", null=True)
    discharge_coefficient = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Discharge Coefficient", help_text="Fill-out only if operating pressure is known.", null=True)
    #
    sprinkler_discharge = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Sprinkler Discharge (lps)", help_text="Fill-out if operating pressure is unknown.", null=True)
    #
    net_app_depth = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Net Application Depth (mm)", null=True)
    gross_app_depth = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Gross Application Depth (mm)", null=True)
    application_rate = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Application Rate (lps/sq.m)", null=True)
    #If application rate is less than FC, then irrigation rate is equal to FC. Insert if then statement in views.py for this.
    irrigation_rate = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Irrigation Rate (lps/sq.m)", null=True)
    irrigation_period = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Irrigation Period (mins)", null=True)
    
    class Meta:
        verbose_name_plural = "Computation: Sprinkler"

class DripComp(models.Model):
    system = models.ForeignKey (FarmSummaries, on_delete=models.CASCADE, null=True, blank=True)  

    percent_wetted_area  = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Percent Wetted Diameter (%)", null=True)
    bln_pw_between_33_and_50 = models.BooleanField (verbose_name="Is the Percent Wetted Perimeter between 33 to 50 percent?")
    #Insert recommendation to redesign system?
    net_app_depth = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Net Application Depth (mm)", null=True)

    bln_compute_EU = models.BooleanField (verbose_name="Design Emission Uniformity unknown, compute!")
    #if compute EU true
    ave_emitter_discharge = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Average emitter discharge (lps)", null=True)
    min_emitter_discharge = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Minimum emitter discharge (lps)", null=True)
    
    #if bln_compute_emitter_coeff is true, make form for inputting table of discharge data
    bln_compute_emitter_coeff = models.BooleanField (verbose_name="Emitter coefficient unknown, compute!")
    emitter_coeff = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Emitter coefficient", help_text="Input emitter coefficient if known.", null=True)
    transpiration_requirement = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Transpiration Requirement (?)", null=True)
    gross_app_depth = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Gross Application Depth (mm)", null=True)
    #
    bln_prefers_irrig_interval = models.BooleanField (verbose_name="Have preffered irrigation interval.")
    #if bln_prefers_irrig_interval false
    #input crop characteristics
    percent_shaded = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Percent Shaded (%)", null=True)
    peak_ETo  = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Peak Evapotranspiration (mm)", null=True)
    ave_peak_daily_transpiration = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Average Peak Daily Transpiration Rate", null=True)
    #
    gross_volume_required_per_plant = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Gross Volume Required per Plant (l)", null=True)
    irrigation_period = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Irrigation Peiod (mins)", null=True)

    timestamp = models.DateTimeField(verbose_name='Time Measured', null=True, blank=True)

    class Meta:
        verbose_name_plural = "Computation: Drip"
        get_latest_by = "timestamp"

#MESSAGES
class Receiver(models.Model):#FOREIGNKEY PERSONNEL??? FIELDUNIT SETTINGS??
    receiver_number = PhoneNumberField(null=True, blank=True)
    def __str__(self):
        return str(self.receiver_number)

class Sender(models.Model):
    sender_number = PhoneNumberField(null=True, blank=True)
    def __str__(self):
        return str(self.sender_number)

class SentMsgs(models.Model):
    msg = models.TextField(max_length=200)
    usk = models.CharField(verbose_name="Unique Security Key", max_length=8)
    receiver_number = models.ForeignKey(Receiver, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Receiver")
    sender_number = models.ForeignKey(Sender, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Sender")
    fieldunit_number =PhoneNumberField(null=True, blank=True) #foreignkey field unit settings?
    timestamp = models.DateTimeField(verbose_name='Date/Time Sent', null=True, blank=True)

    class Meta:
        verbose_name_plural = "Messages: Sent"
        get_latest_by = "timestamp"

class ReceivedMsgs(models.Model):
    msg = models.TextField(max_length=200)
    usk = models.CharField(verbose_name="Unique Security Key", max_length=8)
    receiver_number = models.ForeignKey(Receiver, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Receiver")
    sender_number = models.ForeignKey(Sender, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Sender")
    fieldunit_number = PhoneNumberField(null=True, blank=True)
    timestamp = models.DateTimeField(verbose_name='Time Sent', null=True, blank=True)

    class Meta:
        verbose_name_plural = "Messages: Received"
        get_latest_by = "timestamp"

