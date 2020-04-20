import requests
from django.shortcuts import render , redirect
from .models import City
from .forms import CityForm

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=271d1234d3f497eed5b1d80a07b3fcd1'
    err=''
    message=""
    message_class=""
    if request.method == 'POST':

        form = CityForm(request.POST)
        if form.is_valid():
            new_city=form.cleaned_data["name"]
            c = City.objects.filter(name=new_city).count()
            if c == 0:
                r = requests.get(url.format(new_city)).json()
                if r["cod"]==200:
                    form.save()
                else:
                    err="city does not exist in the world"
            else:
                err="city already exists"
        if err:
            message = err
            message_class = "is-danger"
        else:
            message = "city added succesfully"
            message_class = 'is-success'

    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:

        r = requests.get(url.format(city)).json()

        city_weather = {
            'city' : city.name,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }

        weather_data.append(city_weather)
    context = {'weather_data' : weather_data, 'form' : form, 'message': message,'message_class': message_class}
    return render(request, 'weather.html', context)



def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()

    return redirect('home')