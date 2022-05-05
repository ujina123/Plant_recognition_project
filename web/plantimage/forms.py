from django import forms
from .models import ImageModel


class ImageUploadForm(forms.Form):
    title = forms.CharField(max_length=255)
    image = forms.ImageField()