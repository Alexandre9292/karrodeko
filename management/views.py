from django.shortcuts import render, redirect, get_object_or_404
from . import forms, models

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
    return render(request, 'management/edit_customer.html', context={'form': form})

#Info du client
def info_customer(request, customer_id):
    customer = get_object_or_404(models.Customer, id=customer_id)
    return render(request, 'management/info_customer.html', context={'customer': customer})

#Bon de commande    
def bon_de_commande(request):
    return render(request, 'management/bon_de_commande.html')

#Etiquette
def etiquette(request, customer_id):
    customer = get_object_or_404(models.Customer, id=customer_id)
    return render(request, 'management/etiquette.html', context={'customer': customer})
