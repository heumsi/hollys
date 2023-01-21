from typing import List, Optional

import pynecone as pc
from kubernetes import client

from hollys.model import SavedFilter


def get_nodes(labels: Optional[List[str]] = None) -> List[str]:
    if not labels:
        labels = []
    v1_api = client.CoreV1Api()
    node_list = v1_api.list_node(label_selector=",".join(labels))
    return [node.metadata.name for node in node_list.items]


def list_saved_filter() -> List[SavedFilter]:
    with pc.session() as session:
        return session.query(SavedFilter).all()


def add_saved_filter(saved_filter: SavedFilter) -> None:
    with pc.session() as session:
        session.add(saved_filter)
        session.commit()


def remove_saved_filter(saved_filter_id: str) -> None:
    with pc.session() as session:
        saved_filter = session.get(SavedFilter, saved_filter_id)
        session.delete(saved_filter)
        session.commit()
