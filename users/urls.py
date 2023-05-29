from django import views
from django.urls import path
from .views import  addcomment, home, RegisterView
from . import views
urlpatterns = [
    path('', views.index, name='users-home'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('addservice/', views.addservice, name='addservice'),
    path('service/<int:service_id>/', views.service_detail, name='service_detail'),
    path('addpersonnel/', views.addpersonnel, name='addpersonnel'),
    path('personnel/<int:personnel_id>/', views.personnel_detail, name='personnel_detail'),
    path('addprojet/', views.addprojet, name='addprojet'),
    path('projet/<int:projet_id>/', views.projet_detail, name='projet_detail'),
    path('addcontact/', views.addcontact, name='addcontact'),
    path('contact/<int:contact_id>/', views.contact_detail, name='contact_detail'),
    path('mespersonnels/', views.mespersonnels, name='mespersonnels'),
    path('addcomment/', addcomment, name='addcomment'),

   
]
