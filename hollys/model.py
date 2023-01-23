import uuid
from typing import List

import pynecone as pc
from sqlmodel import JSON, Column, Field, String


def _get_id() -> str:
    return str(uuid.uuid4())


class SavedFilter(pc.Model, table=True):
    # comment(heumsi): '_' is added at end of var name, because of reserved name in library
    name_: str = Field(sa_column=Column("name", String))
    description_: str = Field(sa_column=Column("description", String, default=""))
    labels: List[str] = Field(sa_column=Column(JSON))
    id: str = Field(default_factory=_get_id, primary_key=True)


pc.Model.create_all()
