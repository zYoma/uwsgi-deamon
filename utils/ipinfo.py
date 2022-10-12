import urllib.parse
from functools import cached_property

from config import settings
from schemas import GetIpInfoResponseBody, IpInfoToken
from utils.client import BaseAPI


class GetIpInfo(BaseAPI):
    method = 'GET'
    request_timeout = settings.IP_INFO_REQUEST_TIMEOUT
    query_params = IpInfoToken
    response = GetIpInfoResponseBody
    BASE_URL = settings.IP_INFO_BASE_URL

    def __init__(self, ip: str, token: str = settings.IP_INFO_TOKEN):
        self.ip = ip
        super().__init__(ip=ip, token=token)

    @cached_property
    def full_url(self) -> str:
        return urllib.parse.urljoin(self.BASE_URL, self.ip)
