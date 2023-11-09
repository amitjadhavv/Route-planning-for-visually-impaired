import requests


def request_get(url,parameters):

    response = requests.get(url,params=parameters)
    print(response.json())
    if response.status_code == 200:
        data = response.json()

    else:
        raise Exception("Error fetching data from API")

    return data