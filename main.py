import json
from tools import extract_directions
from tools import haversine
from tools import walk_simulator
from collections import deque
import xmltodict
from request import request_get

# "locations": [{"lat": 49.595921, "lon": 11.002812}, {"lat": 49.596609, "lon": 11.007213}],
url = "https://valhalla1.openstreetmap.de/route"
data = {
    "locations": [{"lat": 49.59586959, "lon": 11.00270821}, {"lat": 49.59662267, "lon": 11.0070331}],
    "costing": "pedestrian",
    "directions_options": {"units": "miles"},
}

output = request_get(url,data)
output_json = json.dumps(output)
maneuvers = output['trip']['legs'][0]['maneuvers']
total_length_valhalla = 0
valhalla_instruction_list = deque()
for maneuver in maneuvers:
    total_length_valhalla += maneuver["length"]
    valhalla_instruction_list.append({'length':maneuver['length'], 'instruction': maneuver['instruction']})

gps_file_path = "2023-11-13_13_Nov_2023_11_58_22.gpx"


xml_result = open('2023-11-13_13_Nov_2023_11_58_22.gpx', 'r')
xml_dict = xmltodict.parse(xml_result.read())
route_track = xml_dict["gpx"]["trk"]["trkseg"]["trkpt"]
previous_coordiante = {'lat': None, 'lon': None, 'current_time': None}
the_distance_you_have_walked = 0
valhalla_instruction = valhalla_instruction_list.popleft()
the_distance_you_got_to_turn = valhalla_instruction['length']
for current_coordiante in walk_simulator(gps_file_path):
    distance_between_two_location = haversine(previous_coordiante['lat'],
                                              previous_coordiante['lon'],
                                              current_coordiante['lat'],
                                              current_coordiante['lon'])
    the_distance_you_have_walked += distance_between_two_location
    if the_distance_you_have_walked > the_distance_you_got_to_turn:
        direction = extract_directions(valhalla_instruction["instruction"])
        print(f'instruction: {direction}  lat: {current_coordiante["lat"]}    '
              f'lon: {current_coordiante["lon"]}  elapsed time: {current_coordiante["elapsed_time"]}')
        if valhalla_instruction_list:
            valhalla_instruction = valhalla_instruction_list.popleft()
            the_distance_you_got_to_turn += valhalla_instruction['length']
        else:
            break
    previous_coordiante = current_coordiante
