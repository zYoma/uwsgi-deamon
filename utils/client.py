from typing import Optional, Type

import logging
import requests
from functools import cached_property
from pydantic import BaseModel


logger = logging.getLogger()


class BaseAPI:
    body: Optional[Type[BaseModel]] = None
    query_params: Optional[Type[BaseModel]] = None
    response: Optional[Type[BaseModel]] = None
    request_timeout: Optional[int] = None

    url: str
    method: str

    def __init__(self, **kwargs):
        if self.body:
            self.body = self.body.parse_obj(kwargs)

        if self.query_params:
            self.query_params = self.query_params.parse_obj(kwargs)

    @cached_property
    def headers(self) -> dict:
        return {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

    @cached_property
    def full_url(self) -> str:
        raise NotImplementedError

    @cached_property
    def json(self):
        if not self.body:
            return None

        return self.body.json(exclude_none=True, by_alias=True)

    @cached_property
    def params(self):
        if not self.query_params:
            return None

        return self.query_params.dict(exclude_none=True, by_alias=True)

    def __call__(self):
        return self.request()

    def request(self) -> Optional[BaseModel]:

        _request_kwargs = {
            'method': self.method,
            'url': self.full_url,
            'headers': self.headers,
            'data': self.json,
            'params': self.params,
            'timeout': self.request_timeout,
        }
        logger.info('Request %s %s', self.method, self.full_url, extra=_request_kwargs)
        with requests.Session() as s:
            resp = s.request(**_request_kwargs)

            logger.info('Finish request %s %s', self.method, self.full_url)
            if resp.status_code < 200 or resp.status_code >= 300:
                txt = resp.text
                _request_kwargs.update({
                    'status_code': resp.status_code,
                    'resp_headers': dict(resp.headers),
                    'content': txt
                })
                logger.error('Request fail %s %s', self.method, self.full_url, extra=_request_kwargs, stack_info=True)
                raise Exception(f'Request fail {self.__class__}', txt)

            if not self.response:
                return None

            txt = resp.text
            logger.debug('Response %s', txt)
            resp_obj = self.response.parse_raw(txt)

        return resp_obj
