import requests


API_KEY = 'e1ee55658d4a2b28c4841e373c3b3d87'
BASE_URL = f'https://api.darksky.net/forecast/{API_KEY}/'


def get_temperature(lat, lng):
    '''
    Esta função realiza uma chamada para o serviço de previsão de
    tempo Dark Sky API.

    Attributes:
        lat(float): Representa a latitude da localização.
        lng(float): Representa a longitude da localização.
    '''
    url = f'{BASE_URL}/{lat}/{lng}'

    reponse = requests.get(url)
    data = reponse.json()
    temperature = data.get('currently').get('temperature')

    if temperature is None:
        return
    return int((temperature - 32) * 5.0 / 9.0)
