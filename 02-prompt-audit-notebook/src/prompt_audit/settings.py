# src/prompt_audit/settings.py
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # required
    openai_api_key: str = Field(
        ...,
        validation_alias="OPENAI_API_KEY",
        description="Secret API key from https://platform.openai.com/account/api-keys",
    )

    # optional overrides (read from .env or exported env vars)
    openai_model: str = Field(
        "gpt-4o-mini",
        validation_alias="OPENAI_MODEL",
        description="Default chat/completions model",
    )
    request_timeout: int = Field(
        30,
        validation_alias="OPENAI_REQUEST_TIMEOUT",
        description="HTTP timeout in seconds",
    )
    max_retries: int = Field(
        6,
        validation_alias="OPENAI_MAX_RETRIES",
        description="Tenacity retry limit",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
