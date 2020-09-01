from django.contrib import admin
from .models import Personnel, Farm, SensorNumber, FarmSummaries, MoistureContent, FieldUnit, Soil, IntakeFamily, Crop, FieldUnitSettings, BasinAppEff, BasinComp, BorderComp, FurrowComp, DripComp, SprinklerComp, CalibrationConstant, BasinPara, BorderPara, FurrowPara, DripPara, SprinklerPara

class FieldUnitInline(admin.TabularInline):
    model = FieldUnit
    extra=0

class MoistureContentInline(admin.TabularInline):
    model = MoistureContent
    extra=3

class MoistureContentAdmin(admin.ModelAdmin):
    list_display = ('sensor', 'fieldunit', 'raw_data')
    ordering = ['timestamp']

class SensorNumberInline(admin.TabularInline):
    model = SensorNumber
    extra=0

class SensorNumberAdmin(admin.ModelAdmin):
    list_display = ('name', 'depth', 'fieldunit')
    inlines = [MoistureContentInline]

class FarmInline(admin.TabularInline):
    model = Farm

class FarmAdmin(admin.ModelAdmin):
    ordering = ["farm_name"]
    list_display=('farm_name', 'farm_location')

class FieldUnitAdmin(admin.ModelAdmin):
    list_display=('name', 'farm_name')
    inlines = [SensorNumberInline]
    
class FarmSummariesInline(admin.TabularInline):
    model = FarmSummaries

class FarmSummariesAdmin(admin.ModelAdmin):
    list_display = ('name', 'farm_name', 'farm_manager', 'fieldunit', 'crop', 'soil', 'intakefamily', 'calib_eqn', 'basin_sys', 'border_sys', 'furrow_sys', 'sprinkler_sys', 'drip_sys')
    ordering = ["name"]

admin.site.register(Farm, FarmAdmin)
admin.site.register(FarmSummaries, FarmSummariesAdmin)
admin.site.register(SensorNumber, SensorNumberAdmin)
admin.site.register(Personnel)
admin.site.register(MoistureContent, MoistureContentAdmin)
admin.site.register(FieldUnit, FieldUnitAdmin)

class SoilInline(admin.TabularInline):
    model = Soil
    list_display =('soiltype', 'fc', 'pwp', 'As', )

class SoilAdmin(admin.ModelAdmin):
    list_display = ('soiltype', 'fc', 'pwp', 'As', 'source')
    ordering = ["soiltype"]

class IntakeFamilyInline(admin.TabularInline):
    model = IntakeFamily
    list_display =('intakefamily','coeff_a', 'coeff_b', 'coeff_c', 'coeff_f', 'coeff_g')

class IntakeFamilyAdmin(admin.ModelAdmin):
    list_display = ('intakefamily', 'coeff_a', 'coeff_b', 'coeff_c', 'coeff_f', 'coeff_g')
    ordering = ["intakefamily"]

class CropInline(admin.TabularInline):
    model = Crop
    list_display =('crop', 'mad', 'growingperiod', 'drz', 'kc_ini', 'kc_mid', 'kc_end', 'kc_cc_1', 'kc_cc_2', 'kc_cc_3', 'fieldunit', 'farm_name')

class CropAdmin(admin.ModelAdmin):
    list_display =('crop', 'mad', 'growingperiod', 'drz', 'kc_ini', 'kc_mid', 'kc_end', 'kc_cc_1', 'kc_cc_2', 'kc_cc_3')
    ordering = ['crop',]

class FieldUnitSettingsInline(admin.TabularInline):
    model = FieldUnitSettings
    list_display =( 'usk', 'fieldunitstatus', 'withirrigation', 'automaticthreshold', 'servernumber', 'fieldunitnumber', 'numberofsamples', 'sensorintegrationtime', 'timestart', 'timestop', 'delay', 'clockcorrection')

class FieldUnitSettingsAdmin(admin.ModelAdmin):
    list_display =('usk', 'fieldunitstatus', 'withirrigation', 'automaticthreshold', 'servernumber', 'fieldunitnumber', 'numberofsamples', 'sensorintegrationtime', 'timestart', 'timestop', 'delay', 'clockcorrection')

admin.site.register(Soil, SoilAdmin)
admin.site.register(IntakeFamily, IntakeFamilyAdmin)
admin.site.register(Crop, CropAdmin)
admin.site.register(FieldUnitSettings, FieldUnitSettingsAdmin)

class BasinAppEffInline(admin.TabularInline):
    model = BasinAppEff

class BasinAppEffAdmin(admin.ModelAdmin):
    list_display = ('appeff', 'eff_adv_ratio')

class BasinCompInline(admin.TabularInline):
    model = BasinComp

class BorderCompInline(admin.TabularInline):
    model = BorderComp

class FurrowCompInline(admin.TabularInline):
    model = FurrowComp

class SprinklerCompInline(admin.TabularInline):
    model = SprinklerComp

class DripCompInline(admin.TabularInline):
    model = DripComp

class BasinCompAdmin(admin.ModelAdmin):
    list_display = ('system', 'net_app_depth', 'net_opp_time', 'inflow_time', 'advance_time', 'irrigation_period')

class BorderCompAdmin(admin.ModelAdmin):
    list_display = ('system', 'net_app_depth', 'net_opp_time', 'lag_time', 'inflow_time', 'irrigation_period')

class FurrowCompAdmin(admin.ModelAdmin):
    list_display = ('system', 'net_app_depth', 'net_opp_time', 'advance_time', 'irrigation_period')

class SprinklerCompAdmin(admin.ModelAdmin):
    list_display = ('system', 'net_app_depth', 'gross_app_depth', 'application_rate', 'irrigation_rate', 'irrigation_period' )

class DripCompAdmin(admin.ModelAdmin):
    list_display = ('system', 'percent_wetted_area', 'net_app_depth', 'transpiration_requirement', 'gross_app_depth', 'percent_shaded', 'peak_ETo','ave_peak_daily_transpiration', 'gross_volume_required_per_plant', 'irrigation_period')

class CalibrationConstantInline(admin.TabularInline):
    model = CalibrationConstant
    
class CalibrationConstantAdmin(admin.ModelAdmin):
    list_display =('calib_name', 'sensor','calib_equation', 'calib_coeff_a', 'calib_coeff_b', 'calib_coeff_c', 'calib_coeff_d', 'calib_coeff_m')

admin.site.register(BasinComp, BasinCompAdmin)
admin.site.register(BorderComp, BorderCompAdmin)
admin.site.register(FurrowComp, FurrowCompAdmin)
admin.site.register(SprinklerComp, SprinklerCompAdmin)
admin.site.register(DripComp, DripCompAdmin)
admin.site.register(BasinAppEff, BasinAppEffAdmin)
admin.site.register(CalibrationConstant, CalibrationConstantAdmin)

class BasinParaInline(admin.TabularInline):
    model = BasinPara

class BorderParaInline(admin.TabularInline):
    model = BorderPara

class FurrowParaInline(admin.TabularInline):
    model = FurrowPara

class SprinklerParaInline(admin.TabularInline):
    model = SprinklerPara

class DripParaInline(admin.TabularInline):
    model = DripPara

class BasinParaAdmin(admin.ModelAdmin):
    list_display =('basin_name', 'discharge', 'basin_length', 'ea', 'eff_adv_ratio')

class BorderParaAdmin(admin.ModelAdmin):
    list_display =('border_name','discharge')

class FurrowParaAdmin(admin.ModelAdmin):
    list_display =('name', 'bln_furrow_type')

class SprinklerParaAdmin(admin.ModelAdmin):
    list_display =('name', 'farm_area')

class DripParaAdmin(admin.ModelAdmin):
    list_display =('name', 'bln_single_lateral', 'emitters_per_plant', 'emitter_spacing', 'plant_spacing', 'row_spacing', 'wetted_dia', 'EU', 'irrigation_interval')

admin.site.register(BasinPara, BasinParaAdmin)
admin.site.register(BorderPara, BorderParaAdmin)
admin.site.register(FurrowPara, FurrowParaAdmin)
admin.site.register(SprinklerPara, SprinklerParaAdmin)
admin.site.register(DripPara, DripParaAdmin)