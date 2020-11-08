from multiprocessing.connection import Client
import csv
import json

location_data = []

# Read location data from CSV file
with open('locations.csv', newline='') as csvfile:
    location_reader = csv.reader(csvfile, delimiter=',')
    next(location_reader)
    for row in location_reader:
        location_data.append({"track_data_id": row[0],
                              "latitude": row[1],
                              "longitude": row[2],
                              "altitude": row[3],
                              "ground_speed (M/S)": row[4],
                              "heading": row[5],
                              "utc_time_stamp": row[6]})

with open('stops.json') as jsoninput:
    stops_data = json.load(jsoninput)





while True:
    val = input("Enter your value: ")

    address = ('localhost', 5000)
    conn = Client(address, authkey=b'1234')
    conn.send(val)
    conn.send('close')
