from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# Resolves to: /Users/yeasin/Projects/AI_Customer_Support_Assistant
BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    database_url: str
    ollama_base_url: str

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        extra="ignore",
    )


settings = Settings()
