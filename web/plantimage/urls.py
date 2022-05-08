# JngMkk
from django.urls import path
from . import views

app_name = "plantimage"

urlpatterns = [
    path("", views.getImage, name="plantimage")
]