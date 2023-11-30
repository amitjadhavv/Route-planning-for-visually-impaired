import xmltodict
from datetime import datetime
import time
from math import radians, sin, cos, sqrt, atan2
import re


def haversine(lat1, lon1, lat2, lon2):

    if lat1 is None or lon1 is None:
        lat1 = lat2
        lon1 = lon2

    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Radius of the Earth in kilometers (you can change it to miles if needed)
    R = 6371.0

    # Calculate the distance
    distance = R * c

    return distance



def walk_simulator(file_path):
    with open('2023-11-13_13_Nov_2023_11_58_22.gpx', 'r') as f:
        xml_dict = xmltodict.parse(f.read())
    route_track = xml_dict["gpx"]["trk"]["trkseg"]["trkpt"]
    previous_time = None
    current_time = None
    initialize_time = None
    for point in route_track:
        lat = float(point["@lat"])
        lon = float(point["@lon"])
        current_time = datetime.fromisoformat(point["time"][:-1])
        if previous_time is None: 
            previous_time = current_time
        if initialize_time is None:
            initialize_time = current_time
        sleep_time = current_time - previous_time
        # put thread to sleep to simulate walking on the pedestrian
        time.sleep(sleep_time.total_seconds())
        yield {'lat': lat, 'lon': lon, 'elapsed_time': (current_time-initialize_time).total_seconds()}
        previous_time = current_time


def extract_directions(text):
    pattern = re.compile(r'(right|left|You have arrived at your destination)', re.IGNORECASE)
    matches = pattern.findall(text)
    if not matches:
        return "go straight"
    elif matches[0].startswith("You"):
        return matches[0]
    else:
        return "turn " + matches[0]