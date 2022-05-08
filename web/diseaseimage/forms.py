# JngMkk
from django import forms

class ImageUpload(forms.Form):
    image = forms.ImageField(widget=forms.FileInput(
        attrs={
            "id": "image_file",
            "accept": "image/*"
        }
    ))