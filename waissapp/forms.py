from django.forms import ModelForm
from django import forms
from .models import SentMsgs, Personnel, Soil, Crop, CalibrationConstant, Farm, FieldUnit, Sensor, MoistureContent, WAISSystems, Rainfall, Gravimetric, PercentShaded, Basin, Furrow, Border, Drip, Sprinkler
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )

class UserForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email'
        )

class SoilForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(SoilForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = 'small'
    class Meta:
        model = Soil
        exclude = ('author', 'personal',)  # this says to include all fields from model to the form

class CropForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CropForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = 'small'
    class Meta:
        model = Crop
        exclude = ('author', 'personal',)  # this says to include all fields from model to the form

class FieldUnitForm(forms.ModelForm):
    timestart = forms.TimeField(widget=forms.TextInput(attrs={'type': 'time'}), label="Start Time", required=True)
    timestop = forms.TimeField(widget=forms.TextInput(attrs={'type': 'time'}), label="Stop Time", required=True)

    def __init__(self, *args, **kwargs):
        super(FieldUnitForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = 'small'
    class Meta:
        model = FieldUnit
        exclude = ('author', 'personal',)  # this says to include all fields from model to the form 

class CalibForm(ModelForm):
    date_tested = forms.DateField(
    widget=forms.TextInput(     
        attrs={'type': 'date'},
        ),
    required=False
    )
    def __init__(self, *args, **kwargs):
        super(CalibForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = 'small' 
    class Meta:
        model = CalibrationConstant
        exclude = ('author', 'personal',)  # this says to include all fields from model to the form 

class SensorForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(SensorForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = 'small'
    class Meta:
        model = Sensor
        exclude = ('author', 'personal',)  # this says to include all fields from model to the form 

class MCForm(forms.ModelForm):
    timestamp = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )
    def __init__(self, *args, **kwargs):
        super(MCForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = 'small'
    class Meta:
        model = MoistureContent
        exclude = ('author', 'personal',)  # this says to include all fields from model to the form 

class FarmForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(FarmForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = 'small'
    class Meta:
        model = Farm
        exclude = ('author', 'personal',)  # this says to include all fields from model to the form 

class BasinForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(BasinForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = 'small'
    class Meta:
        model = Basin
        exclude = ('author', 'personal',)  # this says to include all fields from model to the form

class BorderForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(BorderForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = 'small' 
    class Meta:
        model = Border
        exclude = ('author', 'personal',)  # this says to include all fields from model to the form

class FurrowForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(FurrowForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = 'small'
    class Meta:
        model = Furrow
        exclude = ('author', 'personal',)  # this says to include all fields from model to the form

class DripForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(DripForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = 'small'
    class Meta:
        model = Drip
        exclude = ('author', 'personal',)  # this says to include all fields from model to the form

class SprinklerForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(SprinklerForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = 'small'
    class Meta:
        model = Sprinkler
        exclude = ('author', 'personal',)  # this says to include all fields from model to the form

class WAISSystemsForm(ModelForm):
    date_transplanted = forms.DateField(
    widget=forms.TextInput(     
        attrs={'type': 'date'},
        ),
    required=True
    )
    def __init__(self, *args, **kwargs):
        super(WAISSystemsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = 'small'
    class Meta:
        model = WAISSystems
        exclude = ('author', 'id', 'personal', )  # this says to include all fields from model to the form 
        
class PersonnelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(PersonnelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = 'small'
    class Meta:
        model = Personnel
        exclude = ('author', 'personal',)

class SentMsgsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(SentMsgsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = 'small'
        self.fields['msg'].widget = forms.Textarea(attrs={'rows': 2})
    class Meta:
        model = SentMsgs
        exclude = ('author', 'personal',)  # this says to include all fields from model to the form

class RainfallForm(forms.ModelForm):
    timestamp = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )
    def __init__(self, *args, **kwargs):
        super(RainfallForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = 'small'
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
        self.helper.label_class = 'small'
    class Meta:
        model = PercentShaded
        exclude = ('author', 'personal',)  # this says to include all fields from model to the form

class GravimetricForm(forms.ModelForm):
    timestamp = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )
    def __init__(self, *args, **kwargs):
        super( GravimetricForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = 'small'
    class Meta:
        model =  Gravimetric
        exclude = ('author', 'personal',)  # this says to include all fields from model to the form