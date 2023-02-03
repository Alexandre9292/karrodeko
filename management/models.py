from django.db import models
from django.utils.translation import gettext_lazy  as _

#Class qui gère les clients
class Customer(models.Model):
    nom = models.CharField(max_length=100, blank=True, verbose_name='Nom')
    prenom = models.CharField(max_length=100, blank=True, verbose_name='Prénom')
    numero = models.CharField(max_length=100, blank=True, verbose_name='Numéro')
    email = models.EmailField(_('email address'), unique=True)
    description = models.TextField(max_length=5000, blank=True, verbose_name='Description')
    qr_path = models.CharField(max_length=500, blank=True)
    status = models.IntegerField(blank=True, default=1)
