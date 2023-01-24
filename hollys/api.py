from typing import List, Optional

import pynecone as pc
from kubernetes import client

from hollys import model


def get_nodes(
    labels: Optional[List[str]] = None, taints: Optional[List[str]] = None
) -> List[str]:
    if not labels:
        labels = []
    v1_api = client.CoreV1Api()
    v1_nodes = v1_api.list_node(label_selector=",".join(labels)).items
    if not taints:
        return [node.metadata.name for node in v1_nodes]
    else:
        nodes = []
        for node in v1_nodes:
            if not node.spec.taints:
                continue
            for taint in node.spec.taints:
                if taint.value:
                    str_ = f"{taint.key}={taint.value}:{taint.effect}"
                else:
                    str_ = f"{taint.key}:{taint.effect}"
                if str_ in taints:
                    nodes.append(node)
        return [node.metadata.name for node in nodes]


def list_saved_query() -> List[model.SavedQuery]:
    with pc.session() as session:
        return session.query(model.SavedQuery).all()


def add_saved_query(saved_query: model.SavedQuery) -> None:
    with pc.session() as session:
        session.add(saved_query)
        session.commit()


def remove_saved_query(saved_query_id: str) -> None:
    with pc.session() as session:
        saved_query = session.get(model.SavedQuery, saved_query_id)
        session.delete(saved_query)
        session.commit()
