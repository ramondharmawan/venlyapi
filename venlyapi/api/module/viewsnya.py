from django.shortcuts import render
from django.http import HttpResponse
import requests


# Create your views here.



def index(request):
    context = {}
    return render(request, 'api/api-starter.html', context)
    #return HttpResponse("Hello, world. You're at the polls index.")



def submitggggg_test(request):
    if request.method == 'POST':
        urls = request.POST['url']
        #grant = request.POST.get('gtipe', False), ini namenya id html gytpe jadi salah gak mau pake yang grant di bawah
        grant = request.POST['gtipe'],
        clientId = request.POST['Cid'],
        clientSecret = request.POST['Csecret'],
    else:
        return render(request,'api/api-starter.html')

    
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''

    no_punct_grant = ""
    for char in grant:
        if char not in punctuations:
            no_punct_grant = no_punct_grant + char

    no_punct_clientId = ""
    for char in clientId:
        if char not in punctuations:
            no_punct_clientId = no_punct_clientId + char

    no_punct_clientSecret = ""
    for char in clientSecret:
        if char not in punctuations:
            no_punct_clientSecret = no_punct_clientSecret + char

    #url = "https://login-staging.arkane.network/auth/realms/Arkane/protocol/openid-connect/token"
    url = urls

    #payload='grant_type=client_credentials&client_id=Testaccount-capsule&client_secret=82c19251-1753-44f5-ae76-93438d3628de'
    payload='grant_type={}&client_id={}&client_secret={}'.format(no_punct_grant,no_punct_clientId,no_punct_clientSecret)
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
    }

    print(payload)
    print(no_punct_clientId)

    response = requests.request("POST", url, headers=headers, data=payload)

    #print(response.text)
    #return HttpResponse(response.text)

    #data = json.loads(response.text)

    #return HttpResponse(json.dumps(response.text))
    #return HttpResponse(data[:1])
    
    res = response.json()
    return HttpResponse(res["access_token"])

def uubg(request):
    context: {}
    return render(request, 'api/api-starter.html', context)
