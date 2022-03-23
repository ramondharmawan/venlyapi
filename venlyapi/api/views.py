from django.shortcuts import render,redirect
from django.http import HttpResponse
import requests, json
from . module.getToken import getTokens
from . module.getProfile import getprofile
from . module.getChain import getchain
from . module.getWalletClient import clientdata
import yagmail
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponseRedirect
from . models import CustomerInfo


# Create your views here.


def index(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'],password = request.POST['password'])
        if user is not None:
            auth.login(request,user)
            return redirect('dashboard')
        else:
            return render (request,'api/login.html', {'error':'Username or password is incorrect!'})
    else:
        return render(request,'api/login.html')
    #return HttpResponse("Hello, world. You're at the polls index.")

def signup(request):
    context = {}
    return render(request, 'api/create-user.html', context)

def dashboard(request):
    if request.user.is_authenticated:
        current_user = request.user

        token = getTokens(HttpResponse)
        profile = getprofile(HttpResponse)
        chain = getchain(HttpResponse)
        dataclient = clientdata(HttpResponse)

        print(dataclient)

        context = {
            'user': current_user,
            "user_id": profile["userId"],
            "nickname": profile["nickname"],
            "bearer":token,
            "chaintoken": chain,
            "datacust":dataclient
        }

        return render(request, 'api/dashboard.html', context)
    else:
        return render(request, 'api/login.html')
    

def processSignup(request):
    if request.method == "POST":
        if request.POST['password1'] == request.POST['password2']:
            try:
                User.objects.get(username = request.POST['username'])
                return render (request,'api/create-user.html', {'error':'Username is already taken!'})
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['username'],password=request.POST['password1'])
                auth.login(request,user)
                return redirect('index')
        else:
            return render (request,'api/create-user.html', {'error':'Password does not match!'})
    else:
        return render(request,'api/create-user.html')

# ini juga bisa
#def logout(request):
#    if request.method == 'GET':
#        auth.logout(request)
#    return redirect('index')

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")


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

        url = "https://api-staging.arkane.network/api/wallets"

        payload = json.dumps({
        "pincode": pincode,
        "description": desc,
        "identifier": "type=unrecoverable",
        "secretType": secrettype,
        "walletType": wallettype
        })
        headers = {
        'Content-Type': 'application/json',
        "Authorization": "Bearer {}".format(token)
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        res = response.json()

        walletid = res["result"]["id"]
        walletaddress = res["result"]["address"]
        creating = res["result"]["createdAt"]

        CustomerInfo.objects.create(
            name=username,
            email=email,
            description=desc,
            secrettype=secrettype,
            wallettype=wallettype,
            pincode=pincode,
            walletid=walletid,
            walletaddress=walletaddress,
        )

        return HttpResponseRedirect("dashboard")
    else:
        return HttpResponseRedirect("dashboard")

    #try:
        #initializing the server connection
    #    yag = yagmail.SMTP(user='ramon.dharmawan@prototype.global', password='Yes2021#')
        #sending the email
    #    contents = [
    #   "hello {}".format(username),
    #    "This is your pin code: {}, please save it somewhere save".format(pincode)
    #    ]
    #    yag.send(to='{}'.format(email), subject='Successfully Creating Wallet', contents)
    #    return render(request, 'api/deploy-nft-contract.html') 
    #except:
    #    print("Error, email was not sent")   
    #    return render(request, 'api/walletcreation.html') 




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
    'Authorization': 'Bearer {}'.format(token)
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


