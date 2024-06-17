"""
URL configuration for Ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import  views
from django.urls import path
from .views import  payment_success

urlpatterns = [
    path('', views.index, name="index"),
    path('about/', views.about, name="about"),
    path('contact/', views.contact, name="contactUs"),
    path('tracker/', views.tracker, name="trackingStatus"),
    path('search/', views.search, name="search"),
    path("products/<int:myid>", views.products, name="Products"),
    path('checkout/', views.checkout, name="checkout"),
    path('payment-success/', payment_success, name='payment_success'),
    path('subcategory/<str:subcategory>/', views.subcategory_view, name='subcategory'),
]
