from django.shortcuts import render
from django.http import HttpResponse
import requests
from . getToken import getTokens


def getchain(request):
    token = getTokens(HttpResponse)

    url = "https://api-staging.arkane.network/api/chains"

    payload={}
    headers = {
        "Authorization": "Bearer {}".format(token)
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    res = response.json()

    print(res)
    return res["result"]