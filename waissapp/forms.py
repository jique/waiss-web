from django.forms import ModelForm
from django import forms
from .models import SentMsgs, Personnel, Soil, Crop, CalibrationConstant, Farm, FieldUnit, Sensor, MoistureContent, WAISSystems, Rainfall, Gravimetric, PercentShaded, Basin, Furrow, Border, Drip, Sprinkler
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
        exclude = ('author', 'personal',)  # this says to include all fields from model to the form

class CropForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CropForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8'
    class Meta:
        model = Crop
        exclude = ('author', 'personal',)  # this says to include all fields from model to the form

class FieldUnitForm(forms.ModelForm):
    timestart = forms.TimeField(widget=forms.TextInput(attrs={'type': 'time'}), label="Start Time")
    timestop = forms.TimeField(widget=forms.TextInput(attrs={'type': 'time'}), label="Stop Time")

    def __init__(self, *args, **kwargs):
        super(FieldUnitForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8'
    class Meta:
        model = FieldUnit
        exclude = ('author', 'personal',)  # this says to include all fields from model to the form 

class CalibForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CalibForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8' 
    class Meta:
        model = CalibrationConstant
        exclude = ('author', 'personal',)  # this says to include all fields from model to the form 

class SensorForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(SensorForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8' 
    class Meta:
        model = Sensor
        exclude = ('author', 'personal',)  # this says to include all fields from model to the form 

class MCForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MCForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8' 
    class Meta:
        model = MoistureContent
        exclude = ('author', 'personal',)  # this says to include all fields from model to the form 

class FarmForm(ModelForm):
    class Meta:
        model = Farm
        exclude = ('author', 'personal',)  # this says to include all fields from model to the form 

class BasinForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(BasinForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8' 
    class Meta:
        model = Basin
        exclude = ('author', 'personal',)  # this says to include all fields from model to the form

class BorderForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(BorderForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8' 
    class Meta:
        model = Border
        exclude = ('author', 'personal',)  # this says to include all fields from model to the form

class FurrowForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(FurrowForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8' 
    class Meta:
        model = Furrow
        exclude = ('author', 'personal',)  # this says to include all fields from model to the form

class DripForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(DripForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8' 
    class Meta:
        model = Drip
        exclude = ('author', 'personal',)  # this says to include all fields from model to the form

class SprinklerForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(SprinklerForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8' 
    class Meta:
        model = Sprinkler
        exclude = ('author', 'personal',)  # this says to include all fields from model to the form

class WAISSystemsForm(ModelForm):
    date_transplanted = forms.DateField(
    widget=forms.TextInput(     
        attrs={'type': 'date'}
        ),
    required=True
    )
    def __init__(self, *args, **kwargs):
        super(WAISSystemsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'
    class Meta:
        model = WAISSystems
        exclude = ('author', 'id', 'personal', )  # this says to include all fields from model to the form 
        
class PersonnelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(PersonnelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8' 
    class Meta:
        model = Personnel
        exclude = ('author', 'personal',)

class SentMsgsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(SentMsgsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9' 
        self.fields['msg'].widget = forms.Textarea(attrs={'rows': 2})
    class Meta:
        model = SentMsgs
        exclude = ('author', 'personal',)  # this says to include all fields from model to the form

class RainfallForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RainfallForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8' 
    class Meta:
        model = Rainfall
        exclude = ('author', 'personal',)  # this says to include all fields from model to the form

class PercentShadedForm(forms.ModelForm):
    date = forms.DateField(
    widget=forms.TextInput(     
        attrs={'type': 'date'}
        ),
    required=True
    )
    def __init__(self, *args, **kwargs):
        super(PercentShadedForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8' 
    class Meta:
        model = PercentShaded
        exclude = ('author', 'personal',)  # this says to include all fields from model to the form

class GravimetricForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super( GravimetricForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8' 
    class Meta:
        model =  Gravimetric
        exclude = ('author', 'personal',)  # this says to include all fields from model to the form