def walletcreation(request):
    token = getTokens(HttpResponse)

    tan = request.POST.get('username')

    print(tan)
    req = CustomerInfo.objects.filter(email=request.POST.get('email'))
    req1 = CustomerInfo.objects.filter(name=request.POST.get('username'))

    print(req)
    print(req1)


    if req is None:
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
            return HttpResponseRedirect("dashboard")
    elif req1 is not None:
        return HttpResponseRedirect("dashboard")
    else:
        try:
            asem = CustomerInfo.objects.get(email=request.POST.get('email'))
            print(asem)
        except:
            asem = CustomerInfo.objects.filter(email=request.POST.get('email')).values_list('secrettype', flat=True)
            for i in asem:
                if request.POST.get('secrettype') == i:
                    return redirect('dashboard')
                else:
                    desc = request.POST.get('desc')
                    username = request.POST.get('username')
                    email = request.POST.get('email')
                    secrettype = request.POST.get('secrettype')
                    wallettype = request.POST.get('wallettype')
                    pincode = request.POST.get('pincode')

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
            if asem.secrettype == request.POST.get('secrettype'):
                return redirect('dashboard')
            else:
                desc = request.POST.get('desc')
                username = request.POST.get('username')
                email = request.POST.get('email')
                secrettype = request.POST.get('secrettype')
                wallettype = request.POST.get('wallettype')
                pincode = request.POST.get('pincode')

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