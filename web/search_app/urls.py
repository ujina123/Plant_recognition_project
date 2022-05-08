# JngMkk
from django.urls import path
from search_app import views

urlpatterns = [
    path('', views.searching, name="search"),
    path('info/', views.info)
]