import uuid
from typing import List

import pynecone as pc
from sqlmodel import JSON, Column, Field


def _get_id() -> str:
    return str(uuid.uuid4())


class SavedFilter(pc.Model, table=True):
    name_: str  # comment(heumsi): 'name' cannot be used as var name, because when I used this, wrong value appeared.
    labels: List[str] = Field(sa_column=Column(JSON))
    id: str = Field(default_factory=_get_id, primary_key=True)
