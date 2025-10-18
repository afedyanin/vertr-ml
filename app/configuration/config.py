from pydantic_settings import BaseSettings, SettingsConfigDict


class PgSqlSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='../.env',
        env_prefix="PG_",
        extra="ignore"
    )
    dbname: str = "postgres"
    host: str = "localhost"
    port: int = 5432
    user: str = "postgres"
    password: str = "password"

    def get_database_url(self):
        return f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}"


if __name__ == "__main__":

    db_settings = PgSqlSettings()
    print(db_settings.get_database_url())
    print(db_settings.model_dump())


