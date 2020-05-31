import pytest
import requests

from main import get_temperature


class MockResponse:
    def __init__(self, expected):
        self.__expected = expected

    def json(self):
        return {"currently": {"temperature": self.__expected}}


VALID_LOCATION_WEATHER = [
    (-14.235004, -51.92528, 62, 16),
    (-27.600526, -48.510145, 65.69, 18),
    (-3.731859, -38.529593, 83.1, 28),
    (-14.235004, -51.92528, 0, -17),
]


@pytest.mark.parametrize('lat, lng, temperature, expected', VALID_LOCATION_WEATHER)
def test_get_temperature_by_lat_lng(monkeypatch, lat, lng, temperature, expected):
    def mock_get(*args, **kwargs):
        return MockResponse(temperature)
    monkeypatch.setattr(requests, "get", mock_get)

    response = get_temperature(lat, lng)
    assert response == expected, f'Deveria ter retornado response({expected})'
