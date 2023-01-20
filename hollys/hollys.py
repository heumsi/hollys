from typing import List

import pynecone as pc


class State(pc.State):
    labels: List[str]
    label: str = ""
    taints: List[str]
    taint: str = ""

    def add_label(self) -> None:
        if not self.label:
            return
        self.labels += [self.label]
        self.label = ""

    def remove_label(self, label: str) -> None:
        self.labels = [_label for _label in self.labels if _label != label]


def index():
    return pc.center(
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
                pc.list(
                    pc.list_item("Node 1"),
                    pc.list_item("Node 2"),
                    pc.list_item("Node 3"),
                ),
                padding="2em",
                width="100%",
                background="white",
            ),
            width="70%",
            padding="2em",
        ),
        width="100%",
        height="100vh",
        background="radial-gradient(circle at 22% 11%,rgba(62, 180, 137,.20),hsla(0,0%,100%,0) 19%),radial-gradient(circle at 82% 25%,rgba(33,150,243,.18),hsla(0,0%,100%,0) 35%),radial-gradient(circle at 25% 61%,rgba(250, 128, 114, .28),hsla(0,0%,100%,0) 55%)",
    )


app = pc.App(state=State)
app.add_page(index)
app.compile()
