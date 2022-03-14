from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get-profile', views.getprofile, name='getprofile'),
    path('create-wallet', views.createwallet, name='createwallet'),
    #path('wallet-id', views.walletid, name='walletid') no need of this,
]