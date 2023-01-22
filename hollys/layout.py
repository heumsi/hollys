import pynecone as pc

from hollys import style


def header():
    return pc.box(
        pc.heading("Hollys", size="lg"),
        width="100%",
        padding="1rem 5rem",
        bg=style.Color.navbar_bg,
        border_bottom=f"0.07rem solid {style.Color.border}",
    )


def sidebar(State):
    return pc.box(
        pc.heading("Saved filters", size="sm", margin="0 0 1rem 0"),
        pc.foreach(
            State.list_saved_filter,
            lambda saved_filter: pc.box(
                pc.hstack(
                    pc.text(
                        saved_filter.name_,
                        padding="0 0 0 1rem",
                        on_click=lambda: State.set_by_saved_filter(saved_filter),
                    ),
                    padding="0.2rem 0",
                    color="#00000080",
                    _hover={
                        "color": "#000000",
                        "cursor": "pointer",
                    },
                    font_size="0.8rem",
                )
            ),
        ),
        width="20%",
        min_width="240px",
        height="100%",
        padding="1rem 1rem 0 0",
        border_right=f"0.07rem solid {style.Color.border}",
    )


def content(State, ModalState):
    return pc.box(
        pc.flex(
            pc.heading(State.name_, size="lg"),
            pc.spacer(),
            pc.text(
                "Delete",
                font_size="sm",
                color=style.get_color("gray", 500),
                _hover={
                    "color": "#000000",
                    "cursor": "pointer",
                },
                on_click=lambda: State.remove_saved_filter(),
            ),
            margin="0 0 1rem 0",
            align_items="flex-end",
        ),
        pc.heading("Labels", size="md", padding="1rem 0"),
        pc.text(
            State.labels.length()
            + " items",  # comment(heumsi): It seems that f-string is not supported yet.
            margin_top="-0.5rem",
            font_size="xs",
            color=style.get_color("gray", 500),
        ),
        pc.box(
            pc.foreach(
                State.labels,
                lambda label: pc.box(
                    pc.text(label),
                    width="fit-content",
                    margin="0.5rem",
                    padding="0.5rem",
                    display="inline-block",
                    bg=style.get_color("gray", 50),
                    font_size="sm",
                ),
            ),
            min_height="50px",
            padding="1rem",
        ),
        pc.heading("Nodes", size="md", padding="1rem 0"),
        pc.text(
            State.nodes.length()
            + " items",  # comment(heumsi): It seems that f-string is not supported yet.
            margin_top="-0.5rem",
            font_size="xs",
            color=style.get_color("gray", 500),
        ),
        pc.box(
            pc.foreach(
                State.nodes,
                lambda node: pc.box(
                    pc.text(node),
                    width="fit-content",
                    margin="0.5rem",
                    padding="0.5rem",
                    display="inline-block",
                    bg=style.get_color("gray", 50),
                    font_size="sm",
                ),
            ),
            min_height="50px",
            padding="1rem",
        ),
        width="80%",
        height="100%",
        padding="1rem",
    )


def body(State, ModalState):
    return pc.hstack(
        sidebar(State),
        content(State, ModalState),
        width="100%",
        height="100%",
        padding_inline="5rem",
        align_itrems="flex-start",
        spacing="0",
        bg=style.Color.body_bg,
    )


def index(State, ModalState):
    return pc.vstack(
        header(),
        body(State, ModalState),
        spacing="0",
        width="100vw",
        height="100vh",
    )
