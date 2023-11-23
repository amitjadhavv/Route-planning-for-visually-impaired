import xmltodict
from datetime import datetime
import time


def walk_simulator(file_path):
    with open('2023-11-13_13_Nov_2023_11_58_22.gpx', 'r') as f:
        xml_dict = xmltodict.parse(f.read())
    route_track = xml_dict["gpx"]["trk"]["trkseg"]["trkpt"]
    previous_time = None
    current_time = None
    intial_time = None
    for point in route_track:
        lat = point["@lat"]
        lon = point["@lon"]
        current_time = datetime.fromisoformat(point["time"][:-1])
        if previous_time is None:
            intial_time = current_time
            previous_time = current_time
        sleep_time = current_time - previous_time
        print(sleep_time.total_seconds())
        time.sleep(sleep_time.total_seconds())
         # put thread to sleep to simulate walking on the pedestrian
        previous_time = current_time
        yield [lat,lon,current_time.strftime("%Y-%m-%d %H:%M:%S")]
    print("total time elapsed:", current_time-intial_time)

