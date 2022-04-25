from django.shortcuts import render
from ..models import CustomerInfo
import json

def clientdata(request):
    query_results = CustomerInfo.objects.all()

    #cliente = query_results.json

    print(query_results)

    return query_results
