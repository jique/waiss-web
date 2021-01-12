from django.forms import ModelForm
from django import forms
from .models import SentMsgs, Personnel, Soil, Crop, CalibrationConstant, IntakeFamily, Farm, FieldUnit, IrrigationParameters, Sensor, MoistureContent
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

  
class SoilForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(SoilForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-5'
        self.helper.field_class = 'col-lg-7' 
    class Meta:
        model = Soil
        exclude = ()  # this says to include all fields from model to the form

class IntakeFamilyForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(IntakeFamilyForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8' 
    class Meta:
        model = IntakeFamily
        exclude = ()  # this says to include all fields from model to the form

class CropForm(forms.ModelForm):
    date_transplanted = forms.DateField(
    widget=forms.TextInput(     
        attrs={'type': 'date'} 
        )
    )  
    def __init__(self, *args, **kwargs):
        super(CropForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8'
    class Meta:
        model = Crop
        exclude = ()  # this says to include all fields from model to the form

class FieldUnitForm(forms.ModelForm):
    class Meta:
        model = FieldUnit
        exclude = ()  # this says to include all fields from model to the form 
    
    timestart = forms.TimeField(widget=forms.TextInput(attrs={'type': 'time'}), label="Start Time")
    timestop = forms.TimeField(widget=forms.TextInput(attrs={'type': 'time'}), label="Stop Time")

    def __init__(self, *args, **kwargs):
        super(FieldUnitForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8'

class CalibForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CalibForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8' 
    class Meta:
        model = CalibrationConstant
        exclude = ()  # this says to include all fields from model to the form 

class SensorForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(SensorForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8' 
    class Meta:
        model = Sensor
        exclude = ()  # this says to include all fields from model to the form 

class MCForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(MCForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8' 
    class Meta:
        model = MoistureContent
        exclude = ()  # this says to include all fields from model to the form 

class FarmForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(FarmForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8'
    class Meta:
        model = Farm
        exclude = ()  # this says to include all fields from model to the form 

class IrrigationParametersForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(IrrigationParametersForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8' 
    class Meta:
        model =IrrigationParameters
        exclude = ()  # this says to include all fields from model to the form
        
class PersonnelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(PersonnelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8' 
    class Meta:
        model = Personnel
        exclude = ()

class SentMsgsForm(ModelForm):
    class Meta:
        model = SentMsgs
        exclude = ()  # this says to include all fields from model to the form