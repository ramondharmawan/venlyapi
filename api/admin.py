from django.contrib import admin
from .models import Profile, CustomerInfo, ImageContractNft, TokenTypeNft, FungibleToken, MintNft

# Register your models here.
admin.site.register(Profile)
admin.site.register(CustomerInfo)
admin.site.register(ImageContractNft)
admin.site.register(TokenTypeNft)
admin.site.register(FungibleToken)
admin.site.register(MintNft)