from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField(null=True, blank=True)


class CustomerInfo(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    pincode = models.IntegerField(null=True, blank=True)
    secrettype = models.CharField(max_length=100, null=True, blank=True)
    wallettype = models.CharField(max_length=100, null=True, blank=True)
    walletid = models.CharField(max_length=200, null=True, blank=True)
    walletaddress = models.CharField(max_length=200, null=True, blank=True)
    creating = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.name