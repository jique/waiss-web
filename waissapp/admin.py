from django.contrib import admin
from .models import SentMsgs, ReceivedMsgs, Personnel, Farm, Sensor, MoistureContent, FieldUnit, Soil, Crop, CalibrationConstant, WAISSystems, PercentShaded, Rainfall, Gravimetric, Basin, Border, Furrow, Drip, Sprinkler, ThingsboardDB

class PersonnelInline(admin.TabularInline):
    model = Personnel
    
class PersonnelAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'number', 'timestamp')

class SentMsgsInline(admin.TabularInline):
    model = SentMsgs

class SentMsgsAdmin(admin.ModelAdmin):
    list_display = ('number', 'msg', 'timestamp')
    ordering = ['timestamp']

class ReceivedMsgsInline(admin.TabularInline):
    model = ReceivedMsgs

class ReceivedMsgsAdmin(admin.ModelAdmin):
    list_display = ('number', 'msg', 'author', 'personal', 'timestamp')
    ordering = ['timestamp']
    
class FieldUnitInline(admin.TabularInline):
    model = FieldUnit

class MoistureContentInline(admin.TabularInline):
    model = MoistureContent
    extra=3

class MoistureContentAdmin(admin.ModelAdmin):
    list_display = ('sensor', 'mc_data', 'date', 'time')
    ordering = ['date']

class SensorInline(admin.TabularInline):
    model = Sensor
    extra=0

class SensorAdmin(admin.ModelAdmin):
    list_display = ('name', 'depth', 'fieldunit')
    inlines = [MoistureContentInline]

class FarmInline(admin.TabularInline):
    model = Farm

class FarmAdmin(admin.ModelAdmin):
    ordering = ["name"]
    list_display=('name', 'brgy', 'municipality', 'province', 'lat', 'long', 'author', 'personal', 'timestamp')

class FieldUnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'usk', 'number', 'fieldunitstatus', 'withirrigation', 'samples', 'sensorintegrationtime', 'timestart', 'timestop', 'delay', 'clockcorrection' , 'author', 'personal', 'timestamp')
    inlines = [SensorInline]

class SoilInline(admin.TabularInline):
    model = Soil

class SoilAdmin(admin.ModelAdmin):
    list_display = ('soiltype', 'fc', 'pwp', 'bln_surface_irrigation', 'intake_family', 'source', 'author', 'personal', 'timestamp')
    ordering = ["soiltype"]

class CropInline(admin.TabularInline):
    model = Crop
class CropAdmin(admin.ModelAdmin):
    list_display =('crop', 'mad', 'growingperiod', 'drz', 'root_growth_model', 'kc_ini', 'kc_mid', 'kc_end', 'kc_cc_1', 'kc_cc_2', 'kc_cc_3', 'source', 'author', 'personal', 'timestamp')
    ordering = ['crop',]

class CalibrationConstantInline(admin.TabularInline):
    model = CalibrationConstant
    
class CalibrationConstantAdmin(admin.ModelAdmin):
    list_display =('name', 'calib_equation', 'coeff_a', 'coeff_b', 'coeff_c', 'coeff_d', 'coeff_m', 'author', 'personal', 'timestamp')

class WAISSystemsInline(admin.TabularInline):
    model = WAISSystems
    
class WAISSystemsAdmin(admin.ModelAdmin):
    list_display =('name', 'farm', 'farm_manager', 'crop', 'date_transplanted', 'soil', 'fieldunit', 'calib', 'basin', 'border', 'furrow', 'drip', 'sprinkler', 'author', 'personal', 'timestamp')

class PercentShadedInline(admin.TabularInline):
    model = PercentShaded

class PercentShadedAdmin(admin.ModelAdmin):
    list_display =('fieldunit', 'area_shaded', 'date')

class RainfallInline(admin.TabularInline):
    model = Rainfall

class RainfallAdmin(admin.ModelAdmin):
    list_display =('fieldunit', 'amount', 'date', 'time')

class GravimetricInline(admin.TabularInline):
    model = Gravimetric

class GravimetricAdmin(admin.ModelAdmin):
    list_display =('date', 'time', 'fieldunit', 'mc_data')

admin.site.register(Soil, SoilAdmin)
admin.site.register(Crop, CropAdmin)
admin.site.register(WAISSystems, WAISSystemsAdmin)
admin.site.register(PercentShaded, PercentShadedAdmin)
admin.site.register(SentMsgs, SentMsgsAdmin)
admin.site.register(ReceivedMsgs, ReceivedMsgsAdmin)
admin.site.register(Farm, FarmAdmin)
admin.site.register(Sensor, SensorAdmin)
admin.site.register(Personnel, PersonnelAdmin)
admin.site.register(MoistureContent, MoistureContentAdmin)
admin.site.register(FieldUnit, FieldUnitAdmin)
admin.site.register(CalibrationConstant, CalibrationConstantAdmin)
admin.site.register(Rainfall, RainfallAdmin)
admin.site.register(Gravimetric, GravimetricAdmin)

class BasinInline(admin.TabularInline):
    model = Basin

class BasinAdmin(admin.ModelAdmin):
    list_display =('name', 'basin_length', 'discharge', 'ea', 'author', 'personal', 'timestamp')

class BorderInline(admin.TabularInline):
    model = Border

class BorderAdmin(admin.ModelAdmin):
    list_display =('name', 'discharge', 'border_length', 'ea', 'timestamp', 'author', 'personal', 'timestamp')

class FurrowInline(admin.TabularInline):
    model = Furrow

class FurrowAdmin(admin.ModelAdmin):
    list_display =('name', 'discharge', 'area_slope', 'mannings_coeff', 'bln_furrow_type', 'furrow_spacing', 'furrow_length', 'author', 'personal', 'timestamp')

class SprinklerInline(admin.TabularInline):
    model = Sprinkler

class SprinklerAdmin(admin.ModelAdmin):
    list_display =('name', 'discharge', 'ea', 'lateral_spacing', 'sprinkler_spacing', 'author', 'personal', 'timestamp')

class DripInline(admin.TabularInline):
    model = Drip

class DripAdmin(admin.ModelAdmin):
    list_display =('name', 'ave_discharge', 'bln_single_lateral', 'emitters_per_plant', 'emitter_spacing', 'plant_spacing', 'row_spacing', 'wetted_dia', 'bln_ii', 'irrigation_interval', 'EU', 'author', 'personal', 'timestamp')

admin.site.register(Basin, BasinAdmin)
admin.site.register(Border, BorderAdmin)
admin.site.register(Furrow, FurrowAdmin)
admin.site.register(Sprinkler, SprinklerAdmin)
admin.site.register(Drip, DripAdmin)

class ThingsboardDBInline(admin.TabularInline):
    model = ThingsboardDB

class ThingsboardDBAdmin(admin.ModelAdmin):
    list_display = ('sensor_name', 'unix_timestamp', 'analog_readin')

admin.site.register(ThingsboardDB, ThingsboardDBAdmin)