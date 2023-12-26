from django.shortcuts import render
from basicapp.forms import Currency_form,Bmi_form,Weather_form
import requests
import json
from sys import getsizeof
# Create your views here.

#--------------------home page--------------------

def index(request):
    return render(request,'basicapp/index.html')

#-----------------------BMI---------------------

def bmi(request):
    flag=False
    calculated_BMI=0
    category=''
    if(request.method=='GET'):
        bmi_form=Bmi_form(request.GET)
        
        if(bmi_form.is_valid()):
            weight=float(request.GET.get('weight'))
            height=float(request.GET.get('height'))/100
            flag=True
            calculated_BMI=weight/(height*height)
            if(calculated_BMI<18.5):
                category='Underweight:'
            elif(calculated_BMI>=18.5 and calculated_BMI<24.9):
                category='Normal weight:'
            elif(calculated_BMI>=25 and calculated_BMI<29.9):
                category='Overweight:'

            else:
                category='Obesity:'

        else:
            print(bmi_form.errors)

    else:
        bmi_form=Bmi_form()

    return render(request,'basicapp/BMIcalculator.html',{'BMI_form':bmi_form,'calculated_BMI':calculated_BMI,'flag':flag,'category':category})

#--------------------currency----------------------------

def currency(request):
    flag=False
    converted_value=''

    
    if(request.method=='GET'):

        #curr_form=Currency_form(base_currency=request.GET['base_currency'],convert_currency=request.GET['convert_currency'],amount=request.GET['amount'])
        curr_form=Currency_form(request.GET)
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
            #print('--------')
            conversion_rate=float(data_dict['conversion_rates'][conversion_to])
            #print(conversion_rate)
            amount=float(amount)

            converted_value=amount*conversion_rate

        else:
            print(curr_form.errors)

    else:
        curr_form=Currency_form()

    return render(request,'basicapp/currencyconverter.html',{'currency_form':curr_form,'converted_value':converted_value,'flag':flag})


#---------------------weather---------------------

def weather(request):
    flag=False
    Flag_lat_long='NOTFOUND'
    city=''
    country=''
    temp=''
    humidity=''
    wind_speed=''
    content={'Flag_lat_long':Flag_lat_long,'flag':flag,'weather_form':Weather_form() ,'city':city,'country':country,'temp':temp,'humidity':humidity,'wind_speed':wind_speed}
    if request.method == 'GET':

        weather_form=Weather_form(request.GET)

        if (weather_form.is_valid()):
        
            city=request.GET.get('city')
            state=request.GET.get('state')
            country=request.GET.get('country')

            #Step 1 get the lattitude and longitude based on city ,state ,country name
            #http://api.openweathermap.org/geo/1.0/direct?q={city name},{state code},{country code}&limit={limit}&appid={API key}
            first_url='http://api.openweathermap.org/geo/1.0/direct?q='
            q=city+','+state+','+country
            last_part='&limit=1&appid=3afe718612962238f9e5a65484413f37'
            joined_url=first_url+q+last_part
            response=requests.get(joined_url)
            if response.status_code==200:
                response_lat_long=response.json()
                #print('---------------',len(response_lat_long),'-------------------')
                if(len(response_lat_long)>0):
                    lat=str(response_lat_long[0]['lat'])
                    lon=str(response_lat_long[0]['lon'])
                    Flag_lat_long="FOUND"
                else:
                    Flag_lat_long="NOTFOUND"
                    return render(request,'basicapp/weather.html',context=content)
                
            # STEP 2 getting weather based on lattitude and longitude
            if(Flag_lat_long=='FOUND'):

                
                first_url_wed='https://api.openweathermap.org/data/2.5/weather?'
                get_wetlatlon='lat='+lat+'&'+'lon='+lon
                last_url_wed='&appid=3afe718612962238f9e5a65484413f37'
                joined_url=first_url_wed+get_wetlatlon+last_url_wed
                response=requests.get(joined_url)
                if(response.status_code==200):

                    response_res=response.json()
                    #result stored in varaiables
                    city=response_res['name']
                    country=response_res['sys']['country']
                    temp=response_res['main']['temp']-273.15
                    temp=round(temp,2)
                    humidity=response_res['main']['humidity']
                    wind_speed=response_res['wind']['speed']*3.6
                    
                    flag=True
                    content={'Flag_lat_long':Flag_lat_long,'flag':flag,'weather_form':weather_form ,'city':city,'country':country,'temp':temp,'humidity':humidity,'wind_speed':wind_speed}
        else:
            print(weather_form.errors)

    else:
        weather_form=Weather_form()
        
        


    return render(request,'basicapp/weather.html',context=content)
