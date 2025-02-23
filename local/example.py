import requests
import config
import math

url = "https://openapi.emtmadrid.es/v1/mobilitylabs/user/login/"
email = config.EMAIL
password = config.PASSWORD


def _extract_token(response):
    """Extract the access token from the API response."""
    try:
        if response.get("code") != "01":
            print("Invalid email or password")
            return "Invalid token"
        return response["data"][0]["accessToken"]
    except (KeyError, IndexError) as e:
        raise ValueError("Unable to get token from the API") from e
    
def autenticate():
    headers = {
        "accept": "*/*",
        "email": email,
        "password": password
    }
    response = requests.get(url, headers=headers)
    return _extract_token(response.json())


token = autenticate()

print(token)


def getBusTime(token, stop_id, bus_id):
    urlBusTime = f"https://openapi.emtmadrid.es/v1/transport/busemtmad/stops/{stop_id}/arrives/{bus_id}/"
    headers = {
        "accessToken": token,

    }

    body = {
        "cultureInfo": "ES",
        "Text_StopRequired_YN": "Y",
        "Text_EstimationsRequired_YN": "Y",
        "Text_IncidencesRequired_YN": "N"
        }
    
    try:
        response = requests.post(urlBusTime, headers=headers, json=body)
    
        responseJson = response.json()

        next_bus = None
        next_bus2 = None
        error = None
        try:
            next_bus = math.floor(responseJson['data'][0]['Arrive'][0]['estimateArrive']/60)
        except:
            error = "Error al obtener el tiempo del bus"
        try:
            next_bus2 = math.floor(responseJson['data'][0]['Arrive'][1]['estimateArrive']/60)
        except:
            pass
    except:
        error = "Error al hacer la petición de la parada"
    return [next_bus, next_bus2, error]


print(getBusTime(token, "5727", "N3"))
print(getBusTime(token, "985", "28"))




