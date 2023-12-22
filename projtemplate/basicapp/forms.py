from django import forms


class Currency_form(forms.Form):
    #list containing conversion currency names 
    currency_list=[('INR','INR'),('USD','USD'),('EUR','EUR'),('GBP','GBP')]

    base_currency=forms.ChoiceField(choices=currency_list,label='Base Currency')
    amount=forms.FloatField(label='amount')
    convert_currency=forms.ChoiceField(choices=currency_list,label='Convert Currency')


