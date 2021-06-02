from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Personnel(models.Model):
    first_name = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=30, null=True)
    number = models.IntegerField(null=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, blank=True)
    personal = models.BooleanField(default=True)
    timestamp =  models.DateTimeField(verbose_name="Date Created", null=True, auto_now_add=True)

    def __str__(self):
        return str(self.number)
    
    class Meta:
        verbose_name_plural = "2. Farm Managers"
        ordering = ('last_name',)
    
class FieldUnit(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True, verbose_name="Field Unit Name")
    usk = models.CharField(verbose_name="Unique Security Key", max_length=8, null=True, blank=True)
    number = models.IntegerField(verbose_name="Field Unit Number", null=True, blank=True)
    fieldunitstatus = models.BooleanField(verbose_name="Field Unit Status", default=True)
    withirrigation = models.BooleanField(verbose_name="With Irrigation (?)", default=True)
    automaticthreshold = models.BooleanField(verbose_name="Automatic Threshold (?)", default=True)
    samples = models.DecimalField(max_digits=3, decimal_places=0, verbose_name="No. of Samples", null=True, blank=True)
    sensorintegrationtime = models.IntegerField(verbose_name='Sensor Integration Time (ms)', null=True, blank=True)
    timestart = models.TimeField(verbose_name='Starting Time', null=True, blank=True)
    timestop = models.TimeField(verbose_name='Stopping Time', null=True, blank=True)
    delay = models.IntegerField(verbose_name='Sending Delay (ms)', null=True, blank=True)
    clockcorrection = models.IntegerField(verbose_name='Clock Correction (s)', null=True, blank=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, blank=True)
    personal = models.BooleanField(default=True)
    timestamp =  models.DateTimeField(verbose_name="Date Created", null=True, auto_now_add=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "6. Field Units"
        ordering = ('name',)

class Sensor(models.Model):
    name = models.CharField(max_length=30, verbose_name="Sensor Name", null=True)
    fieldunit = models.ForeignKey (FieldUnit, on_delete=models.CASCADE, verbose_name="Field Unit", null=True)
    depth = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Depth, m", null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "8. Sensors"
        ordering = ('name',)

class MoistureContent(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(verbose_name='Date & Time Measured', null=True, help_text="Format: mm/dd/yyyy hh:mm")
    mc_data = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Analog Reading", null=True)

    class Meta:
        verbose_name_plural = "9. Moisture Content"
        get_latest_by = "timestamp"
    def __str__(self):
        return str(self.sensor)

class Soil(models.Model):
    soiltype = models.CharField(max_length=25, verbose_name="Soil")
    fc = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="Field Capacity (% vol)", null=True)
    pwp = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Permanent Wilting Point (% vol)", null=True)

    clay_005= 'clay_005)'
    clay_01= 'clay_01'
    clay_015= 'clay_015'
    clay_loam_02=  'clay_loam_02'
    clay_loam_025= 'clay_loam_025'
    clay_loam_03= 'clay_loam_03'
    silty_035= 'silty_035'
    silty_04= 'silty_04'
    silty_loam_045= 'silty_loam_045'
    silty_loam_05= 'silty_loam_05'
    silty_loam_06 = 'silty_loam_06'
    silty_loam_07= 'silty_loam_07'
    sandy_loam_08= 'sandy_loam_08'
    sandy_loam_09= 'sandy_loam_09'
    sandy_loam_10 = 'sandy_loam_10'
    sandy_15= 'sandy_15'
    sandy_20= 'sandy_20'

    choices = [
        (clay_005, 'clay (0.5)'),
        (clay_01, 'clay (0.1)'),
        (clay_015, 'clay (0.15)'),
        (clay_loam_02,  'clay loam (0.2)'),
        (clay_loam_025, 'clay loam (0.25)'),
        (clay_loam_03, 'clay loam (0.3)'),
        (silty_035, 'silty (0.35)'),
        (silty_04, 'silty (0.4)'),
        (silty_loam_045, 'silty loam (0.45)'),
        (silty_loam_05, 'silty loam (0.5)'),
        (silty_loam_06 , 'silty loam (0.6)'),
        (silty_loam_07, 'silty loam (0.7)'),
        (sandy_loam_08 , 'sandy loam (0.8)'),
        (sandy_loam_09, 'sandy loam (0.9)'),
        (sandy_loam_10 , 'sandy loam (1.0)'),
        (sandy_15 , 'sandy (1.5)'),
        (sandy_20 , 'sandy (2.0)')
    ]

    intake_family = models.CharField(max_length=30,choices=choices,verbose_name="Intake Family",null=True, blank=True, help_text="The number indicates the intake rate of the soil. Required for surface irrigations- basin, border, and furrow.")
    source = models.CharField(max_length=30, verbose_name="Data Source", null=True, blank=True)
    timestamp =  models.DateTimeField(verbose_name="Date Created", null=True, auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, blank=True)
    personal = models.BooleanField(default=True)

    def __str__(self):
        return self.soiltype

    class Meta:
        verbose_name_plural = "4. Soil"
        ordering = ('soiltype',)

class CalibrationConstant(models.Model):
    name = models.CharField(max_length=25, verbose_name="File Name", unique=True, null=True)
    LINEAR = 'linear'
    QUADRATIC = 'quadratic'
    SYMMETRICAL_SIGMOIDAL = 'symmetrical sigmoidal'
    ASYMMETRICAL_SIGMOIDAL = 'asymmetrical sigmoidal'
    EXPONENTIAL = 'exponential'
    LOGARITHMIC = 'logarithmic'

    CALIBRATION_EQUATION_CHOICES = [
        (LINEAR, 'Linear'),
        (QUADRATIC, 'Quadratic'),
        (EXPONENTIAL, 'Exponential'),
        (LOGARITHMIC, 'Logarithmic'),
        (SYMMETRICAL_SIGMOIDAL, 'Symmetrical Sigmoidal'),
        (ASYMMETRICAL_SIGMOIDAL, 'Asymmetrical Sigmoidal'),
    ]

    calib_equation = models.CharField(
        max_length=30,
        choices=CALIBRATION_EQUATION_CHOICES,
        default=LINEAR,
        verbose_name="Equation Form", null=True,
    )

    coeff_a = models.DecimalField(max_digits=20, decimal_places=4, verbose_name=" a", null=True)
    coeff_b = models.DecimalField(max_digits=20, decimal_places=4, verbose_name=" b", null=True)
    coeff_c = models.DecimalField(max_digits=20, decimal_places=4, verbose_name=" c", null=True, blank=True)
    coeff_d = models.DecimalField(max_digits=20, decimal_places=4, verbose_name=" d", null=True, blank=True)
    coeff_m = models.DecimalField(max_digits=20, decimal_places=4, verbose_name=" m", null=True, blank=True)
    date_tested = models.DateTimeField(verbose_name='Date Calibrated', null=True, blank=True)
    tested_by = models.CharField(max_length=30, verbose_name="Tested By", null=True, blank=True)
    timestamp =  models.DateTimeField(verbose_name="Date Created", null=True, auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, blank=True)
    personal = models.BooleanField(default=True)

    def __str__(self):
        return self.name
        
    class Meta:
        verbose_name_plural = "7. Calibration Equations"
        ordering = ('name',)

class Crop(models.Model):
    crop = models.CharField(max_length=100, unique=True, null=True,)
    growingperiod = models.IntegerField(verbose_name="Growing Period, days", null=True,)
    mad = models.DecimalField(max_digits=3, decimal_places=2, verbose_name="Management Allowable Deficit", null=True,)
    drz = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Depth of Rootzone, m", null=True,)
    peak_Etcrop = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Peak Evapotranspiration (mm/day)", null=True, blank=True)
    transpiration_ratio = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Transpiration Ratio", null=True, blank=True)

    rooting = [
        ("Borg-Grimes Model", 'Borg-Grimes Model'),
        ("User-Defined", 'User-Defined'),
        ("Inverse Kc", 'Inverse Kc'),
    ]

    root_growth_model = models.CharField(choices=rooting, max_length=30, verbose_name="Root Growth Model", null=True, help_text="Fillout additional information below.")
    kc_ini = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Kc (ini)", null=True, blank=True)
    kc_mid = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Kc (med)", null=True, blank=True)
    kc_end = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Kc (end)", null=True, blank=True)
    kc_cc_1 = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Curve cutoff 1", null=True, blank=True)
    kc_cc_2 = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Curve cutoff 2", null=True, blank=True)
    kc_cc_3 = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Curve cutoff 3", null=True, blank=True)
    source = models.CharField(max_length=30, verbose_name="Data Source", null=True, blank=True)

    CHOICES = [
        ("linear", 'linear'),
        ("quadratic", 'quadratic'),
    ]

    eqnform = models.CharField(choices=CHOICES, max_length=20, verbose_name="Equation Form", null=True, blank=True)                          
    root_a = models.DecimalField(max_digits=15, decimal_places=5, verbose_name=" a", null=True, blank=True)
    root_b = models.DecimalField(max_digits=15, decimal_places=5, verbose_name=" b", null=True, blank=True)
    root_c = models.DecimalField(max_digits=15, decimal_places=5, verbose_name=" c", null=True, blank=True)
    root_ini = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Root Depth during Transplant (m)", null=True, blank=True)
    
    timestamp =  models.DateTimeField(verbose_name="Date Created", null=True, auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, blank=True)
    personal = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "3. Crops"
        ordering = ('crop',)
    
    def __str__(self):
        return self.crop


class Basin(models.Model):
    name= models.CharField(max_length=30, verbose_name="File Name", unique=True, null=True,)
    discharge = models.DecimalField(max_digits=20, decimal_places=2, verbose_name="Unit Discharge (lps)", null=True)
    basin_length = models.DecimalField(max_digits=20, decimal_places=4, verbose_name="Basin Length (m)", null=True)
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
    ea = models.DecimalField(choices=EFF_CHOICES, max_digits=5, decimal_places=2, verbose_name="Application Efficiency (%)", null=True)
    timestamp =  models.DateTimeField(verbose_name="Date Created", null=True, auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, blank=True)
    personal = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "5.a. Irrigation System: Basin"
    def __str__(self):
        return self.name

class Furrow(models.Model):
    name= models.CharField(max_length=30, verbose_name="File Name", unique=True, null=True)
    discharge = models.DecimalField(max_digits=20, decimal_places=2, verbose_name="Unit Discharge (lps)", null=True)
    mannings_coeff = models.DecimalField(max_digits=20, decimal_places=4, verbose_name="Manning's coefficient", null=True)
    area_slope = models.DecimalField(max_digits=20, decimal_places=4, verbose_name="Slope (m/m)", null=True)
    bln_furrow_type = models.BooleanField (verbose_name="It is an open-ended furrow.", null=True)
    furrow_spacing = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Furrow Spacing", null=True)
    furrow_length = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Furrow Length", null=True)
    timestamp =  models.DateTimeField(verbose_name="Date Created", null=True, auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, blank=True)
    personal = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "5.c. Irrigation System: Furrow"
    def __str__(self):
        return self.name

class Border(models.Model):
    name= models.CharField(max_length=30, verbose_name="File Name", unique=True, null=True)
    discharge = models.DecimalField(max_digits=20, decimal_places=2, verbose_name="Unit Discharge (lps)", null=True)
    mannings_coeff = models.DecimalField(max_digits=20, decimal_places=4, verbose_name="Manning's coefficient", null=True)
    area_slope = models.DecimalField(max_digits=20, decimal_places=4, verbose_name="Slope (m/m)", null=True)
    timestamp =  models.DateTimeField(verbose_name="Date Created", null=True, auto_now_add=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, blank=True)
    personal = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "5.b. Irrigation System: Border"
    def __str__(self):
        return self.name

class Drip(models.Model):
    name= models.CharField(max_length=30, verbose_name="File Name", unique=True, null=True,)
    bln_single_lateral = models.BooleanField (verbose_name="Single Straight Lateral", null=True)
    discharge = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Emitter Discharge (l/day)", null=True)
    emitters_per_plant = models.DecimalField(max_digits=5, decimal_places=0, verbose_name="No. of Emitters per Plant", null=True)
    emitter_spacing = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Emitter Spacing (m)", null=True)
    plant_spacing = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Plant spacing (m)", null=True)
    row_spacing = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Row spacing (m)", null=True)
    wetted_dia = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Wetted diameter (m)", null=True)
    bln_ii = models.BooleanField(verbose_name="Has preferred irrigation interval", null=True)
    irrigation_interval = models.DecimalField(max_digits=5, decimal_places=0, verbose_name="Irrigation Interval (days)", null=True, blank=True, help_text="Fillout only if you have preferred irrigation interval based on your farm schedule.")
    EU = models.DecimalField(max_digits=3, decimal_places=3, verbose_name="Design Emission Uniformity", null=True, blank=True)
    timestamp =  models.DateTimeField(verbose_name="Date Created", null=True, auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True)
    personal = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "5.e. Irrigation System: Drip"
    def __str__(self):
        return self.name

class Sprinkler(models.Model):
    name= models.CharField(max_length=30, verbose_name="File Name", unique=True, null=True,)
    discharge = models.DecimalField(max_digits=20, decimal_places=2, verbose_name="Unit Discharge (lps)", null=True, blank=True)
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
    ea = models.DecimalField(choices=EFF_CHOICES, max_digits=5, decimal_places=2, verbose_name="Application Efficiency (%)", null=True)
    lateral_spacing = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Lateral spacing (m)", null=True)
    sprinkler_spacing = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Sprinkler spacing (m)", null=True)
    bln_sprinkler_discharge = models.BooleanField(verbose_name="Compute Sprinkler Discharge", null=True, blank=True)
    nozzle_diameter = models.DecimalField(max_digits=5, decimal_places=4, verbose_name="Nozzle Diameter (cm)", null=True, blank=True)
    operating_pressure = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Operating Pressure (kPa)", null=True, blank=True)
    discharge_coefficient = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Discharge Coefficient", null=True, blank=True, help_text="Common values: 0.95 - 0.98")
    timestamp =  models.DateTimeField(verbose_name="Date Created", null=True, auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, blank=True)
    personal = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "5.d. Irrigation System: Sprinkler"
    def __str__(self):
        return self.name

class Farm(models.Model):
    name = models.CharField(max_length=20)
    province = models.CharField(max_length=50, null="True", blank="True")
    municipality = models.CharField(max_length=50, null="True", blank="True")
    brgy = models.CharField(max_length=50, verbose_name="Barangay", null="True", blank="True")
    lat = models.CharField(max_length=50, verbose_name="Latitude", null="True", blank="True")
    long = models.CharField(max_length=50, verbose_name="Longitude", null="True", blank="True")
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, blank=True)
    personal = models.BooleanField(default=True)
    timestamp =  models.DateTimeField(verbose_name="Date Created", null=True, auto_now_add=True)

    class Meta:
        verbose_name_plural = "1. Farms"
        ordering = ('name',)
        get_latest_by = "timestamp"

    def __str__(self):
        return self.name

class WAISSystems(models.Model):
    name = models.CharField(max_length=50)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, verbose_name="Farm", null=True)
    farm_manager = models.ForeignKey(Personnel, on_delete=models.CASCADE, verbose_name="Farm Manager", null=True)
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, null=True)
    date_transplanted = models.DateField(verbose_name='Date Transplanted', null=True,)
    soil = models.ForeignKey(Soil, on_delete=models.CASCADE, null=True)
    fieldunit = models.ForeignKey(FieldUnit, on_delete=models.CASCADE, verbose_name="Field Unit", null=True)
    calib = models.ForeignKey(CalibrationConstant, on_delete=models.CASCADE, verbose_name="Calibration Equation", null=True)
    basin = models.ForeignKey(Basin, on_delete=models.CASCADE, verbose_name="Basin System", null=True, blank=True)
    border = models.ForeignKey(Border, on_delete=models.CASCADE, verbose_name="Border System", null=True, blank=True)
    furrow = models.ForeignKey(Furrow, on_delete=models.CASCADE, verbose_name="Furrow System", null=True, blank=True)
    drip = models.ForeignKey(Drip, on_delete=models.CASCADE, verbose_name="Drip System", null=True, blank=True)
    sprinkler = models.ForeignKey(Sprinkler, on_delete=models.CASCADE, verbose_name="Sprinkler System", null=True, blank=True)    
    timestamp =  models.DateTimeField(verbose_name="Date Created", null=True, auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, blank=True)
    personal = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "0. WAISSystems"
        ordering = ('name',)
        get_latest_by = "timestamp"
    def __str__(self):
        return self.name

#MESSAGES
class ReceivedMsgs(models.Model):
    number = models.ForeignKey(Personnel, on_delete=models.CASCADE, null=True, blank=True)
    msg = models.TextField(max_length=200, verbose_name="Message", null=True, blank=True)
    timestamp = models.DateTimeField(verbose_name='Date/Time Sent', auto_now_add=True, null=True, blank=True)
    marker = models.BooleanField(default=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, blank=True)
    personal = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Messages: Received"
        get_latest_by = "timestamp"
    def __str__(self):
        return str(self.number)

class SentMsgs(models.Model):
    number = models.ForeignKey(Personnel, on_delete=models.CASCADE, null=True, blank=True)
    msg = models.TextField(max_length=200, verbose_name="Message", null=True, blank=True)
    sent = models.BooleanField(verbose_name="Sent?", default=False)
    timestamp = models.DateTimeField(verbose_name='Date/Time Sent', auto_now_add=True, null=True, blank=True)
    marker = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, blank=True)
    personal = models.BooleanField(default=True)
    class Meta:
        verbose_name_plural = "Messages: Sent"
        get_latest_by = "timestamp"
    def __str__(self):
        return str(self.number)

class Rainfall(models.Model):
    fieldunit = models.ForeignKey (FieldUnit, on_delete=models.CASCADE, verbose_name="Field Unit", null=True, blank=True)
    amount = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Rainfall (mm)", null=True, blank=True)
    timestamp = models.DateTimeField(verbose_name='Date & Time', null=True, blank=True)

class Gravimetric(models.Model):
    fieldunit = models.ForeignKey(FieldUnit, on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(verbose_name='Date & Time', null=True, help_text="Format: mm/dd/yyyy hh:mm (should be an exact counterpart on MCv datapoints)")
    mc_data = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="MCv (%)", null=True)
    note = models.CharField(max_length=100, verbose_name="Remarks", null=True, blank=True)

class PercentShaded(models.Model):
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, verbose_name="Crop", null=True)
    area_shaded =  models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Area Shaded (%)", null=True)
    date =  models.DateField(verbose_name="Date", null=True)
    class Meta:
        verbose_name_plural = "Percent Area Shaded"
        get_latest_by = "date"