import os
import uuid
from datetime import datetime, timezone

import psycopg
import pandas as pd
from sqlalchemy import create_engine

from app.configuration.config import PgSqlSettings
from app.models.data.sb3_model import Sb3Model


class Sb3ModelsRepository:

    def __init__(self, config: PgSqlSettings):
        self._config = config
        self._models_table = "sb3_models"
        self._engine = create_engine(config.get_database_url())

    def get_models(self) -> pd.DataFrame:
        sql = f"SELECT id, time_utc, file_name, algo, version, description FROM {self._models_table}"
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

    def get_model_by_file_name(self, file_name: str) -> Sb3Model | None:
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
                return Sb3Model.from_dict(row_dict)

    def delete_model(self, model_id: uuid) -> None:
        with psycopg.connect(
                dbname=self._config.dbname,
                user=self._config.user,
                password=self._config.password,
                host=self._config.host,
                port=self._config.port) as conn:
            with conn.cursor() as cur:
                cur.execute(f"DELETE FROM {self._models_table} WHERE id = {model_id}")
                conn.commit()

    def insert_model(self, file_path: str, algo: str, description: str | None) -> None:
        file_name = os.path.basename(file_path)
        last_version = self.get_last_version(file_name)
        next_version = last_version + 1

        model = Sb3Model(
            id=uuid.uuid4(),
            time_utc=datetime.now(timezone.utc),
            file_name=file_name,
            algo=algo,
            version=next_version,
            description=description,
            content=self._convert_to_binary(file_path)
        )

        self._insert_model_internal(model)

    def _insert_model_internal(self, model: Sb3Model) -> None:
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
                    "file_name, "
                    "algo, "
                    "version, "
                    "description, "
                    "content)"
                    "VALUES (%s, %s, %s, %s, %s, %s, %s) ",
                    (model.id,
                     model.time_utc,
                     model.file_name,
                     model.algo,
                     model.version,
                     model.description,
                     psycopg.Binary(model.content)))
                conn.commit()

    @staticmethod
    def _convert_to_binary(file_path: str) -> bytes:
        with open(file_path, 'rb') as file:
            data = file.read()
        return data
