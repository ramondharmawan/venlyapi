import requests, json

def getContractNft(lists):
    url = "https://api-business-staging.arkane.network/api/apps/3b613051-4e10-479d-a75a-ee355541e5a0/contracts"

    payload = json.dumps({
    "name": "{}".format(lists.contract_name),
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

    return HttpResponse(res)

