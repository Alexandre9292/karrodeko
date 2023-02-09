from django.db import models
from django.contrib.auth.models import AbstractUser, Group, BaseUserManager 
from django.utils.translation import gettext_lazy  as _

#Class qui configure la class user
class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


#Class qui gère les Users
class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    ADMINISTRATION = 'ADMIN'
    AUTRE = 'AUTRE'

    ROLE_CHOICES = (
        (ADMINISTRATION, 'Admin'),
        (AUTRE, 'Autre'),
    )

    role = models.CharField(max_length=30, choices=ROLE_CHOICES, verbose_name='rôle')

    objects = UserManager()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.role == self.ADMINISTRATION:
            group = Group.objects.get(name='administrator')
            group.user_set.add(self)
        elif self.role == self.AUTRE:
            group = Group.objects.get(name='autre')
            group.user_set.add(self)
