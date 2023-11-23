import json
import tools
from tools import walk_simulator
import xmltodict
from request import request_get


url = "http://localhost:8002/route"
data = {
    "locations": [{"lat": 49.595921, "lon": 11.002812}, {"lat": 49.596609, "lon": 11.007213}],
    "costing": "pedestrian",
    "directions_options": {"units": "miles"},
}

output = request_get(url,data)
output_json = json.dumps(output)
maneuvers = output['trip']['legs'][0]['maneuvers']
for m in maneuvers:
    print(m['instruction'])

gps_file_path = "2023-11-13_13_Nov_2023_11_58_22.gpx"


xml_result = open('2023-11-13_13_Nov_2023_11_58_22.gpx', 'r')
xml_dict = xmltodict.parse(xml_result.read())
route_track = xml_dict["gpx"]["trk"]["trkseg"]["trkpt"]
for t in walk_simulator(gps_file_path):
    print(t)
