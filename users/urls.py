from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_go, name='login'),
    path('register/', views.register_request, name='register'),
]
