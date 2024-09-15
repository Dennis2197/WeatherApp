import geocoder
import requests
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from learning.models import Worldcities
from datetime import datetime


def get_temp(request):
    if request.method == "POST":
        city = get_user_input(request)
        try:
            loc = get_location(city)
            endpoint = "https://api.open-meteo.com/v1/forecast"
            template = loader.get_template("locationTemp.html")
            return api_request(request, loc, endpoint, template, city)
        except Worldcities.DoesNotExist:
            return HttpResponse("City does not exist")
    else:
        return HttpResponse("Method not allowed (We don't know what you are doing)")

def get_user_input(request):
    user_input = request.POST.get("textfield", None)
    if user_input:
        return user_input
    else: return HttpResponse("Please enter a city name")

def get_location(city):
    city = city
    city_data = Worldcities.objects.all().filter(city=city).first()
    locationlatlng = [city_data.lat, city_data.lng]
    return locationlatlng

def get_temp_here(request):
    endpoint = "https://api.open-meteo.com/v1/forecast"
    loc = geocoder.ip("me").latlng
    template = loader.get_template("index.html")
    return api_request(request, loc, endpoint, template, None)

def api_request(request, location, endpoint, template, city):
    api_request = f"{endpoint}?latitude={location[0]}&longitude={location[1]}&hourly=temperature_2m"
    now = datetime.now()
    hour = now.hour
    meteo_data = requests.get(api_request).json()
    temp = meteo_data['hourly']['temperature_2m'][hour]
    if city is not None:
        context = {"temp": temp, "city": city}
    else:
        context = {"temp": temp}
    return HttpResponse(template.render(context, request))
