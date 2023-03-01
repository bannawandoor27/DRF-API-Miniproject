from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=255)
    mobile_number = models.IntegerField()
    email = models.EmailField(unique=True,max_length=255)
    password = models.CharField(max_length=100)
    date_of_birth = models.DateField(max_length=8)
    profile_picture = models.ImageField(upload_to='profile_pictures',blank=True,null=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [ 'username','mobile_number','password','date_of_birth','name',]


    