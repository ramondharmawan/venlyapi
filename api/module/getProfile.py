from django.shortcuts import render
from django.http import HttpResponse
import requests
from . getToken import getTokens


def getprofile(request):

    token = getTokens(HttpResponse)
    #bearer = "Bearer {}".format(token)

    url = "https://api-staging.arkane.network/api/profile"

    payload={}
    headers = {
         "Authorization": "Bearer {}".format(token)
    }
    #headers["Accept"] = "application/json"

    response = requests.request("GET", url, headers=headers, data=payload)

    #print(response.text)
    res = response.json()

    return res["result"]

    #context = {
    #   "user_id": res["result"]["userId"],
    #   "username" : res["result"]["username"],
    #   "email" : res["result"]["email"],
    #   "nickname": res["result"]["nickname"]
    #}

    #print(res["result"]["userId"])
    #print(res["result"])
    #print(bearer)

    #return render(request, 'api/getprofile.html', context)