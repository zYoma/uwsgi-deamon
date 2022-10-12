from pydantic import BaseSettings


class Settings(BaseSettings):
    IP_INFO_BASE_URL: str = 'https://ipinfo.io'
    IP_INFO_REQUEST_TIMEOUT: int = 3
    IP_INFO_TOKEN: str

    OPENWATHERMAP_BASE_URL: str = 'https://api.openweathermap.org'
    OPENWATHERMAP_REQUEST_TIMEOUT: int = 3
    OPENWATHERMAP_TOKEN: str

    LOG_FILE_PATCH: str = 'app_log.log'

    class Config:
        env_file = ".env"


settings = Settings()
