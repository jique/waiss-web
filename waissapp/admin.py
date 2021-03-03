from django.contrib import admin
from .models import SentMsgs, ReceivedMsgs, Personnel, Farm, Sensor, MoistureContent, FieldUnit, Soil, Crop, IrrigationAdvisory, CalibrationConstant, IrrigationParameters, WAISSystems, PercentShaded


class SentMsgsInline(admin.TabularInline):
    model = SentMsgs

class SentMsgsAdmin(admin.ModelAdmin):
    list_display = ('number', 'msg', 'timestamp')
    ordering = ['timestamp']

class ReceivedMsgsInline(admin.TabularInline):
    model = ReceivedMsgs

class ReceivedMsgsAdmin(admin.ModelAdmin):
    list_display = ('number', 'msg', 'timestamp')
    ordering = ['timestamp']
    
class FieldUnitInline(admin.TabularInline):
    model = FieldUnit
    extra=1

class MoistureContentInline(admin.TabularInline):
    model = MoistureContent
    extra=3

class MoistureContentAdmin(admin.ModelAdmin):
    list_display = ('sensor', 'mc_data', 'timestamp')
    ordering = ['timestamp']

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
    list_display=('name', 'brgy', 'municipality', 'province')

class FieldUnitAdmin(admin.ModelAdmin):
    inlines = [SensorInline]

admin.site.register(SentMsgs, SentMsgsAdmin)
admin.site.register(ReceivedMsgs, ReceivedMsgsAdmin)
admin.site.register(Farm, FarmAdmin)
admin.site.register(Sensor, SensorAdmin)
admin.site.register(Personnel)
admin.site.register(MoistureContent, MoistureContentAdmin)
admin.site.register(FieldUnit, FieldUnitAdmin)

class SoilInline(admin.TabularInline):
    model = Soil
    list_display =('soiltype', 'fc', 'pwp')

class SoilAdmin(admin.ModelAdmin):
    list_display = ('soiltype', 'fc', 'pwp', 'source')
    ordering = ["soiltype"]

class CropInline(admin.TabularInline):
    model = Crop
    list_display =('crop', 'mad', 'growingperiod', 'drz', 'kc_ini', 'kc_mid', 'kc_end', 'kc_cc_1', 'kc_cc_2', 'kc_cc_3', 'fieldunit', 'farm_name')

class CropAdmin(admin.ModelAdmin):
    list_display =('crop', 'mad', 'growingperiod', 'drz', 'kc_ini', 'kc_mid', 'kc_end', 'kc_cc_1', 'kc_cc_2', 'kc_cc_3')
    ordering = ['crop',]


admin.site.register(Soil, SoilAdmin)
admin.site.register(Crop, CropAdmin)

class CalibrationConstantInline(admin.TabularInline):
    model = CalibrationConstant
    
class CalibrationConstantAdmin(admin.ModelAdmin):
    list_display =('name', 'calib_equation', 'coeff_a', 'coeff_b', 'coeff_c', 'coeff_d', 'coeff_m')

admin.site.register(CalibrationConstant, CalibrationConstantAdmin)

class IrrigationParametersInline(admin.TabularInline):
    model = IrrigationParameters

class IrrigationParametersAdmin(admin.ModelAdmin):
    list_display =('name', 'discharge', 'basin_length', 'ea', 'bln_furrow_type', 'bln_single_lateral', 'emitters_per_plant', 'emitter_spacing', 'plant_spacing', 'row_spacing', 'wetted_dia', 'EU', 'irrigation_interval')

admin.site.register(IrrigationParameters, IrrigationParametersAdmin)

class IrrigationAdvisoryInline(admin.TabularInline):
    model = IrrigationAdvisory
class IrrigationAdvisoryAdmin(admin.ModelAdmin):
    list_display =('fieldunit', 'net_app_depth', 'irrigation_period', 'irrigation_volume')

class WAISSystemsInline(admin.TabularInline):
    model = WAISSystems
class WAISSystemsAdmin(admin.ModelAdmin):
    list_display =('name', 'farm', 'farm_manager', 'crop', 'soil', 'irrigation', 'fieldunit')

class PercentShadedInline(admin.TabularInline):
    model = PercentShaded

class PercentShadedAdmin(admin.ModelAdmin):
    list_display =('crop', 'area_shaded', 'date')

admin.site.register(IrrigationAdvisory, IrrigationAdvisoryAdmin)
admin.site.register(WAISSystems, WAISSystemsAdmin)
admin.site.register(PercentShaded, PercentShadedAdmin)