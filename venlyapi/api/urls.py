from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('wallet-create', views.walletcreate, name='walletcreate'),
]