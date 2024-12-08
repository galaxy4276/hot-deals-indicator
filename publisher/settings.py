from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class AppSettings(BaseSettings):
    ELASTICSEARCH_HOST: List[str] = ["http://han-box.co.kr:9200"]
    ELASTICSEARCH_USERNAME: str = "elastic"
    ELASTICSEARCH_PASSWORD: str = "rhehdgur12"
    MONITORING_INTERVAL: int = 10
    MAX_RESULTS_PER_SEARCH: int = 15
    WEBSOCKET_TIMEOUT: int = 30

    class Config:
        model_config = SettingsConfigDict(env_file=".env")
