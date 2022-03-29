from django.contrib import admin
from .models import Profile, CustomerInfo, ImageContractNft, TokenTypeNft

# Register your models here.
admin.site.register(Profile)
admin.site.register(CustomerInfo)
admin.site.register(ImageContractNft)
admin.site.register(TokenTypeNft)