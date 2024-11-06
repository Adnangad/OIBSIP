"""Contains other functions necessary for running the app"""
import geopy
import geocoder
import pandas as pd
import timezonefinder as tz
import pytz
from datetime import datetime

def find_coordinates():
    gp = geocoder.ip('me')
    return gp.latlng if gp.latlng else None

def get_city(long, lat):
    """Retreives the city name based on long lat"""
    geolocator = geopy.Nominatim(user_agent="WeatherApp")
    location = geolocator.reverse(f"{lat}, {long}", timeout=10)
    adress = location.raw['address']
    city = adress.get('city', 'unkown')
    return city

def get_date_time(long, lat):
    """Gets the date and time based on long lat"""
    tf = tz.TimezoneFinder()
    timezone = tf.timezone_at(lng=long, lat=lat)
    date_time = {}
    if timezone:
        local_time = datetime.now(pytz.timezone(timezone))
        date_str = local_time.strftime("%Y-%m-%d")
        time_str = local_time.strftime("%H:%M")
        day = pd.Timestamp(date_str).day_name()
        month = pd.Timestamp(date_str).month_name()
        date_time['day'] = day
        date_time['month'] = month
        date_time['time'] = time_str
        return date_time

def get_coordinates_from_city(city_name):
    """retreives a citys longitude and latitude"""
    loc = geopy.Nominatim(user_agent="GetLoc")
    getLoc = loc.geocode(city_name, timeout=10)
    return [getLoc.latitude, getLoc.longitude]

def temp_converter(temp):
    """converts celcius to farenhiet"""
    temp = float(temp)
    rez = (temp * 9/5) + 32
    return round(rez, 2)