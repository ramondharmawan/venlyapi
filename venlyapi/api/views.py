from django.shortcuts import render
from django.http import HttpResponse
import requests
from . module.getToken import getTokens


# Create your views here.


def index(request):
    context = {}
    return render(request, 'api/api-starter.html', context)
    #return HttpResponse("Hello, world. You're at the polls index.")


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

    context = {
       "user_id": res["result"]["userId"],
       "username" : res["result"]["username"],
       "email" : res["result"]["email"],
       "nickname": res["result"]["nickname"]
    }

    print(res["result"]["userId"])
    #print(res["result"])
    #print(bearer)

    return render(request, 'api/getprofile.html', context)


def createwallet(request):
    #token = getTokens(HttpResponse)

    if request.method == 'POST':
        answer = str(request.POST['walletcreation'])
        if answer == "yes":
            print(answer)
            return render(request, 'api/walletcreation.html')
        else:
            print(answer) 
            return render(request, 'api/putwalletid.html')   





