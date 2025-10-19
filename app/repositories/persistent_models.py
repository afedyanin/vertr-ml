import os
import psycopg2 as psycopg
import pandas as pd

from datetime import datetime, timezone
from uuid import UUID
from typing import Any
from dataclasses import dataclass
from sqlalchemy import create_engine
from app.configuration.config import PgSqlSettings

@dataclass
class PersistentModel:
    id: UUID
    time_utc: datetime
    version: int
    model_type: str
    file_name: str
    description: str
    content: bytes

    @staticmethod
    def from_dict(model: dict[str, Any]) -> "PersistentModel":
        return PersistentModel(
            id=model['id'],
            time_utc=model['time_utc'],
            version=model['version'],
            model_type=model['model_type'],
            file_name=model['file_name'],
            description=model['description'],
            content=model['content'])


# noinspection SqlNoDataSourceInspection
class PersistentModelsRepository:

    def __init__(self, config: PgSqlSettings):
        self._config = config
        self._models_table = "models"
        self._engine = create_engine(config.get_database_url())

    def get_models(self) -> pd.DataFrame:
        sql = f"SELECT id, time_utc, version, model_type, file_name, description FROM {self._models_table}"
        df = pd.read_sql_query(sql, self._engine)
        return df

    def get_last_version(self, file_name: str) -> int:
        with psycopg.connect(
                dbname=self._config.dbname,
                user=self._config.user,
                password=self._config.password,
                host=self._config.host,
                port=self._config.port) as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT version FROM {self._models_table} WHERE file_name = '{file_name}' "
                            f"ORDER BY version DESC LIMIT 1")
                row = cur.fetchone()
                if row is None:
                    return 0
                return row[0]

    def get_model_by_file_name(self, file_name: str) -> PersistentModel | None:
        with psycopg.connect(
                dbname=self._config.dbname,
                user=self._config.user,
                password=self._config.password,
                host=self._config.host,
                port=self._config.port) as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {self._models_table} WHERE file_name = '{file_name}' "
                            f"ORDER BY version DESC LIMIT 1")
                row = cur.fetchone()
                if row is None:
                    return None
                columns = list(cur.description)
                row_dict = {}
                for i, col in enumerate(columns):
                    row_dict[col.name] = row[i]
                return PersistentModel.from_dict(row_dict)

    def get_model_by_type(self, model_type: str) -> PersistentModel | None:
        with psycopg.connect(
                dbname=self._config.dbname,
                user=self._config.user,
                password=self._config.password,
                host=self._config.host,
                port=self._config.port) as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {self._models_table} WHERE model_type = '{model_type}' "
                            f"ORDER BY version DESC LIMIT 1")
                row = cur.fetchone()
                if row is None:
                    return None
                columns = list(cur.description)
                row_dict = {}
                for i, col in enumerate(columns):
                    row_dict[col.name] = row[i]
                return PersistentModel.from_dict(row_dict)

    def delete_model(self, model_id: UUID) -> None:
        with psycopg.connect(
                dbname=self._config.dbname,
                user=self._config.user,
                password=self._config.password,
                host=self._config.host,
                port=self._config.port) as conn:
            with conn.cursor() as cur:
                cur.execute(f"DELETE FROM {self._models_table} WHERE id = {model_id}")
                conn.commit()

    def insert_model(self, file_path: str, model_type: str, description: str | None) -> None:
        file_name = os.path.basename(file_path)
        last_version = self.get_last_version(file_name)
        next_version = last_version + 1

        model = PersistentModel(
            id=UUID(),
            time_utc=datetime.now(timezone.utc),
            version=next_version,
            model_type=model_type,
            file_name=file_name,
            description=description,
            content=self._convert_to_binary(file_path)
        )

        self._insert_model_internal(model)

    def _insert_model_internal(self, model: PersistentModel) -> None:
        with psycopg.connect(
                dbname=self._config.dbname,
                user=self._config.user,
                password=self._config.password,
                host=self._config.host,
                port=self._config.port) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"INSERT INTO {self._models_table} ("
                    "id, "
                    "time_utc, "
                    "version, "
                    "model_type, "
                    "file_name, "
                    "description, "
                    "content)"
                    "VALUES (%s, %s, %s, %s, %s, %s, %s) ",
                    (model.id,
                     model.time_utc,
                     model.version,
                     model.model_type,
                     model.file_name,
                     model.description,
                     psycopg.Binary(model.content)))
                conn.commit()

    @staticmethod
    def _convert_to_binary(file_path: str) -> bytes:
        with open(file_path, 'rb') as file:
            data = file.read()
        return data
