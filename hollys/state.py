from typing import List

import pynecone as pc

from hollys import api, model


class State(pc.State):
    labels: List[str] = []
    label: str = ""
    name_: str = "Default"
    nodes: List[str] = api.get_nodes()

    def add_label(self) -> None:
        if not self.label:
            return
        self.labels += [self.label]
        self.label = ""
        self.nodes = api.get_nodes(self.labels)

    def remove_label(self, label: str) -> None:
        self.labels = [_label for _label in self.labels if _label != label]
        self.nodes = api.get_nodes(self.labels)

    def set_by_saved_filter(self, saved_filter: model.SavedFilter) -> None:
        self.name_ = saved_filter["name_"]
        self.labels = saved_filter["labels"]
        self.nodes = api.get_nodes(self.labels)

    @pc.var
    def list_saved_filter(self) -> List[model.SavedFilter]:
        return api.list_saved_filter()

    def remove_saved_filter(self, saved_filter_id: str) -> None:
        api.remove_saved_filter(saved_filter_id)


class ModalState(State):
    show: bool = False
    name: str = ""
    saved_filters: List[model.SavedFilter] = [
        model.SavedFilter(name_="default", labels=[])
    ]

    def cancel(self) -> None:
        self.show = not self.show
        self.name = ""

    def done(self) -> None:
        saved_filter = model.SavedFilter(name_=self.name, labels=self.labels)
        api.add_saved_filter(saved_filter)
        self.show = not self.show
        self.name = ""

    def toggle_show(self) -> None:
        self.show = not self.show