import requests
import json

def obtener_informacion_ubicacion(latitud, longitud):
    url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={latitud}&lon={longitud}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Error")
        return None

################################################################################

# Example
latitud = 40.2784
longitud = -3.9213

# Obtain info and present it in json format
info_ubicacion = obtener_informacion_ubicacion(latitud, longitud)
if info_ubicacion:
    print(json.dumps(info_ubicacion, indent=4))
