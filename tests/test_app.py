from typing import Optional

import pytest
from unittest.mock import Mock, patch

from app import get_client_ip
from schemas import GetIpInfoResponseBody, GetWeather, GetWeatherResponseBody


class MockRequest:
    environ: Optional[dict] = None
    remote_addr: Optional[str] = None

    def __init__(self, environ=None, remote_addr=None):
        self.environ = environ if environ else {}
        self.remote_addr = remote_addr


@pytest.mark.parametrize('mock_requests, result', [  # noqa
    (MockRequest({'HTTP_X_REAL_IP': '8.8.8.8'}), '8.8.8.8'),
    (MockRequest(remote_addr='5.5.5.5'), '5.5.5.5'),
])
def test_get_client_ip(mock_requests, result):
    test_result = get_client_ip(mock_requests)
    assert test_result == result


def test_get_weather(client):
    get_ip_info_response = GetIpInfoResponseBody(loc='43.6481, 51.1722', lat=43.6481, lon=51.1722)
    get_weather_info_response = GetWeatherResponseBody(
        weather=[GetWeather(id=801, main='Clouds', description='few clouds', icon='02d')])
    with patch(
            "utils.ipinfo.GetIpInfo.__call__",
            new_callable=lambda *args: Mock(return_value=get_ip_info_response)
    ):
        with patch(
                "utils.openweathermap.GetWeatherInfo.__call__",
                new_callable=lambda *args: Mock(return_value=get_weather_info_response)
        ):
            test_result = client.get('/')
            assert test_result.json == get_weather_info_response.dict()
