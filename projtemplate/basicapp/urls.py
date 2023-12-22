from django.urls import path
from basicapp import views

app_name='basicapp'

urlpatterns = [
    path('bmi/',views.bmi,name='bmi'),
    path('weather/',views.weather,name='weather'),
    path('currency/',views.currency,name='currency'),
]