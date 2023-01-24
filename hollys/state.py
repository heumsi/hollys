from typing import List

import pynecone as pc

from hollys import api, model


class BaseState(pc.State):
    ...


class SidebarState(BaseState):
    saved_querys: List[model.SavedQuery] = api.list_saved_query()

    def refresh_saved_querys(self) -> None:
        self.saved_querys = api.list_saved_query()


class QueryState(BaseState):
    label: str
    labels: List[str] = []
    taint: str
    taints: List[str] = []
    nodes: List[str] = api.get_nodes()
    is_loaded: bool = True

    def add_label(self):
        if not self.label:
            return
        self.labels += [self.label]

    def remove_label(self, label: str):
        self.labels = [_label for _label in self.labels if _label != label]
        # TODO(heumsi): This will be moved to page after following issue is resolved.
        # https://github.com/pynecone-io/pynecone/issues/319
        return [self.refresh_nodes]

    def add_taint(self):
        if not self.taint:
            return
        self.taints += [self.taint]

    def remove_taint(self, taint: str):
        self.taints = [_taint for _taint in self.taints if _taint != taint]
        # TODO(heumsi): This will be moved to page after following issue is resolved.
        # https://github.com/pynecone-io/pynecone/issues/319
        return [self.refresh_nodes]

    def reset(self):
        return [
            self.reset_label,
            self.reset_labels,
            self.reset_taint,
            self.reset_taints,
            self.refresh_nodes,
        ]

    def refresh_nodes(self) -> None:
        self.is_loaded = False
        self.nodes = api.get_nodes(self.labels, self.taints)
        self.is_loaded = True

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

    def set_by_model(self, saved_query):
        self.reset()
        self.id = saved_query["id"]
        self.name_ = saved_query["name_"]
        self.description_ = saved_query["description_"]
        self.labels = saved_query["labels"]
        self.taints = saved_query["taints"]
        return self.refresh_nodes

    def refresh_nodes(self) -> None:
        self.is_loaded = False
        self.nodes = api.get_nodes(self.labels, self.taints)
        self.is_loaded = True

    def delete(self):
        api.remove_saved_query(self.id)
        return [SidebarState.refresh_saved_querys, pc.redirect("/")]


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
            self.reset(),
            SidebarState.refresh_saved_querys,
        ]

    def reset(self) -> None:
        self.name = ""
        self.description = ""

    def toggle_show(self) -> None:
        self.show = not self.show
