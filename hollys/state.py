import tomllib
from typing import List

import pynecone as pc

from hollys import api, model


class BaseState(pc.State):
    ...


def get_version() -> str:
    version = tomllib.load(open("pyproject.toml", "rb"))["tool"]["poetry"]["version"]
    return version


class GlobalState(BaseState):
    version: str = get_version()

    def redirect(self, path: str):
        return pc.redirect(path)


class SidebarState(BaseState):
    saved_queries: List[model.SavedQuery] = []
    is_loaded: bool = False

    def init(self):
        self.is_loaded = False
        self.saved_queries = api.list_saved_query()
        self.is_loaded = True

    def refresh_saved_queries(self):
        self.saved_queries = api.list_saved_query()


class QueryState(BaseState):
    label: str
    labels: List[str] = []
    taint: str
    taints: List[str] = []
    nodes: List[str] = []
    is_loaded: bool = False

    def init(self):
        # comment(heumsi): these codes should be modified after following issue resolved.
        # https://github.com/pynecone-io/pynecone/issues/610
        self.is_loaded = False
        self.nodes = api.get_nodes(self.labels, self.taints)
        self.is_loaded = True

    def add_label(self):
        if not self.label:
            return
        self.labels += [self.label]

    def remove_label(self, label: str):
        self.labels = [_label for _label in self.labels if _label != label]

    def add_taint(self):
        if not self.taint:
            return
        self.taints += [self.taint]

    def remove_taint(self, taint: str):
        self.taints = [_taint for _taint in self.taints if _taint != taint]

    def refresh_nodes(self) -> None:
        self.nodes = api.get_nodes(self.labels, self.taints)

    def reset_label(self):
        self.label = ""

    def reset_labels(self):
        self.labels = []

    def reset_taint(self):
        self.taint = ""

    def reset_taints(self):
        self.taints = []


class SavedQueryState(BaseState):
    labels: List[str] = []
    taints: List[str] = []
    name_: str = ""
    description_: str = ""
    id: str = ""
    is_loaded: bool = False
    nodes: List[str] = []

    # comment(heumsi): Not used yet. but will be used after following issue is resolved.
    # https://github.com/pynecone-io/pynecone/issues/609
    # @pc.var
    # def saved_query_name(self):
    #     saved_query_name = self.get_query_params().get("name", "no saved query name")
    #     print(saved_query_name)
    #     return saved_query_name

    # comment(heumsi): Not used yet. but will be used after following issue is resolved.
    # https://github.com/pynecone-io/pynecone/issues/609
    # def init(self):
    #     saved_query = api.get_saved_query(self.saved_query_name)
    #     if not saved_query:
    #         ...  # TODO(heumsi): If saved query is None, Print 404 page.
    #     self.id = saved_query.id
    #     self.name_ = saved_query.name_
    #     self.description_ = saved_query.description_
    #     self.labels = saved_query.labels
    #     self.taints = saved_query.taints
    #     return self.refresh_nodes

    def set_by_model(self, saved_query: model.SavedQuery):
        self.id = saved_query["id"]
        self.name_ = saved_query["name_"]
        self.description_ = saved_query["description_"]
        self.labels = saved_query["labels"]
        self.taints = saved_query["taints"]

    def refresh_nodes(self) -> None:
        self.nodes = api.get_nodes(self.labels, self.taints)

    def delete(self):
        api.remove_saved_query(self.id)

    @pc.var
    def labels_empty(self) -> bool:
        return len(self.labels) == 0

    @pc.var
    def taints_empty(self) -> bool:
        return len(self.taints) == 0

    @pc.var
    def labels_as_kubectl(self) -> str:
        labels = []
        for label in self.labels:
            if "=" in label:
                labels.append(label)
            else:
                labels.append(f"{label}=''")
        labels_as_str = " \\\n".join(labels)
        return (
            """```
kubectl label nodes <your-node-name> \\\n"""
            + labels_as_str
        )

    @pc.var
    def taints_as_kubectl(self) -> str:
        taints_as_str = " \\\n".join(self.taints)
        return (
            """```
kubectl taint nodes <your-node-name> \\\n"""
            + taints_as_str
        )

    @pc.var
    def labels_as_node_affinity(self) -> str:
        expressions_as_str = ""
        for label in self.labels:
            if "=" in label:
                key, value = label.split("=")
                expression_as_str = f"""
        - key: {key}
          operator: "In"
          values:
          - {value} """
            else:
                key = label
                expression_as_str = f"""
        - key: {key}
          operator: "Exists" """
            expressions_as_str += expression_as_str
        return (
            """```
affinity:
  nodeAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      nodeSelectorTerms:
      - matchExpressions: """
            + expressions_as_str
        )

    @pc.var
    def taints_as_tolerations(self) -> str:
        tolerations_as_str = ""
        for taint in self.taints:
            if "=" in taint:
                key, value_with_effect = taint.split("=")
                value, effect = value_with_effect.split(":")
                toleration_as_str = f"""
- key: {key}
  operator: "Equal"
  values: {value}
  effect: {effect}"""
            else:
                key, effect = taint.split(":")
                toleration_as_str = f"""
- key: {key}
  operator: "Exists"
  effect: {effect}"""
            tolerations_as_str += toleration_as_str
        return (
            """```
tolerations: """
            + tolerations_as_str
        )


class SaveModalState(BaseState):
    show: bool = False
    name: str = ""
    description: str = ""

    def cancel(self):
        self.show = not self.show
        return self.reset()

    def done(self, labels: List[str], taints: List[str]):
        saved_query = model.SavedQuery(
            name_=self.name, description_=self.description, labels=labels, taints=taints
        )
        api.add_saved_query(saved_query)
        self.show = not self.show
        return [
            self.reset,
            SidebarState.set_is_loaded(False),
            SidebarState.refresh_saved_queries,
            SidebarState.set_is_loaded(True),
        ]

    def reset(self) -> None:
        self.name = ""
        self.description = ""

    def toggle_show(self) -> None:
        self.show = not self.show


class SnippetModalState(BaseState):
    show: bool = False

    def toggle_show(self) -> None:
        self.show = not self.show
