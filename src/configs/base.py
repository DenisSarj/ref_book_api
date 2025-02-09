import os
from logging import (
    INFO,
    WARNING,
    DEBUG
)

from pydantic import (
    Field,
    computed_field, PostgresDsn,
)
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

LOG_DEFAULT_FORMAT = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)


class BaseApplicationSettings(BaseSettings):
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    @computed_field
    @property
    def configs_dir(self) -> str:
        return os.path.join(self.base_dir, "configs")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class Database(BaseApplicationSettings):
    user: str
    password: str
    name: str
    host: str
    port: int
    echo: bool
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
    model_config = SettingsConfigDict(env_prefix="DB_")

    @computed_field
    @property
    def url(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            path=f"/{self.name}",
        )


class ApplicationSettings(BaseApplicationSettings):
    debug: bool = Field(default=False)
    app_host: str = Field(default="0.0.0.0")
    app_port: int = Field(default=8000)
    app_version: str = Field(default="0.1.0")
    app_docs_url: str = Field(default="/docs")

    log_level: int = INFO if debug else WARNING

    @computed_field
    @property
    def logs_dir(self) -> str:
        return os.path.join(os.path.dirname(self.base_dir), "logs")

    database: Database = Database()


settings = ApplicationSettings()
