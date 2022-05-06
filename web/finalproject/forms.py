from django import forms
from django.forms.widgets import NumberInput
import datetime

t = datetime.date.today

class PlantForm(forms.Form):
    plant_name = forms.CharField(max_length=255)
    plant_nickname = forms.CharField(max_length=50)
    plant_date = forms.DateField(initial=t, widget=NumberInput(attrs={"type": "date", "class": "today_date", "max": t}))
    water_date = forms.DateField(initial=t, widget=NumberInput(attrs={"type": "date", "class": "today_date", "max": t}))