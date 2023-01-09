from django.db import models
from django.contrib.auth.models import AbstractUser,PermissionsMixin,UserManager

# Create your models manager here.
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from django.apps import apps

class MyUserManager(UserManager):
    
    def _create_user(self,  email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        
        if not email:
            raise ValueError("The given email must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self,  email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user( email, password, **extra_fields)

    def create_superuser(self,  email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)



# Create your models here.
class User(AbstractUser):
    name=models.CharField(max_length=255)
    email=models.EmailField(max_length=255,unique=True)
    username=None
    password=models.CharField(max_length=255)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]
    objects = MyUserManager()