from django import forms
from . import models

#Formulaire de création d'un client
class CreateCustomerForm(forms.ModelForm):
    class Meta:
        model = models.Customer
        fields = ['nom', 'prenom', 'numero', 'email', 'description']

#Formulaire de création d'un bon de livraison
class CreateSignatureForm(forms.Form):
    signature_client = forms.CharField(max_length = 1000, label='Signature Client')
    signature_KD = forms.CharField(max_length = 1000, label='Signature KARRO DEKO')