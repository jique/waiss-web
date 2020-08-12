from django.forms import ModelForm
from django import forms
from .models import Personnel, Soil, Crop, FieldUnitSettings, CalibrationConstant, FarmSummaries, IntakeFamily, Farm, FieldUnit, SensorNumber, BasinComp, BorderComp, FurrowComp, SprinklerComp, DripComp, BasinPara, BorderPara, FurrowPara, SprinklerPara, DripPara

class SoilForm(ModelForm):
    class Meta:
        model = Soil
        exclude = ()  # this says to include all fields from model to the form

class IntakeFamilyForm(ModelForm):
    class Meta:
        model = IntakeFamily
        exclude = ()  # this says to include all fields from model to the form

class CropForm(ModelForm):
    class Meta:
        model = Crop
        exclude = ()  # this says to include all fields from model to the form

class FieldUnitForm(ModelForm):
    class Meta:
        model = FieldUnit
        exclude = ()  # this says to include all fields from model to the form 

class FieldUnitSettingsForm(ModelForm):
    class Meta:
        model = FieldUnitSettings
        exclude = ()  # this says to include all fields from model to the form       

class SensorForm(ModelForm):
    class Meta:
        model = SensorNumber
        exclude = ()  # this says to include all fields from model to the form  

class CalibForm(ModelForm):
    class Meta:
        model = CalibrationConstant
        exclude = ()  # this says to include all fields from model to the form 

class FarmForm(ModelForm):
    class Meta:
        model = Farm
        exclude = ()  # this says to include all fields from model to the form 

class FarmSummariesForm(ModelForm):
    class Meta:
        model = FarmSummaries
        exclude = ()  # this says to include all fields from model to the form

class BasinForm(ModelForm):
    class Meta:
        model = BasinComp
        exclude = ()  # this says to include all fields from model to the form

class FurrowForm(ModelForm):
    class Meta:
        model = FurrowComp
        exclude = ()  # this says to include all fields from model to the form

class BorderForm(ModelForm):
    class Meta:
        model = BorderComp
        exclude = ()  # this says to include all fields from model to the form

class SprinklerForm(ModelForm):
    class Meta:
        model = SprinklerComp
        exclude = ()  # this says to include all fields from model to the form

class DripForm(ModelForm):
    class Meta:
        model = DripComp
        exclude = ()

class BasinParaForm(ModelForm):
    class Meta:
        model = BasinPara
        exclude = ()  # this says to include all fields from model to the form

class FurrowParaForm(ModelForm):
    class Meta:
        model = FurrowPara
        exclude = ()  # this says to include all fields from model to the form

class BorderParaForm(ModelForm):
    class Meta:
        model = BorderPara
        exclude = ()  # this says to include all fields from model to the form

class SprinklerParaForm(ModelForm):
    class Meta:
        model = SprinklerPara
        exclude = ()  # this says to include all fields from model to the form

class DripParaForm(ModelForm):
    class Meta:
        model = DripPara
        exclude = ()

class irrigtypeForm(forms.Form):
    farm_irrigation = forms.ChoiceField(choices=[("BASIN", "Basin"), ("BORDER", "Border"),("FURROW", "Furrow"), ("SPRINKLER", "Sprinkler"), ("DRIP", "Drip")], label="Irrigation System Type")

class PersonnelForm(ModelForm):
    class Meta:
        model = Personnel
        exclude = ()