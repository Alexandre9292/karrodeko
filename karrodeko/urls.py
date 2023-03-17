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
import authentication.views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),    
    path('', management.views.dashbord, name='dashbord'),
    path('login/', authentication.views.login_page, name='login'),
    path('logout/', authentication.views.logout_user, name='logout'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='authentication/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="authentication/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='authentication/password_reset_complete.html'), name='password_reset_complete'),      
    path('password_reset', authentication.views.password_reset_request, name="password_reset"),

    path('user/new', authentication.views.new_user_page, name='new_user_page'),
    path('customer/new', management.views.new_customer, name='new_customer'),
    path('customer/import', management.views.import_customer, name='import_customer'),
    path('customer/import/create/<int:client_id>/', management.views.import_to_create_customer, name='import_to_create_customer'),
    path('customer/<int:customer_id>/', management.views.info_customer, name='info_customer'),
    path('customer/<int:customer_id>/edit', management.views.edit_customer, name='edit_customer'),
    path('customer/<int:customer_id>/delete', management.views.delete_customer, name='delete_customer'),
    path('customer/<int:customer_id>/delete-confirmation', management.views.delete_customer_confirmation, name='delete_customer_confirmation'),
    path('customer/<int:customer_id>/BDL', management.views.bon_de_livraison, name='bon_de_livraison'),
    path('customer/<int:customer_id>/en_cours/<int:statut>', management.views.en_cours, name='en_cours'),
    path('customer/<int:customer_id>/validation', management.views.validation, name='validation'),
    path('customer/<int:customer_id>/retour-atelier', management.views.retour_atelier, name='retour_atelier'),
    path('customer/<int:customer_id>/etiquette', management.views.etiquette, name='etiquette'),
    path('customer/<int:customer_id>/etiquette/impression', management.views.etiquette_impression, name='etiquette_impression'),
    path('customer/scanner', management.views.scanner, name='scanner'),
    path('customer/<int:customer_id>/BDL/mail/<int:bdl_id>/', management.views.send_bdl, name='send_bdl'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
handler404 = management.views.page_not_found_view