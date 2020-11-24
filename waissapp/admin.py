from django.contrib import admin
from .models import SentMsgs, ReceivedMsgs, Receiver, Sender, Personnel, Farm, SensorNumber, MoistureContent, FieldUnit, Soil, IntakeFamily, Crop, IrrigationAdvisory, CalibrationConstant, BasinPara, BorderPara, FurrowPara, DripPara, SprinklerPara


class SentMsgsInline(admin.TabularInline):
    model = SentMsgs

class SenderInline(admin.TabularInline):
    model = Sender

class ReceiverInline(admin.TabularInline):
    model = Receiver

class ReceivedMsgsInline(admin.TabularInline):
    model = FieldUnit

class FieldUnitInline(admin.TabularInline):
    model = ReceivedMsgs
    extra=1

class MoistureContentInline(admin.TabularInline):
    model = MoistureContent
    extra=3

class MoistureContentAdmin(admin.ModelAdmin):
    list_display = ('sensor_name', 'fieldunit', 'raw_data')
    ordering = ['timestamp']

class SensorNumberInline(admin.TabularInline):
    model = SensorNumber
    extra=0

class SensorNumberAdmin(admin.ModelAdmin):
    list_display = ('sensor_name', 'depth', 'fieldunit')
    inlines = [MoistureContentInline]

class FarmInline(admin.TabularInline):
    model = Farm

class FarmAdmin(admin.ModelAdmin):
    ordering = ["farm_name"]
    list_display=('farm_name', 'brgy', 'municipality', 'province')

class FieldUnitAdmin(admin.ModelAdmin):
    inlines = [SensorNumberInline]

admin.site.register(SentMsgs)
admin.site.register(Sender)
admin.site.register(ReceivedMsgs)
admin.site.register(Receiver)

admin.site.register(Farm, FarmAdmin)
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


admin.site.register(Soil, SoilAdmin)
admin.site.register(IntakeFamily, IntakeFamilyAdmin)
admin.site.register(Crop, CropAdmin)

class CalibrationConstantInline(admin.TabularInline):
    model = CalibrationConstant
    
class CalibrationConstantAdmin(admin.ModelAdmin):
    list_display =('calib_name', 'calib_equation', 'calib_coeff_a', 'calib_coeff_b', 'calib_coeff_c', 'calib_coeff_d', 'calib_coeff_m')

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
    list_display =('basin_name', 'discharge', 'basin_length', 'ea')

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

class IrrigationAdvisoryInline(admin.TabularInline):
    model = IrrigationAdvisory
class IrrigationAdvisoryAdmin(admin.ModelAdmin):
    list_display =('fieldunit', 'net_app_depth', 'irrigation_period', 'irrigation_volume')

admin.site.register(IrrigationAdvisory, IrrigationAdvisoryAdmin)