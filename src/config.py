from pydantic import BaseModel
from pathlib import Path
from typing import Type
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    TomlConfigSettingsSource,
)

BASE_DIR = Path(__file__).parent.parent.parent
TOML_SETTINGS_PATH = BASE_DIR.joinpath("config.toml")

PathsSourcesDict: dict[Path, Type[PydanticBaseSettingsSource]] = {
    TOML_SETTINGS_PATH: TomlConfigSettingsSource,
}


class Database(BaseModel):
    postgres_username: str = "postgres"
    postgres_db: str = "postgres"
    postgres_port: int = 5432
    postgres_host: str = "localhost"
    postgres_password: str = "postgres"

    @property
    def async_database_url(self) -> str:
        return "postgresql+asyncpg://%s:%s@%s:%d/%s" % (
            self.postgres_username,
            self.postgres_password,
            self.postgres_host,
            self.postgres_port,
            self.postgres_db,
        )


class S3(BaseModel):
    aws_host: str = "localhost:9000"
    aws_access_key: str = ""
    aws_secret_access_key: str = ""
    aws_region: str | None = None
    aws_bucket: str = ""


class Config(BaseSettings):
    database: Database = Database()
    s3: S3 = S3()


cfg = Config()
