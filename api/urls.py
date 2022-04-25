from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    #path('get-profile', views.getprofile, name='getprofile'),
    path('create-wallet-option', views.createwalletoption, name='createwalletoption'),
    #path('wallet-id', views.walletid, name='walletid') no need of this,
    path('signup', views.signup, name='signup'),
    path('processSignup', views.processSignup, name='processSignup'),
    path('logout', views.logout, name='logout'),
    path('dashboard/<int:page>', views.dashboard, name='dashboard'),
    path('walletcreation', views.walletcreation, name='walletcreation'),
    path('deploynft', views.deploynft, name='deploynft'),
    path('deploynftprocess', views.deploynftprocess, name='deploynftprocess'),
    path('nftcontractlist', views.nftcontractlist, name='nftcontractlist'),
    path('createtokentype', views.createtokentype, name='createtokentype'),
    path('createtokentypeprocess', views.createtokentypeprocess, name='createtokentypeprocess'),
    path('tokentypelists', views.tokentypelists, name='tokentypelists'),
    path('fungibletoken', views.fungibletoken, name='fungibletoken'),
    path('createfungible', views.createfungible, name='createfungible'),
    path('fungibletokenlists', views.fungibletokenlists, name='fungibletokenlists'),
    path('mintnft', views.mintnft, name='mintnft'),
    path('processmintnft', views.processmintnft, name='processmintnft'),
    path('mintnftlists', views.mintnftlists, name='mintnftlists'),
    path('instancemintnft', views.instancemintnft, name='instancemintnft'),
    path('instancemintnftprocs', views.instancemintnftprocs, name='instancemintnftprocs'),
    path('profile', views.profile, name='profile'),
    path('updateprofile', views.updateprofile, name='updateprofile'),
    path('updatecredentials', views.updatecredentials, name='updatecredentials'),
    path('changepp', views.changepp, name='changepp'),
    path('results/<int:pk>', views.showresults, name='showresults'),
    path('result-contract/<int:pk>', views.showresultcontract, name='showresultcontract'),
    path('result-token/<int:pk>', views.showresulttoken, name='showresulttoken'),
    path('result-token-metadata-fungible/<int:pk>', views.showresulttokenmetafungible, name='showresulttokenmetafungible'),
    path('result-token-metadata-nonfungible/<int:pk>', views.showresulttokenmetanonfungible, name='showresulttokenmetanonfungible'),
    path('server-venly-error', views.serverError, name='serverError')
]

handler404 = 'api.views.error_404_view'

handler500 = 'api.views.error_500_view'