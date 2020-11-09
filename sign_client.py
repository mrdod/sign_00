import time
from multiprocessing.connection import Client
import csv
import json
from enum import Enum
from math import radians, cos, sin, asin, sqrt
from time import localtime, strftime


# Used to calculate distance between two points
def haversine(lon1, lat1, lon2, lat2):

    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r


# Used to send desired message to the server
def send_message(input_msg):
    address = ('localhost', 5000)
    conn = Client(address, authkey=b'1234')
    conn.send(input_msg)
    conn.send('close')


location_data = []

# Read location data from CSV file
with open('locations.csv', newline='') as csvfile:
    location_reader = csv.reader(csvfile, delimiter=',')
    next(location_reader)
    for row in location_reader:
        location_data.append({"latitude": row[0],
                              "longitude": row[1],
                              "heading": row[2],
                              "speed": row[3],
                              "DateTime": row[4]})

with open('stops.json') as jsoninput:
    stops_data = json.load(jsoninput)


class BusState(Enum):
    NEXT_STOP = 0
    IN_TRANSIT = 1
    ARRIVED_AT_STOP = 2
    LEAVING_STOP = 3


class TransitState(Enum):
    ROUTE_NAME = 0
    ROUTE_NAME_WAIT = 1
    CURRENT_TIME = 2
    CURRENT_TIME_WAIT = 3


time_counter = 0
bus_state = BusState.IN_TRANSIT
transit_state = TransitState.ROUTE_NAME
stop_number = 0

for time_counter in range(len(location_data)):
    x = 0

    # Check to see if bus is getting close to a stop
    if bus_state == BusState.IN_TRANSIT:

        # While in transit, alternate between route name and current Time
        if transit_state == TransitState.ROUTE_NAME:
            send_message("WOLFLINE 2")
            transit_state = TransitState.ROUTE_NAME_WAIT

        elif transit_state == TransitState.ROUTE_NAME_WAIT:
            transit_state = TransitState.CURRENT_TIME

        elif transit_state == TransitState.CURRENT_TIME:
            send_message(strftime("%H:%M:%S", localtime()))
            transit_state = TransitState.CURRENT_TIME_WAIT

        elif transit_state == TransitState.CURRENT_TIME_WAIT:
            transit_state = TransitState.ROUTE_NAME

        for x in range(len(stops_data.get("stops")) - 1):
            distance_from_stop = haversine(float(location_data[time_counter].get("latitude")),
                                           float(location_data[time_counter].get("longitude")),
                                           float(stops_data.get("stops")[x].get("lat")),
                                           float(stops_data.get("stops")[x].get("lon"))) * 1000

            if distance_from_stop < stops_data.get("stops")[x].get("radius"):
                bus_state = BusState.NEXT_STOP
                stop_number = x
                break
    # Bus has arrived at stop, pass message to server
    elif bus_state == BusState.NEXT_STOP:
        send_message("Next Stop:")
        bus_state = BusState.ARRIVED_AT_STOP
    # Display Stop Name
    elif bus_state == BusState.ARRIVED_AT_STOP:
        send_message(stops_data.get("stops")[stop_number].get("stop_name"))
        bus_state = BusState.LEAVING_STOP

    # Wait until bus has left stop to check for next stop
    elif bus_state == BusState.LEAVING_STOP:
        for x in range(len(stops_data.get("stops")) - 1):
            distance_from_stop = haversine(float(location_data[time_counter].get("latitude")),
                                           float(location_data[time_counter].get("longitude")),
                                           float(stops_data.get("stops")[x].get("lat")),
                                           float(stops_data.get("stops")[x].get("lon"))) * 1000

            if distance_from_stop >= stops_data.get("stops")[x].get("radius"):
                bus_state = BusState.IN_TRANSIT
                break

    time.sleep(1.0)
    # input("Enter your value: ")

