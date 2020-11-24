from django.forms import ModelForm
from django import forms
from .models import SentMsgs, Personnel, Soil, Crop, CalibrationConstant, IntakeFamily, Farm, FieldUnit, SensorNumber, BasinPara, BorderPara, FurrowPara, SprinklerPara, DripPara
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from durationwidget.widgets import TimeDurationWidget
  
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
        
class SensorForm(forms.ModelForm):
    class Meta:
        model = SensorNumber
        exclude = ()  # this says to include all fields from model to the form 

    def __init__(self, *args, **kwargs):
        super(SensorForm, self).__init__(*args, **kwargs)
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

class BasinParaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(BasinParaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8' 
    class Meta:
        model = BasinPara
        exclude = ()  # this says to include all fields from model to the form

class FurrowParaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(FurrowParaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8' 
    class Meta:
        model = FurrowPara
        exclude = ()  # this says to include all fields from model to the form

class BorderParaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(BorderParaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8' 
    class Meta:
        model = BorderPara
        exclude = ()  # this says to include all fields from model to the form

class SprinklerParaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(SprinklerParaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8' 
    class Meta:
        model = SprinklerPara
        exclude = ()  # this says to include all fields from model to the form

class DripParaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(DripParaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8' 
    class Meta:
        model = DripPara
        exclude = ()
        
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