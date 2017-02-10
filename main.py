import googlemaps
from datetime import datetime
from config import Config


class Car(object):
    # In gallons
    tank_capacity = Config.Car.tank_capacity
    # MPG
    fuel_efficiency = Config.Car.fuel_efficiency

gmaps = googlemaps.Client(key=Config.api_key)