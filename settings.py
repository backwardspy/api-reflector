import logging
from typing import Any, Optional

from pydantic import BaseSettings, PostgresDsn, validator
from pydantic.validators import str_validator


class LogLevel(str):
    @classmethod
    def __modify_schema__(cls, field_schema: dict[str, Any]) -> None:
        field_schema.update(type="string", format="log_level")

    @classmethod
    def __get_validators__(cls):
        yield str_validator
        yield cls.validate

    @classmethod
    def validate(cls, value: str) -> str:
        v = value.upper()
        if v not in ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]:
            raise ValueError(f"{value} is not a valid LOG_LEVEL value")

        return getattr(logging, v)


class Settings(BaseSettings):
    @validator("azure_client_id", "azure_client_secret", "azure_tenant")
    def enabled_auth_settings(cls, v, values):
        if values["azure_auth_enabled"] and not v:
            raise ValueError("Azure auth details must be provided when auth is enabled")
        return v

    secret_key: str

    azure_auth_enabled: bool = False
    azure_client_id: Optional[str]
    azure_client_secret: Optional[str]
    azure_tenant: Optional[str]

    postgres_dsn: PostgresDsn

    log_json: bool = True
    log_level: LogLevel = "info"

    trace_query_descriptions: bool = False


settings = Settings()
