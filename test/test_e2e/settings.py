from pydantic.fields import Field
from pydantic_settings import BaseSettings


class UvicornURL(BaseSettings):
    host: str = Field("127.0.0.1", env="UVICORN_HOST")
    port: str = Field("8000", env="UVICORN_PORT")


class TestSettings(BaseSettings):
    url_settings: UvicornURL = UvicornURL()
