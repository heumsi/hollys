import pynecone as pc
from kubernetes import config

from hollys.model import SavedFilter

# comment(heumsi): kube config needs to be loaded first before any other packages are imported.
try:
    config.load_kube_config()
except:
    config.load_incluster_config()


from hollys.state import ModalState, State


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
                            pc.hstack(
                                pc.text(
                                    saved_filter.name_,
                                    on_click=lambda: State.set_by_saved_filter(
                                        saved_filter
                                    ),
                                ),
                                pc.button(
                                    pc.icon(tag="CloseIcon"),
                                    color_scheme="red",
                                    on_click=lambda: State.remove_saved_filter(
                                        saved_filter.id
                                    ),
                                ),
                            )
                        ),
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
                            pc.button(
                                pc.icon(tag="AddIcon"),
                                color_scheme="green",
                                on_click=lambda: State.add_label(),
                            ),
                        ),
                        pc.hstack(
                            pc.foreach(
                                State.labels,
                                lambda label: pc.vstack(
                                    pc.hstack(
                                        pc.text(label),
                                        pc.button(
                                            pc.icon(tag="CloseIcon"),
                                            color_scheme="red",
                                            on_click=lambda: State.remove_label(label),
                                        ),
                                    )
                                ),
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
                    pc.foreach(State.nodes, lambda node: pc.vstack(pc.text(node))),
                    padding="2em",
                    width="100%",
                    background="white",
                ),
                pc.vstack(
                    pc.button(
                        "Save", color_scheme="blue", on_click=ModalState.toggle_show
                    ),
                    pc.modal(
                        pc.modal_overlay(
                            pc.modal_content(
                                pc.modal_header("Save"),
                                pc.input(
                                    placeholder="Name",
                                    value=ModalState.name,
                                    on_change=ModalState.set_name,
                                ),
                                pc.modal_footer(
                                    pc.button(
                                        "Done",
                                        color_scheme="green",
                                        on_click=ModalState.done,
                                    ),
                                    pc.button("Close", on_click=ModalState.cancel),
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
