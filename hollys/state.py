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
    nodes: List[str] = api.get_nodes()

    def add_label(self) -> None:
        if not self.label:
            return
        self.labels += [self.label]
        # comment(heumsi): This will be deprecated after following issue is resolved
        # https://github.com/pynecone-io/pynecone/issues/319
        return self.refresh_nodes()

    def remove_label(self, label: str) -> None:
        self.labels = [_label for _label in self.labels if _label != label]
        # comment(heumsi): This will be deprecated after following issue is resolved
        # https://github.com/pynecone-io/pynecone/issues/319
        return self.refresh_nodes()

    def reset_label(self) -> None:
        self.label = ""

    def reset_labels(self) -> None:
        self.labels = []
        # comment(heumsi): This will be deprecated after following issue is resolved
        # https://github.com/pynecone-io/pynecone/issues/319
        return self.refresh_nodes()

    def reset(self):
        return [self.reset_label(), self.reset_labels(), self.refresh_nodes()]

    def refresh_nodes(self) -> None:
        self.nodes = api.get_nodes(self.labels)


class SavedFilterState(BaseState):
    labels: List[str] = []
    name_: str = ""
    description_: str = ""
    id: str = ""
    nodes: List[str] = api.get_nodes()

    def set_by_model(self, saved_filter) -> None:
        self.id = saved_filter["id"]
        self.name_ = saved_filter["name_"]
        self.description_ = saved_filter["description_"]
        self.labels = saved_filter["labels"]
        self.nodes = api.get_nodes(self.labels)

    def delete(self):
        api.remove_saved_filter(self.id)
        return [SidebarState.refresh_saved_filters(), pc.redirect("/")]


class SaveModalState(BaseState):
    show: bool = False
    name: str = ""
    description: str = ""

    def cancel(self):
        self.show = not self.show
        return self.reset()

    def done(self, labels: List[str]):
        saved_filter = model.SavedFilter(
            name_=self.name, description_=self.description, labels=labels
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
