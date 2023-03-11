import uuid
from typing import List

import pynecone as pc
from pydantic import BaseModel
from sqlmodel import JSON, Column, Field, String


def _get_id() -> str:
    return str(uuid.uuid4())


class SavedQuery(pc.Model, table=True):
    # comment(heumsi): '_' is added at end of var name, because of reserved name in library
    name_: str = Field(sa_column=Column("name", String(128)))
    description_: str = Field(sa_column=Column("description", String(256), default=""))
    labels: List[str] = Field(sa_column=Column(JSON))
    taints: List[str] = Field(sa_column=Column(JSON))
    id: str = Field(default_factory=_get_id, primary_key=True)


pc.Model.create_all()


class NodeDetail(BaseModel):
    name: str
    labels: List[str]
    taints: List[str]
