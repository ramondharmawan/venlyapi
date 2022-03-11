from django.shortcuts import render
from django.http import HttpResponse
import requests
from . module.getToken import getTokens


# Create your views here.


def index(request):
    context = {}
    return render(request, 'api/api-starter.html', context)
    #return HttpResponse("Hello, world. You're at the polls index.")


def walletcreate(request):

    token = getTokens(HttpResponse)

    url = "https://api-staging.arkane.network/api/profile"

    payload={}
    headers = {}
    headers["Accept"] = "application/json"
    headers["Authorization"] = "Bearer {token}"

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)

    context = {
        
    }

    #print(token)

    return render(request, 'api/create-wallet.html', context)
