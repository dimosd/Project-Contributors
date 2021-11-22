from django.db import models
from django.utils import timezone
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

class User(AbstractBaseUser, PermissionsMixin):


    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=False)
    age = models.IntegerField(null=False, default=0)
    country = models.CharField(max_length=255, null=False)
    residence = models.CharField(max_length=255, null=False)
    email = models.EmailField(max_length=255, null=False)
    username = models.CharField(max_length=255, null=False, unique=True)
    password = models.CharField(max_length=50)
    skills = models.CharField(max_length=255, null=False, default="[]")
    is_registered = models.BooleanField(null=True, default=True)
    last_login = models.DateTimeField(null=True, default=timezone.now)
    is_staff = models.BooleanField(default=False, null=True)
    is_superuser =  models.BooleanField(default=False, null=True)
    is_active = models.BooleanField(default=True)

    
    objects = UserManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []