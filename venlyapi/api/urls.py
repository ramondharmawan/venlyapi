from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get-profile', views.getprofile, name='getprofile'),
    path('create-wallet-option', views.createwalletoption, name='createwalletoption'),
    #path('wallet-id', views.walletid, name='walletid') no need of this,
    path('signup', views.signup, name='signup'),
    path('processSignup', views.processSignup, name='processSignup'),
    path('logout', views.logout, name='logout'),
]