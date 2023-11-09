import json
import requests
from tools import request_get

request_URL = 'http://localhost:8002/route?'
json_str = '{"locations":[{"lat":42.358528,"lon":-83.271400,"street":"Appleton"},{"lat":42.996613,"lon":-78.749855,"street":"Ranch Trail"}],"costing":"auto","costing_options":{"auto":{"country_crossing_penalty":2000.0}},"units":"miles","id":"my_work_route"}'
# data = json.load(json_str)
kw = {'json': json_str}
response = request_get(request_URL,kw)










# # Set up Valhalla configuration
# config = valhalla.Client.configure(
#     'http://localhost:8002/route',  # Replace with the Valhalla service URL
#     profile='pedestrian'  # Use the walking profile
# )
#
# # Define start and end coordinates (latitude and longitude)
# start_point = (latitude_start, longitude_start)
# end_point = (latitude_end, longitude_end)
#
# # Request a route from Valhalla
# route = valhalla.Client.route(
#     config,
#     locations=[start_point, end_point],
#     costing='pedestrian',
#     directions_options={"units": "kilometers"},  # Optional: Set units for directions
# )
#
# # Check if the route was successfully generated
# if route.status_code == 200:
#     # Parse the route JSON response
#     route_data = route.json()
#
#     # Extract route geometry and instructions
#     geometry = route_data['trip']['legs'][0]['shape']
#     instructions = route_data['trip']['legs'][0]['maneuvers']
#
#     # You can use a mapping library (e.g., Folium) to display the route on a map.
#     # Here's a simple example using Folium:
#     import folium
#
#     m = folium.Map(location=start_point, zoom_start=15)
#     folium.PolyLine(geometry, color='blue').add_to(m)
#
#     for instruction in instructions:
#         folium.Marker(
#             location=instruction['begin_location'],
#             icon=folium.DivIcon(html=f"<div>{instruction['instruction']}</div>")
#         ).add_to(m)
#
#     m.save('walking_route.html')
# else:
#     print(f"Failed to generate route. Status code: {route.status_code}")
