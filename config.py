import os


class Config(object):
    api_key = os.environ.get("GMAPS_API_KEY", "")

    class Car(object):
        tank_capacity = 11
        fuel_efficiency = 27.6