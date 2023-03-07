from django.db import models
from django.utils.translation import gettext_lazy  as _

#Status des customer
EN_ATTENTE = 1
EN_COURS_GRANITE = 2
EN_COURS_PLINTHE = 3
A_RECUPERER = 4
A_LIVRE = 5
TERMINE = 6

#Class qui gère les clients
class Customer(models.Model):
    nom = models.CharField(max_length=100, blank=True, default="", verbose_name='Nom')
    prenom = models.CharField(max_length=100, blank=True, default="", verbose_name='Prénom')
    numero = models.CharField(max_length=100, blank=True, default="", verbose_name='Numéro')
    email = models.EmailField(_('email address'), unique=False)
    description = models.TextField(blank=True, verbose_name='Description')
    qr_path = models.CharField(max_length=500, blank=True)
    status = models.IntegerField(blank=True, default=1)
    to_deliver = models.BooleanField(default=False)
    signature_client_path = models.CharField(max_length=500, blank=True)
    signature_KD_path = models.CharField(max_length=500, blank=True)
    signature_client_commande_path = models.CharField(max_length=500, blank=True)
    date_commande = models.DateTimeField(auto_now_add=True, null=True)
    is_signed_commande = models.BooleanField(default=False)

    def get_description(self):
        return self.description.split(';')

#Class qui gère les bon de livraisons
class BDL(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date_livraison = models.DateTimeField(auto_now_add=True)
    is_signed_client = models.BooleanField(default=False)
    is_signed_KD = models.BooleanField(default=False)
