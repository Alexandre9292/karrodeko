from django.shortcuts import render, redirect, get_object_or_404
from . import forms, models
import qrcode
from django.conf import settings
from django.urls import reverse
import os
from urllib.parse import urlparse


#Dashbord
def dashbord(request):
    customers = models.Customer.objects.all()
    return render(request, 'management/dashbord.html', context={'list_customer': customers})

#Nouveau client
def new_customer(request):
    form = forms.CreateCustomerForm()
    if request.method == 'POST':
        form = forms.CreateCustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            return redirect('etiquette', customer_id=customer.id)
    return render(request, 'management/new_customer.html', context={'form': form})

#Modifier client
def edit_customer(request, customer_id):
    customer = get_object_or_404(models.Customer, id=customer_id)
    form = forms.CreateCustomerForm(instance=customer)
    if request.method == 'POST':
        form = forms.CreateCustomerForm(request.POST, instance=customer)
        if form.is_valid():
            customer = form.save()
            return redirect('etiquette', customer_id=customer.id)
    return render(request, 'management/edit_customer.html', context={'form': form, 'customer': customer})

#Supprimer client
def delete_customer(request, customer_id):
    customer = get_object_or_404(models.Customer, id=customer_id)
    customer.delete()
    customers = models.Customer.objects.all()
    return render(request, 'management/dashbord.html', context={'list_customer': customers})

#Confirmation de suppression client
def delete_customer_confirmation(request, customer_id):
    customer = get_object_or_404(models.Customer, id=customer_id)
    return render(request, 'management/delete_customer.html', context={'customer': customer})    

#Info du client
def info_customer(request, customer_id):
    customer = get_object_or_404(models.Customer, id=customer_id)
    return render(request, 'management/info_customer.html', context={'customer': customer})

#Bon de commande    
def bon_de_livraison(request, customer_id):
    customer = get_object_or_404(models.Customer, id=customer_id)
    return render(request, 'management/bdl.html', context={'customer': customer})

#Validation  
def validation(request, customer_id):
    customer = get_object_or_404(models.Customer, id=customer_id)
    customer.status = 3
    customer.save()
    return render(request, 'management/info_customer.html', context={'customer': customer})

#Retour en attelier  
def retour_atelier(request, customer_id):
    customer = get_object_or_404(models.Customer, id=customer_id)
    customer.status = 2
    customer.save()
    return render(request, 'management/info_customer.html', context={'customer': customer})

#Etiquette
def etiquette(request, customer_id):
    customer = get_object_or_404(models.Customer, id=customer_id)
    directory = str(settings.BASE_DIR) + settings.MEDIA_URL + str(customer.id) + customer.nom + customer.prenom

    if os.path.isdir(directory) is False :
        os.makedirs(directory)
        url = request.build_absolute_uri(reverse("info_customer", args=[customer_id]))
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img.save(directory + "/code.jpg")
        customer.qr_path = settings.MEDIA_URL + str(customer.id) + customer.nom + customer.prenom + "/code.jpg"
        customer.save()
    
    code_url = customer.qr_path

    return render(request, 'management/etiquette.html', context={'customer': customer, 'code_url': code_url})

#Impression de l'étiquette
def etiquette_impression(request, customer_id):
    customer = get_object_or_404(models.Customer, id=customer_id)
    return render(request, 'management/info_customer.html', context={'customer': customer})

#Fonction de scanner
def scanner(request):
     return redirect('dashbord')

#Redirection en cas d'erreur 404
def page_not_found_view(request, exception):
     return redirect('dashbord')

