from django.shortcuts import render,redirect
from django.http import HttpResponse
import requests, json
from . module.getToken import getTokens
from . module.getProfile import getprofile
from . module.getChain import getchain
from . module.getNftChain import getnftchain
from . module.getWalletClient import clientdata
import yagmail
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponseRedirect
from . models import CustomerInfo, ImageContractNft, TokenTypeNft
from django.core.files.storage import FileSystemStorage


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




def deploynft(request):
    if request.user.is_authenticated:
        current_user = request.user

        nftchain = getnftchain(HttpResponse)

        context = {
            "nftchainlist": nftchain,
        }

        return render(request, 'api/deploynft.html', context)
    else:
        return render(request, 'api/login.html')

    #token = getTokens(HttpResponse)

    #if request.method == 'POST':
    #    aplid = request.POST['applicationId']
    #   descnft = request.POST['descriptionNft']
    #    image = request.POST['imageUrl']
    #    chainNft = request.POST['chainNft']
    #    ownerNft = request.POST['walletaddress']

    #url = "https://api-business-staging.arkane.network/api/apps/dummy-applicationid-abc123/contracts"

    #payload = json.dumps({
    #"name": "Venly",
    #"description": "Example contract created using the VENLY NFT API",
    #"image": "https://gblobscdn.gitbook.com/spaces%2F-MB9NX0aClLh4Gx_kawF%2Favatar-1623151896040.png?alt=media",
    #"externalUrl": "https://venly.io",
    #"media": [
    #    {
    #    "type": "twitter",
    #    "value": "https://twitter.com/Venly_io"
    #    },
    #    {
    #    "type": "linkedin",
    #    "value": "https://www.linkedin.com/company/venly-io"
    #    }
    #],
    #"chain": "MATIC",
    #"owner": "0xF4Cc6E6c585d23585d5F08BDaEE9b85aB658fa95"
    #})
    #headers = {
    #'Content-Type': 'application/json',
    #'Authorization': 'Bearer {}'.format(token)
    #}

    #response = requests.request("POST", url, headers=headers, data=payload)

    #print(response.text)


def deploynftprocess(request):
    token = getTokens(HttpResponse)

    if request.method == 'POST':
        #ImageContractNft.objects.get(title = request.POST['deployname'])
        #return render (request,'api/deploynft.html', {'error':'Username is already taken!'})

        contract_name = request.POST['deployname']
        contract_desc = request.POST['deploydesc']
        appsid = request.POST['appid']
        chain_name = request.POST['deploychain']
        wallet_address = request.POST['deployaddress']
        site = request.POST['deploysite']
        twitter = request.POST['deploytwitter']
        linkedin = request.POST['deploylinkedin']
        #if request.FILES['upload']:
        uploads = request.FILES['upload']
        fss = FileSystemStorage()
        file = fss.save(uploads.name, uploads)
        file_url = fss.url(file)    
   

        ImageContractNft.objects.create(
            title = contract_name,
            image = uploads,
            chain = chain_name,
            wallet = wallet_address,
            site = site,
            twitter = twitter,
            linkedin = linkedin,
            desc = contract_desc,
            applicationId = appsid
        )

        les = ImageContractNft.objects.filter(title = request.POST['deployname'])
        for item in les:
            url_image = item.image
            print (url_image)

        try:
            url = "https://api-business-staging.arkane.network/api/apps/{}/contracts".format(appsid)

            payload = json.dumps({
            "name": "{}".format(contract_name),
            "description": "{}".format(contract_desc),
            "image": "{}".format(url_image),
            "externalUrl": "{}".format(site),
            "media": [
                {
                "type": "twitter",
                "value": "{}".format(twitter)
                },
                {
                "type": "linkedin",
                "value": "{}".format(linkedin)
                }
            ],
            "chain": "{}".format(chain_name),
            "owner": "{}".format(wallet_address)
            })

            headers = {
            'Content-Type': 'application/json',
            "Authorization": "Bearer {}".format(token)
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            res = response.json()

            print(res)

        except:
            #return render(request,'api/deploynft.html', {'error':'Something is wrong'})
            if res['status'] == '500':
                return HttpResponseRedirect('dashboard')
            else:
                return HttpResponseRedirect('')
        else:
            responsex = ImageContractNft.objects.all()
            customer = CustomerInfo.objects.all()

            for i in responsex:
                wallet_address = i.wallet
                contract_list_name = CustomerInfo.objects.get(walletaddress = wallet_address)

            print(contract_list_name)

            ImageContractNft.objects.filter(title = request.POST['deployname']).update(
                contracts_id = res['id'],
                hash = res['transactionHash'],
                symbol = res['symbol'],
                owner_name = str(contract_list_name)
            )  
            return HttpResponseRedirect('deploynft', {'file_url': file_url}) 
          
    return HttpResponseRedirect('deploynft')


def nftcontractlist(request):
    if request.user.is_authenticated:
        current_user = request.user

        response = ImageContractNft.objects.all()
        

        context = {
            'contractlist':response
        }


        return render(request, 'api/nftcontractlist.html', context)
    else:
        return render(request, 'api/login.html')


def createtokentype(request):
    if request.user.is_authenticated:
        current_user = request.user
        return render(request, 'api/createtokentype.html')
    else:
        return render(request, 'api/login.html')

def createtokentypeprocess(request):
    if request.user.is_authenticated:
        current_user = request.user

        token = getTokens(HttpResponse)

        if request.method == 'POST':
            token_name = request.POST['tokenname']
            token_contract_id = request.POST['tokencontractid']
            token_appsid = request.POST['tokenappid']
            external_url = request.POST['tokenexternalurl']
            background = request.POST['tokenbgcolor']
            att_type_token = request.POST['att-type-token']
            att_name_token = request.POST['att-name-token']
            att_value_token = request.POST['att-value-token']
            token_desc = request.POST['tokendesc']
            uploads = request.FILES['token-upload-img']
            fss = FileSystemStorage()
            file = fss.save(uploads.name, uploads)
            file1_url = fss.url(file)    

            TokenTypeNft.objects.create(
            name_token = token_name,
            token_image = uploads,
            contract_id_token = token_contract_id,
            appsid_token = token_appsid,
            site_url = external_url,
            token_type_att = att_type_token,
            token_name_att = att_name_token,
            token_value_att = att_value_token,
            token_description = token_desc,
            token_bg = background
            )

            print(background)
            print(att_type_token)

            les = TokenTypeNft.objects.filter(name_token = request.POST['tokenname'])
            for item in les:
                token_url_image = item.token_image
                print(token_url_image)

        try:
            url = "https://api-business-staging.arkane.network/api/apps/{}/contracts/{}/token-types".format(token_appsid,token_contract_id)

            payload = json.dumps({
            "name": "{}".format(token_name),
            "description": "{}".format(token_desc),
            "image": "{}".format(token_url_image),
            "backgroundColor": "{}".format(background),
            "externalUrl": "{}".format(external_url),
            "attributes": [
                {
                "type": "{}".format(att_type_token),
                "name": "{}".format(att_name_token),
                "value": "{}".format(att_value_token)
                },
            ]
            })
            headers = {
            'Content-Type': 'application/json',
            "Authorization": "Bearer {}".format(token)
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            resp = response.json()

            print(resp)

        except:
            #if resp['status'] == '500':
            print(resp)
            return HttpResponseRedirect('dashboard')
            #else:
            #    return HttpResponseRedirect('')
        else:
            responsed = TokenTypeNft.objects.all()

            owner_token_name = ImageContractNft.objects.get(contracts_id = token_contract_id)
            name_value = owner_token_name.owner_name
            print(name_value)

            TokenTypeNft.objects.filter(name_token = request.POST['tokenname']).update(
                token_type = resp['id'],
                token_hash = resp['transactionHash'],
                storage_url = resp['storage']['location'],
                type_storage = resp['storage']['type'],
                thumbnail_url = resp['imageThumbnail'],
                preview_url = resp['imagePreview'],
                supply = resp['currentSupply'],
                token_owner = name_value
                )
            return HttpResponseRedirect('createtokentype', {'file_url': file1_url}) 

    else:
        return render(request, 'api/login.html')
    
def tokentypelists(request):
    if request.user.is_authenticated:
        current_user = request.user

        responses = TokenTypeNft.objects.all()
        
        new_res = len(responses)
        print(new_res)

        context = {
            'tokentypelists':responses,
            'number':new_res
        }


        return render(request, 'api/tokentypelists.html',context)
    else:
        return render(request, 'api/login.html')
    