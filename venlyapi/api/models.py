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

class ImageContractNft(models.Model):
    owner_name = models.CharField(max_length=100, null=True, blank=True)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='imagesNFT/%Y/%m/%d/')
    chain = models.CharField(max_length=100, null=True, blank=True)
    wallet = models.CharField(max_length=100, null=True, blank=True)
    site = models.CharField(max_length=100, null=True, blank=True)
    twitter = models.CharField(max_length=100, null=True, blank=True)
    linkedin = models.CharField(max_length=100, null=True, blank=True)
    desc = models.CharField(max_length=100, null=True, blank=True)
    applicationId = models.CharField(max_length=100, null=True, blank=True)
    contracts_id = models.CharField(max_length=100,null=True, blank=True)
    hash = models.CharField(max_length=100, null=True, blank=True)
    symbol = models.CharField(max_length=100, null=True, blank=True)
    

    def __str__(self):
        return self.title

class TokenTypeNft(models.Model):
    name_token = models.CharField(max_length=100, null=True, blank=True)
    token_image = models.ImageField(upload_to='ttImages/%Y/%m/%d/')
    contract_id_token = models.CharField(max_length=100,null=True, blank=True)
    appsid_token = models.CharField(max_length=100, null=True, blank=True)
    site_url = models.CharField(max_length=100, null=True, blank=True)
    token_type_att = models.CharField(max_length=100, null=True, blank=True)
    token_name_att = models.CharField(max_length=100, null=True, blank=True)
    token_value_att = models.CharField(max_length=100, null=True, blank=True)
    token_description = models.CharField(max_length=100, null=True, blank=True)
    token_bg = models.CharField(max_length=100, null=True, blank=True)
    token_type = models.CharField(max_length=100, null=True, blank=True)
    token_hash = models.CharField(max_length=100, null=True, blank=True)
    storage_url = models.CharField(max_length=100, null=True, blank=True)
    type_storage = models.CharField(max_length=100, null=True, blank=True)
    thumbnail_url = models.CharField(max_length=100, null=True, blank=True)
    preview_url = models.CharField(max_length=100, null=True, blank=True)
    supply = models.CharField(max_length=100, null=True, blank=True)
    token_owner = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name_token

class FungibleToken(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    application_id = models.CharField(max_length=100, null=True, blank=True)
    contract_id = models.CharField(max_length=100, null=True, blank=True)
    token_id = models.CharField(max_length=100, null=True, blank=True)
    destination = models.CharField(max_length=100, null=True, blank=True)
    supply = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

class MintNft(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    application_id = models.CharField(max_length=100, null=True, blank=True)
    contract_id = models.CharField(max_length=100, null=True, blank=True)
    token_id = models.CharField(max_length=100, null=True, blank=True)
    destination = models.CharField(max_length=100, null=True, blank=True)
    supply = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name