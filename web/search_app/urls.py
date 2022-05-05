from django.urls import path
from search_app import views

urlpatterns = [
    path('', views.search, name="search"),
    path('info/', views.info)
]