from django.shortcuts import render, redirect, get_object_or_404
from . import forms, models
import qrcode
from django.conf import settings
from django.urls import reverse
import os
import cv2
from pyzbar import pyzbar
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
    return redirect('dashbord')  

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
    
    code_url = settings.MEDIA_URL + str(customer.id) + customer.nom + customer.prenom + "/code.jpg"

    return render(request, 'management/etiquette.html', context={'customer': customer, 'code_url': code_url})

#Impression de l'étiquette
def etiquette_impression(request, customer_id):
    customer = get_object_or_404(models.Customer, id=customer_id)
    return render(request, 'management/info_customer.html', context={'customer': customer})

#Fonction de scanner
def scanner(request):
    # Ouvrir la caméra
    cap = cv2.VideoCapture(0)
    
    # Boucle tant que la caméra est ouverte
    while True:
        # Lire la prochaine image de la caméra
        ret, frame = cap.read()
        
        # Détecter les codes QR dans l'image
        codes = pyzbar.decode(frame)
        
        # Afficher les codes QR sur l'image
        for code in codes:
            (x, y, w, h) = code.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            
        # Afficher l'image
        cv2.imshow("Scan QR Code", frame)
        
        # Si un code QR est détecté, sortir de la boucle
        if codes:
            break
        
        # Attendre 10 ms pour vérifier si l'utilisateur a appuyé sur la touche "q"
        key = cv2.waitKey(10)
        if key == ord("q"):
            break
    
    # Fermer la caméra
    cap.release()
    
    # Détruire les fenêtres OpenCV
    cv2.destroyAllWindows()
    
    # Renvoyer le premier code QR trouvé
    if codes:
        # Code to detect QR code and get the decoded data
        decoded_data = codes[0].data.decode("utf-8")
        url = urlparse(decoded_data)
        if url.scheme and url.netloc and url.path:
            return redirect(decoded_data)
        else:
            # Handle invalid URL
            return redirect('dashbord')
    
    return redirect('dashbord')
