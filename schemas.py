from typing import Optional

from pydantic import BaseModel, root_validator, validator


class GetIpInfoResponseBody(BaseModel):
    loc: str
    lat: Optional[float]
    lon: Optional[float]

    @validator('loc')
    def validate_lat(cls, value):
        try:
            lat, lon = value.split(',')
            return float(lat), float(lon)
        except Exception:
            raise ValueError('не верный тип координат')

    @root_validator
    def validate_coordinates(cls, values):
        lat, lon = values.get('loc')

        if not -90 <= lat <= 90:
            raise ValueError('широта указана не верно')
        if not -180 <= lon <= 180:
            raise ValueError('долгота указана не верно')

        values['lat'] = lat
        values['lon'] = lon

        return values


class IpInfoToken(BaseModel):
    token: str


class GetWeather(BaseModel):
    id: int
    main: str
    description: str
    icon: str


class GetWeatherResponseBody(BaseModel):
    weather: list[GetWeather]


class GetWeatherQueryParams(BaseModel):
    lat: float
    lon: float
    appid: str
