import pynecone as pc
from kubernetes import config

# comment(heumsi): kube config needs to be loaded first before any other packages are imported.
try:
    config.load_kube_config()
except:
    config.load_incluster_config()


from hollys import layout, state, style
from hollys.page import query, saved_filter


def index():
    pc.hstack(
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
                pc.button("Save", color_scheme="blue", on_click=ModalState.toggle_show),
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


app = pc.App(state=state.State)
app.add_page(query.index, path="/")
app.add_page(query.index, path="/query")
app.add_page(saved_filter.index, path="/filters")
app.compile()
