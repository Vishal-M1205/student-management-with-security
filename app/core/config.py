from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """Access the .env file using pydantic-settings"""

    database_host: str
    database_port: int
    database_name: str
    database_user: str
    database_password: str
    database_drivername: str
    app_name: str
    app_version: str
    jwt_secret_key: str
    jwt_algorithm: str
    jwt_expiration_minute: int

    model_config = SettingsConfigDict(env_file=".env")


config = Config()
