# JngMkk
from django.urls import path
from . import views

app_name = "diseaseimage"

urlpatterns = [
    path("", views.getImage, name="diseaseimage"),
    path("info/", views.info, name="diseaseinfo")
]