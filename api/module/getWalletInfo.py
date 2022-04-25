from django.shortcuts import render
from django.http import HttpResponse
import requests
from . getToken import getTokens


def getwalletinfo(request):
    url = "https://api-staging.arkane.network/api/wallets/4a7e651a-d3e9-4d3b-9bcf-a7e0d0e42a54"

    token = getTokens(HttpResponse)

    payload={}
    headers = {
        "Authorization": "Bearer {}".format(token)
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    res = response.json()

    return res
