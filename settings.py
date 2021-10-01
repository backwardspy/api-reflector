import logging
from typing import Any, Mapping, Optional

from pydantic import BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    secret_key: str

    azure_auth_enabled: bool = False
    azure_client_id: Optional[str]
    azure_client_secret: Optional[str]
    azure_tenant: Optional[str]
    use_x_forwarded_host: bool = False
    use_x_forwarded_proto: bool = False

    postgres_dsn: PostgresDsn

    log_json: bool = True
    log_level: str = "info"

    trace_query_descriptions: bool = False

    @validator("azure_client_id", "azure_client_secret", "azure_tenant")
    @classmethod
    def enabled_auth_settings(cls, v: Optional[str], values: Mapping[str, Any]) -> Optional[str]:
        if values["azure_auth_enabled"] and not v:
            raise ValueError("Azure auth details must be provided when auth is enabled")
        return v

    @validator("log_level")
    @classmethod
    def validate_log_level(cls, value: str) -> str:
        v = value.upper()

        if v not in logging._nameToLevel:
            raise ValueError(f'"{value}" is not a valid log_level value')

        return v


settings = Settings()
