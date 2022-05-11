from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('', views.main, name="main"),
    path("weather/", views.weather, name="weather"),
    path('plantinfo/', views.plantinfo, name="plantinfo"),
    path('plantdelete/', views.plantdelete, name="plantdelete"),
    path('plantmanage/', views.plantmanage, name="plantmanage"),
    path('plantrecog/', include("plantimage.urls")),
    path('plantdisease/', include("diseaseimage.urls")),
    path('search/', include('search_app.urls')),
    path('accounts/login', include('allauth.urls')),
    path('accounts/signup', include('allauth.urls')),
    path('plantrequest/', views.plantrequest, name='plantrequest'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)