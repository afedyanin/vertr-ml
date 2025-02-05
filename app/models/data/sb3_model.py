import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class Sb3Model:
    id: uuid
    time_utc: datetime
    file_name: str
    algo: str
    version: int
    description: str
    content: bytes

    @staticmethod
    def from_dict(model: dict[str, Any]) -> "Sb3Model":
        return Sb3Model(
            id=model['id'],
            time_utc=model['time_utc'],
            file_name=model['file_name'],
            algo=model['algo'],
            version=model['version'],
            description=model['description'],
            content=model['content'])
