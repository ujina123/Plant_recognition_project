from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('weather_app.urls')),
    path('plantinfo/', views.plantinfo, name="plantinfo"),
    path('plantmanage/', views.plantmanage, name="plantmanage"),
    path('plantrecog/', views.plantrecog, name="plantrecog"),
    path('plantdisease/', views.plantdisease, name="plantdisease"),
    path('search/', include('search_app.urls')),
    path('accounts/login', include('allauth.urls')),
    path('accounts/signup', include('allauth.urls')),
]