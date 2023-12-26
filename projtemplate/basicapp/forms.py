from django import forms


class Currency_form(forms.Form):
    #list containing conversion currency names 
    currency_list=[('INR','INR'),('USD','USD'),('EUR','EUR'),('GBP','GBP')]

    base_currency=forms.ChoiceField(choices=currency_list,label='Base Currency',)
    convert_currency=forms.ChoiceField(choices=currency_list,label='Convert Currency')
    amount=forms.FloatField(label='amount')


class Bmi_form(forms.Form):
    weight=forms.FloatField(label='wight Kilogram')
    height=forms.FloatField(label='height in cm')


class Weather_form(forms.Form):
    city=forms.CharField()
    state=forms.CharField()
    country=forms.CharField()
