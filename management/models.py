from django.db import models
from django.utils.translation import gettext_lazy  as _

#Class qui gère les clients
class Customer(models.Model):
    nom = models.CharField(max_length=100, blank=True, verbose_name='Nom')
    prenom = models.CharField(max_length=100, blank=True, verbose_name='Prénom')
    numero = models.CharField(max_length=100, blank=True, verbose_name='Numéro')
    email = models.EmailField(_('email address'), unique=True)
    description = models.TextField(blank=True, verbose_name='Description')
    qr_path = models.CharField(max_length=500, blank=True)
    status = models.IntegerField(blank=True, default=1)
    signature_client_path = models.CharField(max_length=500, blank=True)
    signature_KD_path = models.CharField(max_length=500, blank=True)

    def get_description(self):
        return self.description.split(';')

#Class qui gère les bon de livraisons
class BDL(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date_livraison = models.DateTimeField(auto_now_add=True)
    is_signed_client = models.BooleanField(default=False)
    is_signed_KD = models.BooleanField(default=False)
