from django.urls import path
from . import views

urlpatterns = [
    path('', views.myapps, name='index')
]