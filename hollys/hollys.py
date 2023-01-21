from typing import List, Optional
import uuid

# from pydantic import BaseModel, Field
import pynecone as pc
from sqlmodel import Field, JSON, Column
from kubernetes import client, config


try:
    config.load_kube_config()
except:
    config.load_incluster_config()


def get_nodes(labels: Optional[List[str]] = None) -> List[str]:
    if not labels:
        labels = []
    v1_api = client.CoreV1Api()
    node_list = v1_api.list_node(label_selector=",".join(labels))
    return [node.metadata.name for node in node_list.items]

def get_id() -> str:
    return str(uuid.uuid4())



class SavedFilter(pc.Model, table=True):
    name_: str  # comment(heumsi): 'name' cannot be used as var name, because when I used this, wrong value appeared.
    labels: List[str] = Field(sa_column=Column(JSON))
    id: str = Field(default_factory=get_id, primary_key=True)

    # class Config:
    #     arbitrary_types_allowed = True


def add_saved_filter(saved_filter: SavedFilter) -> None:
    with pc.session() as session:
        session.add(saved_filter)
        session.commit()


class State(pc.State):
    labels: List[str] = []
    label: str = ""
    nodes: List[str] = get_nodes()
    # saved_filters: List[SavedFilter] = []

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

    # def list_saved_filter(self) -> List[SavedFilter]:
    #     with pc.session() as session:
    #         return session.query(SavedFilter).all()

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
        # self.saved_filters += [saved_filter]
        add_saved_filter(saved_filter)
        self.show = not (self.show)
        self.name = ""

    def toggle_show(self) -> None:
        self.show = not (self.show)



def index():
    return pc.center(
        pc.hstack(
            pc.vstack(
                pc.heading("Saved filters"),
                pc.divider(),
                pc.vstack(
                    pc.foreach(
                        State.list_saved_filter,
                        lambda saved_filter: pc.vstack(
                            pc.text(saved_filter.name_, on_click=lambda: State.set_by_saved_filter(saved_filter))
                        )
                    )
                ),
                padding="2em",
                width="30%",
                height="100%",
                background="white",
            ),
            pc.vstack(
                pc.vstack(
                    pc.heading("Filters"),
                    pc.divider(),
                    pc.vstack(
                        pc.heading("Labels", size="lg"),
                        pc.hstack(
                            pc.input(value=State.label, on_change=State.set_label),
                            pc.button(pc.icon(tag="AddIcon"), color_scheme="green", on_click=lambda: State.add_label()),
                        ),
                        pc.hstack(
                            pc.foreach(
                                State.labels,
                                lambda label: pc.vstack(
                                    pc.hstack(
                                        pc.text(label),
                                        pc.button(pc.icon(tag="CloseIcon"), color_scheme="red", on_click=lambda: State.remove_label(label)),
                                    )
                                )
                            )
                        ),
                    ),
                    padding="2em",
                    width="100%",
                    background="white",
                ),
                pc.vstack(
                    pc.heading("Nodes"),
                    pc.divider(),
                    pc.foreach(
                        State.nodes,
                        lambda node: pc.vstack(
                            pc.text(node)
                        )
                    ),
                    padding="2em",
                    width="100%",
                    background="white",
                ),
                pc.vstack(
                    pc.button("Save", color_scheme="blue", on_click=ModalState.toggle_show),
                    pc.modal(
                        pc.modal_overlay(
                            pc.modal_content(
                                pc.modal_header("Save"),
                                pc.input(placeholder="Name", value=ModalState.name, on_change=ModalState.set_name),
                                pc.modal_footer(
                                    pc.button(
                                        "Done", color_scheme="green", on_click=ModalState.done
                                    ),
                                    pc.button(
                                        "Close", on_click=ModalState.cancel
                                    )
                                ),
                            )
                        ),
                        is_open=ModalState.show,
                    ),
                ),
                width="70%",
                padding="2em",
            ),
            width="80%",
        ),
        width="100%",
        height="100vh",
        background="radial-gradient(circle at 22% 11%,rgba(62, 180, 137,.20),hsla(0,0%,100%,0) 19%),radial-gradient(circle at 82% 25%,rgba(33,150,243,.18),hsla(0,0%,100%,0) 35%),radial-gradient(circle at 25% 61%,rgba(250, 128, 114, .28),hsla(0,0%,100%,0) 55%)",
    )


app = pc.App(state=State)
app.add_page(index)
app.compile()
