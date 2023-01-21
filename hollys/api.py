from typing import List, Optional

import pynecone as pc
from kubernetes import client

from hollys import model


def get_nodes(labels: Optional[List[str]] = None) -> List[str]:
    if not labels:
        labels = []
    v1_api = client.CoreV1Api()
    node_list = v1_api.list_node(label_selector=",".join(labels))
    return [node.metadata.name for node in node_list.items]


def list_saved_filter() -> List[model.SavedFilter]:
    with pc.session() as session:
        return session.query(model.SavedFilter).all()


def add_saved_filter(saved_filter: model.SavedFilter) -> None:
    with pc.session() as session:
        session.add(saved_filter)
        session.commit()


def remove_saved_filter(saved_filter_id: str) -> None:
    with pc.session() as session:
        saved_filter = session.get(model.SavedFilter, saved_filter_id)
        session.delete(saved_filter)
        session.commit()
