from uuid import UUID
from dataclasses import dataclass
from datetime import datetime
from typing import Any


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
