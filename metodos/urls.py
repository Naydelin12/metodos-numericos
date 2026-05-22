from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('newton/', views.newton, name='newton'),
    path('secante/', views.secante, name='secante'),
]