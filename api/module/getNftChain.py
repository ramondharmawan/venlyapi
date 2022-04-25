from django.shortcuts import render
from django.http import HttpResponse
import requests
from . getToken import getTokens


def getnftchain(request):
    token = getTokens(HttpResponse)

    url = "https://api-business-staging.arkane.network/api/env"

    payload={}
    headers = {
        "Authorization": "Bearer {}".format(token)
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    res = response.json()

    print(res)
    return res["supportedChainsForItemCreation"]

