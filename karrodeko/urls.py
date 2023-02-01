"""karrodeko URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
import management.views

urlpatterns = [
    path('admin/', admin.site.urls),    
    path('', management.views.dashbord, name='dashbord'),
    path('customer/new', management.views.new_customer, name='new_customer'),
    path('customer/<int:customer_id>/', management.views.info_customer, name='info_customer'),
    path('customer/<int:customer_id>/edit', management.views.edit_customer, name='edit_customer'),
    path('customer/<int:customer_id>/BDC', management.views.bon_de_commande, name='bon_de_commande'),
    path('customer/<int:customer_id>/etiquette', management.views.etiquette, name='etiquette'),
]
