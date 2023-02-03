from django import forms
from . import models

#Formulaire de création d'un client
class CreateCustomerForm(forms.ModelForm):
    class Meta:
        model = models.Customer
        fields = ['nom', 'prenom', 'numero', 'email', 'description']