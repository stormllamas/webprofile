from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('about/', views.About.as_view(), name='about'),
    # path('contact/', views.contact, name='contact')
    path('contact/', views.ContactView.as_view(), name='contact')
]