# urls.py

from django.urls import path
from django.contrib.auth import views as auth_views

app_name = "users"
urlpatterns=[
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
  # django.contrib.auth앱의 LoginView 클래스를 활용했으므로 별도의 views.py 파일 수정이 필요 없음
]