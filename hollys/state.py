from typing import List

import pynecone as pc

from hollys.function import add_saved_filter, get_nodes
from hollys.model import SavedFilter


class State(pc.State):
    labels: List[str] = []
    label: str = ""
    nodes: List[str] = get_nodes()

    def add_label(self) -> None:
        if not self.label:
            return
        self.labels += [self.label]
        self.label = ""
        self.nodes = get_nodes(self.labels)

    def remove_label(self, label: str) -> None:
        self.labels = [_label for _label in self.labels if _label != label]
        self.nodes = get_nodes(self.labels)

    def set_by_saved_filter(self, saved_filter: SavedFilter) -> None:
        self.labels = saved_filter["labels"]
        self.nodes = get_nodes(self.labels)

    @pc.var
    def list_saved_filter(self) -> List[SavedFilter]:
        with pc.session() as session:
            return session.query(SavedFilter).all()


class ModalState(State):
    show: bool = False
    name: str = ""
    saved_filters: List[SavedFilter] = [SavedFilter(name_="default", labels=[])]

    def cancel(self) -> None:
        self.show = not (self.show)
        self.name = ""

    def done(self) -> None:
        saved_filter = SavedFilter(name_=self.name, labels=self.labels)
        add_saved_filter(saved_filter)
        self.show = not (self.show)
        self.name = ""

    def toggle_show(self) -> None:
        self.show = not (self.show)
