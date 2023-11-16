import json
from request import request_get


url = "http://localhost:8002/route"
data = {
    "locations": [{"lat": 49.595921, "lon": 11.002812}, {"lat": 49.596609, "lon": 11.007213}],
    "costing": "auto",
    "directions_options": {"units": "miles"},
}

output = request_get(url,data)
print(output)