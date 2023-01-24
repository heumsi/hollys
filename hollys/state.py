from typing import List

import pynecone as pc

from hollys import api, model


class BaseState(pc.State):
    ...


class SidebarState(BaseState):
    saved_filters: List[model.SavedFilter] = api.list_saved_filter()

    def refresh_saved_filters(self) -> None:
        self.saved_filters = api.list_saved_filter()


class QueryState(BaseState):
    label: str
    labels: List[str] = []
    taint: str
    taints: List[str] = []
    nodes: List[str] = []
    is_loaded: bool = False

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.is_loaded = False
        self.nodes = api.get_nodes(self.labels, self.taints)
        self.is_loaded = True

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


class SavedFilterState(BaseState):
    labels: List[str] = []
    taints: List[str] = []
    name_: str = ""
    description_: str = ""
    id: str = ""
    is_loaded: bool = False
    nodes: List[str] = []

    def set_by_model(self, saved_filter):
        self.reset()
        self.id = saved_filter["id"]
        self.name_ = saved_filter["name_"]
        self.description_ = saved_filter["description_"]
        self.labels = saved_filter["labels"]
        self.taints = saved_filter["taints"]
        return self.refresh_nodes

    def refresh_nodes(self) -> None:
        self.is_loaded = False
        self.nodes = api.get_nodes(self.labels, self.taints)
        self.is_loaded = True

    def delete(self):
        api.remove_saved_filter(self.id)
        return [SidebarState.refresh_saved_filters, pc.redirect("/")]


class SaveModalState(BaseState):
    show: bool = False
    name: str = ""
    description: str = ""

    def cancel(self):
        self.show = not self.show
        return self.reset()

    def done(self, labels: List[str], taints: List[str]):
        saved_filter = model.SavedFilter(
            name_=self.name, description_=self.description, labels=labels, taints=taints
        )
        api.add_saved_filter(saved_filter)
        self.show = not self.show
        return [
            self.reset(),
            SidebarState.refresh_saved_filters,
        ]

    def reset(self) -> None:
        self.name = ""
        self.description = ""

    def toggle_show(self) -> None:
        self.show = not self.show
