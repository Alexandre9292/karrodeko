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
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),    
    path('', management.views.dashbord, name='dashbord'),
    path('customer/new', management.views.new_customer, name='new_customer'),
    path('customer/<int:customer_id>/', management.views.info_customer, name='info_customer'),
    path('customer/<int:customer_id>/edit', management.views.edit_customer, name='edit_customer'),
    path('customer/<int:customer_id>/delete', management.views.delete_customer, name='delete_customer'),
    path('customer/<int:customer_id>/delete-confirmation', management.views.delete_customer_confirmation, name='delete_customer_confirmation'),
    path('customer/<int:customer_id>/BDL', management.views.bon_de_livraison, name='bon_de_livraison'),
    path('customer/<int:customer_id>/validation', management.views.validation, name='validation'),
    path('customer/<int:customer_id>/retour-atelier', management.views.retour_atelier, name='retour_atelier'),
    path('customer/<int:customer_id>/etiquette', management.views.etiquette, name='etiquette'),
    path('customer/<int:customer_id>/etiquette/impression', management.views.etiquette_impression, name='etiquette_impression'),
    path('customer/scanner', management.views.scanner, name='scanner'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
handler404 = management.views.page_not_found_view