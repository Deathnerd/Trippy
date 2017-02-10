import googlemaps
from googlemaps.convert import decode_polyline
from datetime import datetime
from config import Config
import json
from math import ceil
from pprint import pprint


class Car(object):
    # In gallons
    tank_capacity = Config.Car.tank_capacity
    # MPG
    fuel_efficiency = Config.Car.fuel_efficiency
    fill_level = 1


refill_level = Car.tank_capacity * .25

gmaps = googlemaps.Client(key=Config.api_key)

directions = gmaps.directions("105 Seth Way, Georgetown, KY, USA", "Los Angeles, CA, USA", transit_mode="driving",
                              departure_time=datetime.now())

if len(directions) == 0:
    print "Received nothing!"
    exit()

legs = directions[0]['legs']

print "Total distance from {beginning} to {end} is {distance} with {num_waypoints} waypoints inbetween".format(
    beginning=legs[0]["start_address"],
    end=legs[0]["end_address"],
    distance=legs[0]["distance"]["text"],
    num_waypoints=len(legs[0]["steps"]))


def meters_to_miles(meters):
    return round(meters * 0.00062137, 3)


def calculate_gas_used(distance, car):
    """
    :param distance:
     :type car: Car
    :param car:
    :return:
    """
    return round(distance / car.fuel_efficiency, 3)


waypoints = legs[0]["steps"]

gas_used_for_waypoints = []

for waypoint in waypoints:
    print "Waypoint: {}".format(waypoint)
    miles_for_leg = meters_to_miles(waypoint["distance"]["value"])
    gas_used = calculate_gas_used(miles_for_leg, Car)
    Car.fill_level = round(Car.fill_level - (gas_used / Car.tank_capacity), 3)
    print "{} miles, {} gallons ({} gallons left)".format(miles_for_leg, gas_used, Car.tank_capacity * Car.fill_level)
    gas_used_for_waypoints.append(gas_used)

sampling_size = 100
long_path = googlemaps.convert.decode_polyline(waypoints[6]["polyline"]["points"])

if len(long_path) > sampling_size:
    long_path = [long_path[int(ceil(i * float(len(long_path)) / sampling_size))] for i in range(sampling_size)]

print "Total gas used: {} gallons".format(sum(gas_used_for_waypoints))

# pprint()
road_fit = gmaps.snap_to_roads(long_path, interpolate=True)

pprint(road_fit)
