import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class PgSqlSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='../.env',
        env_prefix="PG_",
        extra="ignore"
    )
    dbname: str
    host: str
    port: int
    user: str
    password: str

    def get_database_url(self):
        return f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}"


class TinvestSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='../.env',
        env_prefix="TINVEST_",
        extra="ignore"
    )
    token: str
    account_id: str


if __name__ == "__main__":

    tinvest_settings = TinvestSettings()
    print(tinvest_settings.model_dump())

    db_settings = PgSqlSettings()
    print(db_settings.model_dump())


