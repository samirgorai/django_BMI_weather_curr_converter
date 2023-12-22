from django.shortcuts import render
from basicapp.forms import Currency_form
import requests
import json
# Create your views here.

def index(request):
    return render(request,'basicapp/index.html')

def bmi(request):
    
    return render(request,'basicapp/BMIcalculator.html')

def currency(request):
    flag=False
    converted_value=''

    
    if(request.method=='GET'):
        print('------------------')
        print(request.GET.get('base_currency'))
        print(request.GET.get('convert_currency'))
        print(request.GET.get('amount'))
        print('------------------')
        #curr_form=Currency_form(base_currency=request.GET['base_currency'],convert_currency=request.GET['convert_currency'],amount=request.GET['amount'])
        curr_form=Currency_form(request.GET)
        print(curr_form)
        #api
        
        if(curr_form.is_valid()):
            #print(curr_form.base_currency)
            base_url='https://v6.exchangerate-api.com/v6/efc3b7a750f182ad4b079971/latest/'
            conversion_from=request.GET.get('base_currency')
            conversion_to=request.GET.get('convert_currency')
            amount=request.GET.get('amount')

            url=base_url + conversion_from    
            flag=True
            data=requests.get(url=url)
            data_dict=json.loads(data.text)
            print('--------')
            conversion_rate=float(data_dict['conversion_rates'][conversion_to])
            print(conversion_rate)
            amount=float(amount)

            converted_value=amount*conversion_rate

        else:
            print(curr_form.errors)

    else:
        curr_form=Currency_form()

    return render(request,'basicapp/currencyconverter.html',{'currency_form':curr_form,'converted_value':converted_value,'flag':flag})




def weather(request):
    return render(request,'basicapp/weather.html')
