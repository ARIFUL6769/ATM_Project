"""
URL configuration for ATM_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
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

from atm import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('Account_Information/', views.Account_Information, name='account_information'),
    path('change_pin/', views.change_pin, name='change_pin'),
    path('create_acc/', views.create_account, name='create_account'),
    path('Deposit/', views.deposit, name='deposit'),
    path('Withdraw/', views.withdraw, name='withdraw'),
    path('Transfer/', views.transfer, name='transfer'),
    path('Transfer_History/', views.transfer_history, name='transfer_history'),
    path('logout/', views.logout, name='logout'),
    path('login/', views.login, name='login'),
    path('balance/', views.check_balance, name='check_balance'),
    path('contact/', views.contact, name='contact'),
    path('privacy/', views.privacy, name='privacy'),
    
]
