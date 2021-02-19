from django.db import models

#SITE VALUES
class Personnel(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    number = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.number)
    
    class Meta:
        verbose_name_plural = "Site: Farm Managers"
        ordering = ('last_name',)
    
#SITE VALUES
class FieldUnit(models.Model):
    name = models.CharField(max_length=25, null=True, blank=True, verbose_name="Field Unit Name")
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

    def __str__(self):
        return '{}'.format(self.number)
    class Meta:
        verbose_name_plural = "Site: Field Units"

class Sensor(models.Model):
    fieldunit = models.ForeignKey (FieldUnit, on_delete=models.CASCADE, verbose_name="Field Unit", null=True, blank=True)
    name = models.CharField(max_length=30, verbose_name="Sensor Name", null=True)
    depth = models.DecimalField(max_digits=6, decimal_places=4, verbose_name="Depth, m", null=True, blank=True)
    
    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name_plural = "Site: Sensors"

class MoistureContent(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(verbose_name='Date & Time Measured', null=True)
    mc_data = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Analog Reading", null=True)

    def __str__(self):
        return '{}'.format(self.sensor)

    class Meta:
        verbose_name_plural = "Site: Moisture Content"
        get_latest_by = "timestamp"

#DATABASE
class Soil(models.Model):
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
    name = models.CharField(max_length=25, verbose_name="Calibration Name", null=True, blank=True)
    fieldunit = models.ForeignKey (FieldUnit, on_delete=models.CASCADE, null=True, blank=True)
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
        (EXPONENTIAL, 'Exponential'),
        (LOGARITHMIC, 'Logarithmic'),
        (SYMMETRICAL_SIGMOIDAL, 'Symmetrical Sigmoidal'),
        (ASYMMETRICAL_SIGMOIDAL, 'Asymmetrical Sigmoidal'),
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
        return self.name
        
    class Meta:
        verbose_name_plural = "Site: Calibration Equation Constants"

#DATABASE
class IntakeFamily(models.Model):
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
    
    rooting = [
        ("Borg-Grimes Model", 'Borg-Grimes Model'),
        ("User-Defined", 'User-Defined'),
        ("Inverse Kc", 'Inverse Kc'),
    ]

    root_growth_model = models.CharField(choices=rooting, max_length=30, verbose_name="Root Growth Model", null=True, blank=True)
    kc_ini = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Kc (ini)", null=True, blank=True)
    kc_mid = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Kc (mid)", null=True, blank=True)
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
    def __str__(self):
        return self.crop

    class Meta:
        verbose_name_plural = "Database: Crop"
        ordering = ('crop',)

#SITE VALUES
class IrrigationParameters(models.Model):
    name= models.CharField(max_length=30, verbose_name="Irrigation System Name", null=True, blank=True)
    irrig_choices = [
        ('basin', 'basin'),
        ('border', 'border'),
        ('furrow', 'furrow'),
        ('sprinkler', 'sprinkler'),
        ('drip', 'drip')
    ]

    irrigation_system_type = models.CharField(choices=irrig_choices, max_length=30, verbose_name="Irrigation System Type", null=True, blank=True)
    #BASIN
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
    ea = models.DecimalField(choices=EFF_CHOICES, max_digits=5, decimal_places=2, verbose_name="Application Efficiency (%)", help_text="Application efficiency is the fraction of the irrigation water that is used by the crop. Provided there are no runoff losses, the application efficiency (%) is the required irrigation depth (mm), divided by the average applied irrigation depth (mm), multiplied by 100%.", blank=True, null=True)
    #BORDER
    width = models.DecimalField(max_digits=20, decimal_places=4, verbose_name="Border Width (m)", null=True, blank=True)
    border_strips = models.DecimalField(max_digits=20, decimal_places=4, verbose_name="Number of Borders", null=True, blank=True)
    mannings_coeff = models.DecimalField(max_digits=20, decimal_places=4, verbose_name="Manning's coefficient", null=True, blank=True)
    area_slope = models.DecimalField(max_digits=20, decimal_places=4, verbose_name="Slope", null=True, blank=True)
    flow_rate_per_strip = models.DecimalField(max_digits=20, decimal_places=4, verbose_name="Flow rate per border strip (lps)", null=True, blank=True)
    total_flow_rate = models.DecimalField(max_digits=20, decimal_places=4, verbose_name="Total flow rate (lps)", null=True, blank=True)
    #FURROW
    bln_furrow_type = models.BooleanField (verbose_name="It is an open-ended furrow.")
    #p_adjusted = models.DecimalField(max_digits=20, decimal_places=4, verbose_name="P adjusted (m)", null=True) #doublecheck details
    #just insert in js computation

    #DRIP
    bln_single_lateral = models.BooleanField (verbose_name="Single Straight Lateral")
    #if bln_single_lateral is true
    emitters_per_plant = models.DecimalField(max_digits=5, decimal_places=0, verbose_name="No. of Emitters per Plant", null=True, blank=True)
    emitter_spacing = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Emitter Spacing (m)", null=True, blank=True)
    #if bln_single_lateral is false
    plant_spacing = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Plant spacing (m)", null=True, blank=True)
    row_spacing = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Row spacing (m)", null=True, blank=True)
    wetted_dia = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Wetted diameter (m)", null=True, blank=True)
    #
    EU = models.DecimalField(max_digits=3, decimal_places=3, verbose_name="Design Emission Uniformity", null=True, blank=True)
    irrigation_interval = models.DecimalField(max_digits=5, decimal_places=0, verbose_name="Irrigation Interval (days)", null=True, blank=True)

    #SPRINKLER
    farm_area = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Farm area (sq.m)", null=True, blank=True)
    area_irrigated_at_a_time = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Area irrigated at a time (sq.m)", null=True, blank=True)
    lateral_spacing = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Lateral spacing (m)", null=True, blank=True)
    sprinkler_spacing = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Sprinkler spacing (m)", null=True, blank=True)
    num_of_sprinklers = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Number of sprinklers", null=True, blank=True)
    class Meta:
        verbose_name_plural = "Irrigation System"

    def __str__(self):
        return self.name

class Farm(models.Model):
    name = models.CharField(max_length=20)
    province = models.CharField(max_length=50, null="True", blank="True")
    municipality = models.CharField(max_length=50, null="True", blank="True")
    brgy = models.CharField(max_length=50, verbose_name="Barangay", null="True", blank="True")

    class Meta:
        verbose_name_plural = "Site: Farms"
        ordering = ('name',)

    def __str__(self):
        return self.name

class WAISSystems(models.Model):
    name = models.CharField(max_length=20)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, verbose_name="Farm", null=True, blank=True)
    farm_manager = models.ForeignKey(Personnel, on_delete=models.CASCADE, verbose_name="Farm Manager", null=True, blank=True)
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, null=True, blank=True)
    soil = models.ForeignKey(Soil, on_delete=models.CASCADE, null=True, blank=True)
    calib = models.ForeignKey(CalibrationConstant, on_delete=models.CASCADE, verbose_name="Calibration Equation", null=True, blank=True)
    irrigation = models.ForeignKey(IrrigationParameters, on_delete=models.CASCADE, verbose_name="Irrigation System", null=True, blank=True)
    fieldunit = models.ForeignKey(FieldUnit, on_delete=models.CASCADE, verbose_name="Field Unit", null=True, blank=True)    

    class Meta:
        verbose_name_plural = "WAISSystems"
        ordering = ('name',)

    def __str__(self):
        return self.name

class IrrigationAdvisory(models.Model):
    fieldunit = models.ForeignKey(FieldUnit, on_delete=models.CASCADE, null=True, blank=True)            
    net_app_depth = models.DecimalField(max_digits=20, decimal_places=4, verbose_name="Net Application Depth (mm)", null=True)
    irrigation_period = models.DecimalField(max_digits=20, decimal_places=4, verbose_name="Irrigation Period (mins)", null=True)
    irrigation_volume = models.DecimalField(max_digits=20, decimal_places=4, verbose_name="Irrigation Volume (l)", null=True)

    class Meta:
        verbose_name_plural = "Computation"

#MESSAGES
class ReceivedMsgs(models.Model):
    number = models.ForeignKey(Personnel, on_delete=models.CASCADE, null=True, blank=True)
    msg = models.TextField(max_length=200, verbose_name="Message", null=True, blank=True)
    timestamp = models.DateTimeField(verbose_name='Date/Time Sent', auto_now_add=True, null=True, blank=True)
    marker = models.BooleanField(default=True)
    class Meta:
        verbose_name_plural = "Messages: Received"
        get_latest_by = "timestamp"
    
    def __str__(self):
        return '{}'.format(self.number)

class SentMsgs(models.Model):
    number = models.ForeignKey(Personnel, on_delete=models.CASCADE, null=True, blank=True)
    msg = models.TextField(max_length=200, verbose_name="Message", null=True, blank=True)
    sent = models.BooleanField(verbose_name="Sent?", default=False)
    timestamp = models.DateTimeField(verbose_name='Date/Time Sent', auto_now_add=True, null=True, blank=True)
    marker = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Messages: Sent"
        get_latest_by = "timestamp"
    
    def __str__(self):
        return '{}'.format(self.number)