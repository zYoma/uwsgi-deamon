import urllib.parse
from functools import cached_property

from config import settings
from schemas import GetIpInfoResponseBody, GetWeatherQueryParams, GetWeatherResponseBody
from utils.client import BaseAPI


class GetWeatherInfo(BaseAPI):
    method = 'GET'
    url = 'data/2.5/weather'
    request_timeout = settings.OPENWATHERMAP_REQUEST_TIMEOUT
    query_params = GetWeatherQueryParams
    response = GetWeatherResponseBody
    BASE_URL = settings.OPENWATHERMAP_BASE_URL

    def __init__(self, coordinates: GetIpInfoResponseBody, appid: str = settings.OPENWATHERMAP_TOKEN):
        super().__init__(lat=coordinates.lat, lon=coordinates.lon, appid=appid)

    @cached_property
    def full_url(self) -> str:
        return urllib.parse.urljoin(self.BASE_URL, self.url)
