from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpRequest
import requests, json
from . module.getToken import getTokens
from . module.getProfile import getprofile
from . module.getChain import getchain
from . module.getNftChain import getnftchain
from . module.getWalletClient import clientdata
import yagmail
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.http import HttpResponseRedirect
from . models import CustomerInfo, ImageContractNft, TokenTypeNft, FungibleToken, MintNft, Profile
from django.core.files.storage import FileSystemStorage
from time import sleep
from django.core.paginator import Paginator



# Create your views here.

def index(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'],password = request.POST['password'])
        if user is not None:
            auth.login(request,user)
            return redirect('dashboard', page=1)
        else:
            return render (request,'api/login.html', {'error':'Username or password is incorrect!'})
    else:
        return render(request,'api/login.html')
    #return HttpResponse("Hello, world. You're at the polls index.")

def signup(request):
    context = {}
    return render(request, 'api/create-user.html', context)

def dashboard(request,page):
    if request.user.is_authenticated:
        current_user = request.user

        token = getTokens(HttpResponse)
        profile = getprofile(HttpResponse)
        chain = getchain(HttpResponse)
        dataclient = clientdata(HttpResponse)

        print(dataclient)

        customer = CustomerInfo.objects.all()
        pp = Profile.objects.get(user=current_user)

        custpage = CustomerInfo.objects.all().order_by('name')
        paginator = Paginator(custpage, per_page=2)
        page_object = paginator.get_page(page)

        context = {
            'user': current_user,
            "user_id": profile["userId"],
            "nickname": profile["nickname"],
            "bearer":token,
            "chaintoken": chain,
            "datacust":dataclient,
            "custinfo":customer,
            'datapp': pp.profile_image,
            "page_obj": page_object,
            "pgt":paginator
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

        print(res)

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
        return HttpResponseRedirect("")

    #for i in req:
    #    details = CustomerInfo.objects.get(name=i.name)
    #    if details.email == request.POST.get('email'):    
    #        HttpResponseRedirect('dashboard',{'error':'the same user already has the blockchain'})
            

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

        pp = Profile.objects.get(user=current_user)

        context = {
            "nftchainlist": nftchain,
            'datapp': pp.profile_image
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
    #request = HttpRequest()

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
            if res is None:
                return HttpResponseRedirect('serverError')
            elif res['status'] == '500':
                return HttpResponseRedirect('dashboard', {'error': 'Server Error'})
            elif res['errorMessage'] == 'Transactional Execution Error':
                return HttpResponseRedirect('dashboard', {'error': 'Transactional Execution Error'})
            else:
                return HttpResponseRedirect('serverError')
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
            return HttpResponse(response)
            return HttpResponseRedirect('deploynft', {'file_url': file_url}) 
          
    return HttpResponseRedirect('deploynft')


def nftcontractlist(request):
    if request.user.is_authenticated:
        current_user = request.user

        response = ImageContractNft.objects.all()
        pp = Profile.objects.get(user=current_user)

        context = {
            'contractlist':response,
            'datapp': pp.profile_image
        }


        return render(request, 'api/nftcontractlist.html', context)
    else:
        return render(request, 'api/login.html')


def createtokentype(request):
    if request.user.is_authenticated:
        current_user = request.user

        pp = Profile.objects.get(user=current_user)

        context = {
            'datapp': pp.profile_image
        }

        return render(request, 'api/createtokentype.html', context)
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
            if res['status'] == '500':
                return HttpResponseRedirect('dashboard', {'error': 'Server Error'})
            elif res['errorMessage'] == 'Transactional Execution Error':
                return HttpResponseRedirect('dashboard', {'error': 'Transactional Execution Error'})
            else:
                return HttpResponseRedirect('serverError')
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

        pp = Profile.objects.get(user=current_user)

        context = {
            'tokentypelists':responses,
            'number':new_res,
            'datapp': pp.profile_image
        }


        return render(request, 'api/tokentypelists.html',context)
    else:
        return render(request, 'api/login.html')
    
def fungibletoken(request):
    if request.user.is_authenticated:
        current_user = request.user

        pp = Profile.objects.get(user=current_user)

        context = {
            'datapp': pp.profile_image
        }

        return render(request, 'api/fungibletoken.html', context)
    else:
        return HttpResponseRedirect('login')


def createfungible(request):
    if request.user.is_authenticated:
        current_user = request.user

        token = getTokens(HttpResponse)

        if request.method == 'POST':
            appsid = request.POST['applicationid']
            contractid = request.POST['contractnumber']
            tokenid = request.POST['tokennumber']
            dest = request.POST['destination']
            amounts = request.POST['qty']
            ownernft = request.POST['ownername']

        try:
            url = "https://api-business-staging.arkane.network/api/apps/{}/contracts/{}/tokens/fungible/{}".format(appsid,contractid,tokenid)

            payload = json.dumps({
            "destinations": [
                "{}".format(dest)
            ],
            "amounts": [
                amounts
            ]
            })
            headers = {
            'Content-Type': 'application/json',
            "Authorization": "Bearer {}".format(token)
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            res = response.json()

            print(res)

        except:
            if res['status'] == '500':
                return HttpResponseRedirect('dashboard', {'error': 'Server Error'})
            elif res['errorMessage'] == 'Transactional Execution Error':
                return HttpResponseRedirect('dashboard', {'error': 'Transactional Execution Error'})
            elif res['errorCode'] == 'fungible-minter-error':
                return HttpResponseRedirect('dashboard', {'error': 'Cannot mint fungible for non-fungible token type'})
            else:
                return HttpResponseRedirect('serverError')
        else:
            assettype = res['asset_contract']['media']['type']
            #owner = res['asset_contract']['address']

            print(assettype)

            FungibleToken.objects.create(
                application_id = appsid,
                contract_id = contractid,
                token_id = tokenid,
                destination = dest,
                supply = amounts,
                name = ownernft
            )

            return HttpResponseRedirect('fungibletokenlists')

def fungibletokenlists(request):
    if request.user.is_authenticated:
        current_user = request.user

        responseb = FungibleToken.objects.all()
        pp = Profile.objects.get(user=current_user)

        context = {
            'ftlists':responseb,
            'datapp': pp.profile_image
        }


        return render(request, 'api/fungibletokenlists.html', context)
    else:
        return HttpResponseRedirect('dashboard')
    

def mintnft(request):
    if request.user.is_authenticated:
        current_user = request.user

        pp = Profile.objects.get(user=current_user)

        context = {
            'datapp': pp.profile_image
        }

        return render(request, 'api/mintnft.html', context)
    else:
        return HttpResponseRedirect('login')

def processmintnft(request):
    if request.user.is_authenticated:
        current_user = request.user

        token = getTokens(HttpResponse)

        if request.method == 'POST':
            appsid = request.POST['applicationid']
            contractid = request.POST['contractnumber']
            tokenid = request.POST['tokennumber']
            dest = request.POST['destination']
            amounts = request.POST['qty']
            ownernft = request.POST['ownername']

        try:
            url = "https://api-business-staging.arkane.network/api/apps/{}/contracts/{}/types/{}/tokens".format(appsid,contractid,tokenid)

            payload = json.dumps({
            "destinations": [
                {
                "address": "{}".format(dest),
                "amount": amounts
                }
            ]
            })
            headers = {
            'Content-Type': 'application/json',
            "Authorization": "Bearer {}".format(token)
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            res = response.json()

            print(res)

        except:
            if res['status'] == '500':
                return HttpResponseRedirect('dashboard', {'error': 'Server Error'})
            elif res['errorMessage'] == 'Transactional Execution Error':
                return HttpResponseRedirect('dashboard', {'error': 'Transactional Execution Error'})
            elif res['errorCode'] == 'fungible-minter-error':
                return HttpResponseRedirect('dashboard', {'error': 'Cannot mint fungible for non-fungible token type'})
            else:
                return HttpResponseRedirect('serverError')
        else:
            #assettype = res['asset_contract']['media']['type']
            #print(assettype)

            MintNft.objects.create(
                application_id = appsid,
                contract_id = contractid,
                token_id = tokenid,
                destination = dest,
                supply = amounts,
                name = ownernft
            )

            return HttpResponseRedirect('mintnftlists')

def mintnftlists(request):
    if request.user.is_authenticated:
        current_user = request.user

        responseb = MintNft.objects.all()
        pp = Profile.objects.get(user=current_user)

        context = {
            'mintlists':responseb,
            'datapp': pp.profile_image
        }

        return render(request, 'api/mintnftlists.html', context)
    else:
        return HttpResponseRedirect('dashboard')


def instancemintnft(request):
    if request.user.is_authenticated:
        current_user = request.user

        token = getTokens(HttpResponse)

        nftchainx = getnftchain(HttpResponse)
        n = []
        for t in nftchainx:
            n.append(t)
            print(n)
        

        pp = Profile.objects.get(user=current_user)
        #clientdata = CustomerInfo.objects.all()
        clientdata = CustomerInfo.objects.filter(secrettype__in=n)
        print(clientdata)

        test = request.POST.get('clientname')
        print(test)
        
        if request.POST.get('clientname') == '' or request.POST.get('clientname') == '0':

            context = {
            'datapp': pp.profile_image,
            'client': clientdata,
            }

        elif request.POST.get('clientname') != '' or request.POST.get('clientname') != '0':

            nameclt = request.POST.get('clientname')
            print (nameclt)
            block = CustomerInfo.objects.filter(name=nameclt)
            appid = Profile.objects.get(id=1)
            
            context = {
            'datapp': pp.profile_image,
            'client': clientdata,
            'namer': nameclt,
            'chain': block,
            'aplid': appid.appsid
            }
        else:
           HttpResponseRedirect('login')
        return render(request, 'api/instancenftmint.html', context)

def instancemintnftprocs(request):
    if request.user.is_authenticated:
        current_user = request.user

        token = getTokens(HttpResponse)

        # start deploy contract
        if request.method == 'POST':
            contract_name = request.POST['deployname']
            contract_desc = request.POST['deploydesc']
            appsid = request.POST.get('appid')
            chain_name = request.POST['deploychain']
            wallet_address = request.POST['deployaddress']
            site = request.POST['deploysite']
            twitter = request.POST['deploytwitter']
            linkedin = request.POST['deploylinkedin']
            uploads = request.FILES['upload']
            fss = FileSystemStorage()
            file = fss.save(uploads.name, uploads)
            file_url = fss.url(file)   
        
            print(appsid)

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

            try:
                url = "https://api-business-staging.arkane.network/api/apps/3b613051-4e10-479d-a75a-ee355541e5a0/contracts"

                payload = json.dumps({
                "name": "{}".format(contract_name),
                "description": "{}".format(contract_desc),
                "image": "{}".format(file_url),
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

                rest = response.json()
                print(rest)
                sleep(30)

            except:
                if rest['status'] == '500':
                    return HttpResponseRedirect('dashboard', {'error': 'Server Error'})
                elif rest['errorMessage'] == 'Transactional Execution Error':
                    return HttpResponseRedirect('dashboard', {'error': 'Transactional Execution Error'})
                else:
                    return HttpResponseRedirect('serverError')
            else:
                responsex = ImageContractNft.objects.all()
                customer = CustomerInfo.objects.all()

                for i in responsex:
                    wallet_address = i.wallet
                    contract_list_name = CustomerInfo.objects.get(walletaddress = wallet_address)

                print(contract_list_name)

                ImageContractNft.objects.filter(title = request.POST['deployname']).update(
                    contracts_id = rest['id'],
                    hash = rest['transactionHash'],
                    symbol = rest['symbol'],
                    owner_name = str(contract_list_name)
                )  

                
                #return HttpResponseRedirect('deploynft', {'file_url': file_url}) 
                # end deploy contract

                # start deploy create token type

                if request.method == 'POST':
                    token_name = request.POST['tokenname']
                    token_contract_id = rest['id']
                    token_appsid = request.POST.get('appid')
                    external_url = request.POST['tokenexternalurl']
                    background = request.POST['tokenbgcolor']
                    att_type_token = request.POST['att-type-token']
                    att_name_token = request.POST['att-name-token']
                    att_value_token = request.POST['att-value-token']
                    token_desc = request.POST['tokendesc']
                    token_supply = request.POST['tokensupply']
                    burnable = request.POST['deployburnable']
                    token_type = request.POST['deploytypetoken']
                    uploads = request.FILES['token-upload-img']
                    fss = FileSystemStorage()
                    file = fss.save(uploads.name, uploads)
                    file1_url = fss.url(file)    
                    

                    TokenTypeNft.objects.create(
                    name_token = token_name,
                    token_image = file1_url,
                    contract_id_token = token_contract_id,
                    appsid_token = token_appsid,
                    site_url = external_url,
                    token_type_att = att_type_token,
                    token_name_att = att_name_token,
                    token_value_att = att_value_token,
                    token_description = token_desc,
                    token_bg = background
                    )

                try:
                    url = "https://api-business-staging.arkane.network/api/apps/{}/contracts/{}/token-types".format(token_appsid,token_contract_id)

                    payload = json.dumps({
                    "name": "{}".format(token_name),
                    "description": "{}".format(token_desc),
                    "image": "{}".format(file1_url),
                    "fungible" : token_type,
                    "maxSupply" : "{}".format(token_supply),
                    "burnable": burnable,
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
                    sleep(30)

                except:
                    if res['status'] == '500':
                        return HttpResponseRedirect('dashboard', {'error': 'Server Error'})
                    elif res['errorMessage'] == 'Transactional Execution Error':
                        return HttpResponseRedirect('dashboard', {'error': 'Transactional Execution Error'})
                    else:
                        return HttpResponseRedirect('serverError')    
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
                    # end deploy create token type
                    
                    # start fungible or non fungible token
                    if token_type == 'true':

                        token = getTokens(HttpResponse)

                        if request.method == 'POST':
                            appsid = request.POST.get('appid')
                            contractid = rest['id']
                            tokenid = resp['id']
                            dest = request.POST['destination']
                            amounts = request.POST['qty']
                            ownernft = request.POST['ownername']

                        try:
                            url = "https://api-business-staging.arkane.network/api/apps/{}/contracts/{}/tokens/fungible/{}".format(appsid,contractid,tokenid)

                            payload = json.dumps({
                            "destinations": [
                                "{}".format(dest)
                            ],
                            "amounts": [
                                amounts
                            ]
                            })
                            headers = {
                            'Content-Type': 'application/json',
                            "Authorization": "Bearer {}".format(token)
                            }

                            response = requests.request("POST", url, headers=headers, data=payload)

                            res = response.json()

                            print(res)
                            sleep(30)

                        except:
                            if res['status'] == '500':
                                return HttpResponseRedirect('dashboard', {'error': 'Server Error'})
                            elif res['errorMessage'] == 'Transactional Execution Error':
                                return HttpResponseRedirect('dashboard', {'error': 'Transactional Execution Error'})
                            elif res['errorCode'] == 'fungible-minter-error':
                                return HttpResponseRedirect('dashboard', {'error': 'Cannot mint fungible for non-fungible token type'})
                            else:
                                return HttpResponseRedirect('serverError')
                        else:
                            #assettype = res['asset_contract']['media']['type']
                            ##owner = res['asset_contract']['address']

                            #print(assettype)

                            FungibleToken.objects.create(
                                application_id = appsid,
                                contract_id = contractid,
                                token_id = tokenid,
                                destination = dest,
                                supply = amounts,
                                name = ownernft
                            )

                            return HttpResponseRedirect('fungibletokenlists')
                    else:
                        token = getTokens(HttpResponse)

                        if request.method == 'POST':
                            appsid = request.POST.get('appid')
                            contractid = rest['id']
                            tokenid = resp['id']
                            dest = request.POST['destination']
                            amounts = request.POST['qty']
                            ownernft = request.POST['ownername']

                        try:
                            url = "https://api-business-staging.arkane.network/api/apps/{}/contracts/{}/types/{}/tokens".format(appsid,contractid,tokenid)

                            payload = json.dumps({
                            "destinations": [
                                {
                                "address": "{}".format(dest),
                                "amount": amounts
                                }
                            ]
                            })
                            headers = {
                            'Content-Type': 'application/json',
                            "Authorization": "Bearer {}".format(token)
                            }

                            response = requests.request("POST", url, headers=headers, data=payload)

                            res = response.json()

                            print(res)
                            sleep(30)

                        except:
                            if res['status'] == '500':
                                return HttpResponseRedirect('dashboard', {'error': 'Server Error'})
                            elif res['errorMessage'] == 'Transactional Execution Error':
                                return HttpResponseRedirect('dashboard', {'error': 'Transactional Execution Error'})
                            elif res['errorCode'] == 'fungible-minter-error':
                                return HttpResponseRedirect('dashboard', {'error': 'Cannot mint fungible for non-fungible token type'})
                            else:
                                return HttpResponseRedirect('serverError')
                        else:
                            #assettype = res['asset_contract']['media']['type']
                            #print(assettype)

                            MintNft.objects.create(
                                application_id = appsid,
                                contract_id = contractid,
                                token_id = tokenid,
                                destination = dest,
                                supply = amounts,
                                name = ownernft
                            )

                            return HttpResponseRedirect('mintnftlists')


#### Error Handling ####
def error_404_view(request, exception):
    
    # we add the path to the the 404.html file
    # here. The name of our HTML file is 404.html
    return render(request, 'api/error-404.html')

def error_500_view(request, *args, **argv):
    
    # we add the path to the the 500.html file
    # here. The name of our HTML file is 500.html
    return render(request, 'api/error-500.html', status=500)

#### End Error Handling ####

def profile(request):
    if request.user.is_authenticated:
        current_user = request.user

        data = User.objects.filter(username = current_user)
        pp = Profile.objects.get(user=current_user)

        print(data)

        context = {
            'data1' : data, 
            'datapp': pp.profile_image
        }

        return render(request, 'api/getprofile.html', context)
    else:
        HttpResponseRedirect('login')
    


def updateprofile(request):
    if request.user.is_authenticated:
        current_user = request.user

        newname = request.POST.get('name')
        newemail = request.POST.get('email')

        usr = User.objects.get(username=current_user)
        print(usr.username)

        if usr.username == current_user:
            if usr.username == newname:
                messages.add_message(request, messages.INFO, "Your Username is Not Changed")
                return HttpResponseRedirect('profile')  
            elif usr.username == '':
                messages.add_message(request, messages.INFO, "Your Username is still the same")
                return HttpResponseRedirect('profile')  
            else:
                User.objects.filter(username=current_user).update(username = newname)
                messages.add_message(request, messages.INFO, "Your Username has been Changed")
                return HttpResponseRedirect('profile')

        else:
            if usr.email == newemail:
                messages.add_message(request, messages.INFO, "Your Email is Not Changed")
                return HttpResponseRedirect('profile')  
            elif usr.email == '':
                messages.add_message(request, messages.INFO, "Your Email is still the same")
                return HttpResponseRedirect('profile')  
            else:
                User.objects.filter(username=current_user).update(email = newemail)
                messages.add_message(request, messages.INFO, "Your Email has been Changed")
                return HttpResponseRedirect('profile')

    else:
        return HttpResponseRedirect('login')


def updatecredentials(request):
    if request.user.is_authenticated:
        current_user = request.user
        print(current_user)

        oldpasswd = request.POST.get('oldpass')
        newpasswd = request.POST.get('newpass')
        confirmpasswd = request.POST.get('confirmpass')
        print(confirmpasswd)

        usr = User.objects.get(email=current_user)

        if newpasswd == confirmpasswd:
            if usr.check_password(oldpasswd):           
                # Success Code
                usr.set_password(newpasswd)
                usr.save()
                return render(request,'api/getprofile.html', {'error':'Password is change successfully'})
            else:
                # Error Code
                return render(request,'api/getprofile.html', {'error':'Password is not correct'})
        else:
            return render(request,'api/getprofile.html', {'error':'new and confirm Password is not match'})
        return render(request, 'api/getprofile.html')
    else:
        return HttpResponseRedirect('login')


def changepp(request):
    if request.user.is_authenticated:
        current_user = request.user

        if request.POST.get('imagespp') == '':
            pp = Profile.objects.get(user=current_user)

            context = {
                'datapp': pp.profile_image
            }
            
            return render(request, 'api/changepp.html',context)

        elif request.method == 'POST':
            uploads = request.FILES['imagespp']
            print(uploads)
            fss = FileSystemStorage()
            file = fss.save(uploads.name, uploads)
            file2_url = fss.url(file)   
            print(file2_url)

            Profile.objects.filter(user=current_user).update(profile_image = file2_url)

            pp = Profile.objects.get(user=current_user)

            context = {
                'datapp': pp.profile_image
            }
            
            return render(request, 'api/changepp.html',context)

        else:
            pp = Profile.objects.get(user=current_user)

            context = {
                'datapp': pp.profile_image
            }
            
            return render(request, 'api/changepp.html',context)

def showresults(request, pk):
     if request.user.is_authenticated:
        current_user = request.user

        token = getTokens(HttpResponse)

        pp = Profile.objects.get(user=current_user)
        obj = CustomerInfo.objects.get(id=pk)

        wallet_id = obj.walletid

        url = "https://api-wallet-staging.venly.io/api/wallets/{}".format(wallet_id)

        payload={}
        headers = {
            'Content-Type': 'application/json',
            "Authorization": "Bearer {}".format(token)
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        resm = response.json()

        print(resm)

        context = {
                'datapp': pp.profile_image,
                'data': obj,
                'details': resm
            }

        return render(request, 'api/results.html', context)

def showresultcontract(request, pk):
     if request.user.is_authenticated:
        current_user = request.user

        token = getTokens(HttpResponse)

        pp = Profile.objects.get(user=current_user)
        obj = ImageContractNft.objects.get(id=pk)

        contractx_id = obj.contracts_id
        appsx_id = pp.appsid

        url = "https://api-business-staging.venly.io/api/apps/{}/contracts/{}".format(appsx_id,contractx_id)

        payload={}
        headers = {
            'Content-Type': 'application/json',
            "Authorization": "Bearer {}".format(token)
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        contract = response.json()

        print(contract)

        context = {
                'datapp': pp.profile_image,
                'data': obj,
                'details': contract
            }

        return render(request, 'api/result-contract.html', context)
        
def showresulttoken(request, pk):
     if request.user.is_authenticated:
        current_user = request.user

        token = getTokens(HttpResponse)

        pp = Profile.objects.get(user=current_user)
        obj = TokenTypeNft.objects.get(id=pk)

        contractx_id = obj.contract_id_token
        tokentype_id = obj.token_type
        appx_id = pp.appsid

        url = "https://api-business-staging.venly.io/api/apps/{}/contracts/{}/token-types/{}".format(appx_id,contractx_id,tokentype_id)

        payload={}
        headers = {
            'Content-Type': 'application/json',
            "Authorization": "Bearer {}".format(token)
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        contract = response.json()



        items1 = contract['animationUrls']
        items2 = contract['attributes']

        print(contract)

        context = {
                'datapp': pp.profile_image,
                'data': obj,
                'details': contract,
                'items_animate': items1,
                'items_atts': items2
        }

        return render(request, 'api/result-token.html', context)

        
def showresulttokenmetafungible(request, pk):
     if request.user.is_authenticated:
        current_user = request.user

        token = getTokens(HttpResponse)

        pp = Profile.objects.get(user=current_user)
        obj = FungibleToken.objects.get(id=pk)
        objx = TokenTypeNft.objects.get(contract_id_token = obj.contract_id) 

        contractx_id = obj.contract_id
        tokenx_id = obj.token_id
        appx_id = pp.appsid

        url = "https://api-business-staging.venly.io/api/apps/{}/contracts/{}/token-types/{}/metadata".format(appx_id,contractx_id,tokenx_id)

        payload={}
        headers = {
            'Content-Type': 'application/json',
            "Authorization": "Bearer {}".format(token)
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        contract = response.json()

        items1 = contract['animationUrls']
        items2 = contract['attributes']
        items3 = contract['properties']
        items4 = contract['contract']['media']
        items5 = contract['asset_contract']['media']


        print(contract)

        context = {
                'datapp': pp.profile_image,
                'data': obj,
                'data_name': objx.token_owner,
                'details': contract,
                'items_animate': items1,
                'items_atts': items2,
                'items_props': items3,
                'items_conme': items4,
                'items_asconme': items5
            }

        return render(request, 'api/result-token-metadata.html', context)


def showresulttokenmetanonfungible(request, pk):
     if request.user.is_authenticated:
        current_user = request.user

        token = getTokens(HttpResponse)

        pp = Profile.objects.get(user=current_user)
        obj = MintNft.objects.get(id=pk)
        objx = TokenTypeNft.objects.get(contract_id_token = obj.contract_id) 

        contractx_id = obj.contract_id
        tokenx_id = obj.token_id
        appx_id = pp.appsid

        url = "https://api-business-staging.venly.io/api/apps/{}/contracts/{}/token-types/{}/metadata".format(appx_id,contractx_id,tokenx_id)

        payload={}
        headers = {
            'Content-Type': 'application/json',
            "Authorization": "Bearer {}".format(token)
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        contract = response.json()

        items1 = contract['animationUrls']
        items2 = contract['attributes']
        items3 = contract['properties']
        items4 = contract['contract']['media']
        items5 = contract['asset_contract']['media']


        print(objx.token_owner)

        context = {
                'datapp': pp.profile_image,
                'data': obj,
                'data_name': objx.token_owner,
                'details': contract,
                'items_animate': items1,
                'items_atts': items2,
                'items_props': items3,
                'items_conme': items4,
                'items_asconme': items5
            }

        return render(request, 'api/result-token-metadata.html', context)


def serverError(request):
    return render(request,'api/error.html')