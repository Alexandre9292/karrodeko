import base64
from django.shortcuts import render, redirect, get_object_or_404
from . import forms, models
import qrcode
from django.conf import settings
from django.urls import reverse
import os
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required, permission_required

from weasyprint import HTML
from datetime import date

from django.core.mail import EmailMessage
import shutil


#Dashbord
@login_required
def dashbord(request):
    customers = models.Customer.objects.all().order_by('-id')
    return render(request, 'management/dashbord.html', context={'list_customer': customers})

#Nouveau client
@login_required
def new_customer(request):
    form = forms.CreateCustomerForm()
    if request.method == 'POST':
        form = forms.CreateCustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()

            clients = models.Clients.objects.all()
            client = models.Clients(nom=customer.nom, prenom=customer.prenom, numero=customer.numero, email=customer.email, email2=customer.email2)
            save = True
            for c in clients :
                if client.nom == c.nom and client.prenom == c.prenom and client.email == c.email and client.email2 == c.email2 :
                    save = False
            if save :
                client.save()

            customer.client = client

            fichier = '/signature_client_commande.png';               
            directory = str(settings.BASE_DIR) + settings.MEDIA_URL + str(customer.id) + customer.nom + customer.prenom 
                    
            if os.path.isdir(directory) is False :
                os.makedirs(directory)

            signatureC = request.POST['signature_client_commande']
            if signatureC and os.path.isfile(os.path.join(directory, fichier)) is False :
                # enregistrer le fichier PNG
                image_sign = open(directory + fichier, 'w')
                with open(directory + fichier, "wb") as f:
                    f.write(base64.b64decode(signatureC.split(",")[1]))
                image_sign.close()
                
                customer.signature_client_commande_path = settings.MEDIA_URL + str(customer.id) + customer.nom + customer.prenom + fichier  

                customer.is_signed_commande = True
                customer.status = models.EN_ATTENTE
                
            customer.save()
            return redirect('etiquette', customer_id=customer.id)

    return render(request, 'management/new_customer.html', context={'form': form, 'date': date.today()})

#Import client
@login_required
def import_customer(request):
    clients = models.Clients.objects.all().order_by('nom')
    return render(request, 'management/import_customer.html', context={'clients': clients})

#Création aprés import client
@login_required
def import_to_create_customer(request, client_id):
    client = get_object_or_404(models.Clients, id=client_id)  
    new_customer = models.Customer(nom=client.nom, prenom=client.prenom, numero=client.numero, email=client.email, email2=client.email2)

    form = forms.CreateCustomerForm(instance=new_customer)
    if request.method == 'POST':
        form = forms.CreateCustomerForm(request.POST, instance=new_customer)
        if form.is_valid():
            customer = form.save()

            clients = models.Clients.objects.all()
            client_tmp = models.Clients(nom=customer.nom, prenom=customer.prenom, numero=customer.numero, email=customer.email, email2=customer.email2)
            save = True
            for c in clients :
                if client_tmp.nom == c.nom and client_tmp.prenom == c.prenom and client_tmp.email == c.email and client_tmp.email2 == c.email2 :
                    save = False
            if save :
                client_tmp.save()
                customer.client = client_tmp
            else :
                customer.client = client

            fichier = '/signature_client_commande.png';               
            directory = str(settings.BASE_DIR) + settings.MEDIA_URL + str(customer.id) + customer.nom + customer.prenom 
                    
            if os.path.isdir(directory) is False :
                os.makedirs(directory)

            signatureC = request.POST['signature_client_commande']
            if signatureC and os.path.isfile(os.path.join(directory, fichier)) is False :
                # enregistrer le fichier PNG
                image_sign = open(directory + fichier, 'w')
                with open(directory + fichier, "wb") as f:
                    f.write(base64.b64decode(signatureC.split(",")[1]))
                image_sign.close()
                
                customer.signature_client_commande_path = settings.MEDIA_URL + str(customer.id) + customer.nom + customer.prenom + fichier  

                customer.is_signed_commande = True
        
            
            customer.save()
            return redirect('etiquette', customer_id=customer.id)
        
    return render(request, 'management/new_customer_import.html', context={'form': form, 'date': date.today()})

#Modifier client
@login_required
def edit_customer(request, customer_id):
    customer = get_object_or_404(models.Customer, id=customer_id)  
    client = get_object_or_404(models.Clients, id=customer.client.id)   
    descriptions = customer.get_description()
    form = forms.CreateCustomerForm(instance=customer)
    if request.method == 'POST':
        form = forms.CreateCustomerForm(request.POST, instance=customer)
        if form.is_valid():

            customer = form.save()
            
            client.nom = customer.nom
            client.prenom = customer.prenom
            client.numero = customer.numero
            client.email = customer.email
            client.email2 = customer.email2
            client.save()
            
            fichier = '/signature_client_commande.png';               
            directory = str(settings.BASE_DIR) + settings.MEDIA_URL + str(customer.id) + customer.nom + customer.prenom 
                    
            if os.path.isdir(directory) is False :
                os.makedirs(directory)

            signatureC = request.POST['signature_client_commande']
            if signatureC and os.path.isfile(os.path.join(directory, fichier)) is False :
                # enregistrer le fichier PNG
                image_sign = open(directory + fichier, 'w')
                with open(directory + fichier, "wb") as f:
                    f.write(base64.b64decode(signatureC.split(",")[1]))
                image_sign.close()
                
                customer.signature_client_commande_path = settings.MEDIA_URL + str(customer.id) + customer.nom + customer.prenom + fichier  

                customer.is_signed_commande = True
                customer.save()
        
            
            return redirect('etiquette', customer_id=customer.id)
        
    return render(request, 'management/edit_customer.html', context={'form': form, 'customer': customer, 'descriptions': descriptions})

#Supprimer Customer
@login_required
def delete_customer(request, customer_id):
    customer = get_object_or_404(models.Customer, id=customer_id)
    directory = str(settings.BASE_DIR) + settings.MEDIA_URL + str(customer.id) + customer.nom + customer.prenom
    if os.path.exists(directory):
        shutil.rmtree(directory)
    customer.delete()
    customers = models.Customer.objects.all().order_by('-id')
    return render(request, 'management/dashbord.html', context={'list_customer': customers})

#Confirmation de suppression Customer
@login_required
def delete_customer_confirmation(request, customer_id):
    customer = get_object_or_404(models.Customer, id=customer_id)
    return render(request, 'management/delete_customer.html', context={'customer': customer})  

#Supprimer client
@login_required
def delete_client(request, client_id):
    client = get_object_or_404(models.Clients, id=client_id)
    client.delete()
    clients = models.Clients.objects.all().order_by('nom')
    return render(request, 'management/import_customer.html', context={'clients': clients})

#Confirmation de suppression client
@login_required
def delete_client_confirmation(request, client_id):
    client = get_object_or_404(models.Clients, id=client_id)
    return render(request, 'management/delete_client.html', context={'client': client})   

#Info du client
@login_required
def info_customer(request, customer_id):
    customer = get_object_or_404(models.Customer, id=customer_id)
    descriptions = customer.get_description()
    return render(request, 'management/info_customer.html', context={'customer': customer, 'descriptions': descriptions})

#Bon de commande    
@login_required
def bon_de_livraison(request, customer_id):
    customer = get_object_or_404(models.Customer, id=customer_id)
    descriptions = customer.get_description()
    if models.BDL.objects.filter(customer=customer).exists():
        bdl = models.BDL.objects.filter(customer=customer)
        bdl = bdl[0]
    else:
        bdl = models.BDL(customer=customer)
        bdl.save()

    form = forms.CreateSignatureForm()
    if request.method == 'POST':
        form = forms.CreateSignatureForm(request.POST)
        fichierC = '/signature_client.png';    
        fichierK = '/signature_KD.png';               
        directory = str(settings.BASE_DIR) + settings.MEDIA_URL + str(customer.id) + customer.nom + customer.prenom 
                
        if os.path.isdir(directory) is False :
            os.makedirs(directory)

        signatureC = request.POST['signature_client']
        signatureK = request.POST['signature_KD']
        if signatureC or signatureK:    
            if signatureC and os.path.isfile(os.path.join(directory, fichierC)) is False :
                # enregistrer le fichier PNG
                image_sign = open(directory + fichierC, 'w')
                with open(directory + fichierC, "wb") as f:
                    f.write(base64.b64decode(signatureC.split(",")[1]))
                image_sign.close()
                
                customer.signature_client_path = settings.MEDIA_URL + str(customer.id) + customer.nom + customer.prenom + fichierC                
                bdl.is_signed_client = True
            if signatureK and os.path.isfile(os.path.join(directory, fichierK)) is False :
                # enregistrer le fichier PNG
                image_sign = open(directory + fichierK, 'w')
                with open(directory + fichierK, "wb") as f:
                    f.write(base64.b64decode(signatureK.split(",")[1]))
                image_sign.close()
                
                customer.signature_KD_path = settings.MEDIA_URL + str(customer.id) + customer.nom + customer.prenom + fichierK                
                bdl.is_signed_KD = True

            customer.save() 
            bdl.save()
        return redirect('bon_de_livraison', customer_id=customer.id)

    return render(request, 'management/bdl.html', context={'form': form, 'customer': customer, 'bdl': bdl, 'descriptions': descriptions})

#Génère le pdf et envoie le mail
@login_required
def send_bdl(request, customer_id, bdl_id):
    
    customer = get_object_or_404(models.Customer, id=customer_id)
    bdl = get_object_or_404(models.BDL, id=bdl_id)
    descriptions = customer.get_description()

    customer.status =  models.TERMINE
    customer.save() 

    # Générer le HTML à partir d'une vue Django
    html = render_to_string('management/bon_de_livraison_pdf.html', {'customer': customer, 'bdl': bdl, 'descriptions': descriptions})

    directory = str(settings.BASE_DIR) + settings.MEDIA_URL + str(customer.id) + customer.nom + customer.prenom
    if os.path.isdir(directory) is False :
        os.makedirs(directory)

    HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(directory + '/BonDeLivraison.pdf')

    
    if os.path.isfile(directory + '/signature_client.png') and os.path.isfile(directory + '/signature_KD.png') : 
        #Envoie du mail
        message = "Bonjour," + "\n\n" + "Vous trouverez ci-joint le bon de livraison, suite à votre commande chez KARRO DEKO." + "\n\n" + "Au plaisir de vous revoir" + "\n\n" + "Cordialement," + "\n\n" + "KARRO DEKO"
        recipient_list = ["karro.deko@gmail.com", customer.email, customer.email2]
        email = EmailMessage("[KARRO DEKO] Bon de livraison", message, to=recipient_list)
        email.attach_file(directory + "/BonDeLivraison.pdf")
        email.send()

        """ recipient_list = [customer.email]
        email = EmailMessage("[KARRO DEKO] Bon de livraison", message, to=recipient_list)
        email.attach_file(directory + "/BonDeLivraison.pdf")
        email.send() """

    return redirect('bon_de_livraison', customer_id=customer.id)

#Validation
@login_required  
def en_cours(request, customer_id, statut):
    customer = get_object_or_404(models.Customer, id=customer_id)
    customer.status = statut
    customer.save()
    descriptions = customer.get_description()
    return render(request, 'management/info_customer.html', context={'customer': customer, 'descriptions': descriptions})

#Validation
@login_required  
def validation(request, customer_id):
    customer = get_object_or_404(models.Customer, id=customer_id)
    if customer.to_deliver :
        customer.status = models.A_LIVRE
    else :
        customer.status = models.A_RECUPERER
    customer.save()
    descriptions = customer.get_description()
    return render(request, 'management/info_customer.html', context={'customer': customer, 'descriptions': descriptions})

#Retour en attelier  
@login_required
def retour_atelier(request, customer_id):
    customer = get_object_or_404(models.Customer, id=customer_id)
    customer.status = models.EN_ATTENTE
    customer.save()
    descriptions = customer.get_description()
    return render(request, 'management/info_customer.html', context={'customer': customer, 'descriptions': descriptions})

#Etiquette
@login_required
def etiquette(request, customer_id):
    customer = get_object_or_404(models.Customer, id=customer_id)
    directory = str(settings.BASE_DIR) + settings.MEDIA_URL + str(customer.id) + customer.nom + customer.prenom

    if os.path.isdir(directory) is False :
        os.makedirs(directory)
    
    if os.path.isfile(os.path.join(directory, "/code.jpg")) is False :
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
@login_required
def etiquette_impression(request, customer_id):
    customer = get_object_or_404(models.Customer, id=customer_id)
    return render(request, 'management/etiquette_imp.html', context={'customer': customer, 'code_url': customer.qr_path})

#Fonction de scanner
@login_required
def scanner(request):
    return render(request, 'management/scan_code.html')

#Redirection en cas d'erreur 404
@login_required
def page_not_found_view(request, exception):
     return redirect('dashbord')

