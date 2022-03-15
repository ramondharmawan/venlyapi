from django.shortcuts import render
from django.http import HttpResponse
import requests
from . module.getToken import getTokens
import smtplib, ssl


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


def createwalletoption(request):
    #token = getTokens(HttpResponse)

    if request.method == 'POST':
        answer = str(request.POST['walletcreation'])
        if answer == "yes":
            print(answer)
            return render(request, 'api/putwalletid.html')
        else:
            print(answer) 
            return render(request, 'api/walletcreation.html')   


def walletcreation(request):
    token = getTokens(HttpResponse)

    if request.method == 'POST':
        desc = request.POST['desc']
        username = request.POST['username']
        email = request.POST['email']
        secrettype = request.POST['secrettype']
        wallettype = request.POST['wallettype']
        pincode = request.POST['pincode']
    else:
        return render(request,'api/walletcreation.html')

def deployNft(request):
    token = getTokens(HttpResponse)

    if request.method == 'POST':
        aplid = request.POST['applicationId']
        descnft = request.POST['descriptionNft']
        image = request.POST['imageUrl']
        chainNft = request.POST['chainNft']
        ownerNft = request.POST['walletaddress']


    url = "https://api-business-staging.arkane.network/api/apps/dummy-applicationid-abc123/contracts"

    payload = json.dumps({
    "name": "Venly",
    "description": "Example contract created using the VENLY NFT API",
    "image": "https://gblobscdn.gitbook.com/spaces%2F-MB9NX0aClLh4Gx_kawF%2Favatar-1623151896040.png?alt=media",
    "externalUrl": "https://venly.io",
    "media": [
        {
        "type": "twitter",
        "value": "https://twitter.com/Venly_io"
        },
        {
        "type": "linkedin",
        "value": "https://www.linkedin.com/company/venly-io"
        }
    ],
    "chain": "MATIC",
    "owner": "0xF4Cc6E6c585d23585d5F08BDaEE9b85aB658fa95"
    })
    headers = {
    'Content-Type': 'application/json',
    'Authorization": "Bearer {}'.format(token)
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


