from django.forms import ModelForm
from django import forms
from .models import SentMsgs, Personnel, Soil, Crop, FieldUnitSettings, CalibrationConstant, FarmSummaries, IntakeFamily, Farm, FieldUnit, SensorNumber, BasinComp, BorderComp, FurrowComp, SprinklerComp, DripComp, BasinPara, BorderPara, FurrowPara, SprinklerPara, DripPara
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from bootstrap_datepicker.widgets import DatePicker


        
class SoilForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(SoilForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9' 
    class Meta:
        model = Soil
        exclude = ()  # this says to include all fields from model to the form

class IntakeFamilyForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(IntakeFamilyForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9' 
    class Meta:
        model = IntakeFamily
        exclude = ()  # this says to include all fields from model to the form

class CropForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CropForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-7'
        self.helper.field_class = 'col-lg-5'
    class Meta:
        model = Crop
        exclude = ()  # this says to include all fields from model to the form

class FieldUnitForm(forms.ModelForm):
    
    class Meta:
        model = FieldUnit
        exclude = ()  # this says to include all fields from model to the form 
    
        fields = [
            'name',
        ]

        widgets = {
            'name': forms.TextInput(attrs={'class': "form-control formset-field"})
        }

class FieldUnitSettingsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(FieldUnitSettingsForm, self).__init__(*args, **kwargs)
        self.fields['timestart'].widget.attrs['class'] = 'datepicker'
    class Meta:
        model = FieldUnitSettings
        exclude = ()  # this says to include all fields from model to the form       

class SensorForm(forms.ModelForm):
    class Meta:
        model = SensorNumber
        exclude = ()  # this says to include all fields from model to the form  

        fields = [
            'sensor_name',
            'depth'
        ]

        widgets = {
            'sensor_name': forms.TextInput(attrs={'class': "form-control formset-field",'placeholder': "sensor_name"}),
            'depth': forms.NumberInput(attrs={'class': "form-control formset-field",'placeholder': "sensor_depth"})
        }
class CalibForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CalibForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9' 
    class Meta:
        model = CalibrationConstant
        exclude = ()  # this says to include all fields from model to the form 

class FarmForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(FarmForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9' 
    class Meta:
        model = Farm
        exclude = ()  # this says to include all fields from model to the form 

class FarmSummariesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FarmSummariesForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-5'
        self.helper.field_class = 'col-lg-7' 
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
        
class PersonnelForm(ModelForm):
    class Meta:
        model = Personnel
        exclude = ()

class SentMsgsForm(ModelForm):

    class Meta:
        model = SentMsgs
        exclude = ()  # this says to include all fields from model to the form