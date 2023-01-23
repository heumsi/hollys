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
        pc.box(
            pc.link(pc.text("Query", font_size="1em"), href="/query"),
        ),
        pc.box(
            pc.text("Saved filters", font_size="xs", margin="0 0 1rem 0"),
            pc.foreach(
                State.list_saved_filter,
                lambda saved_filter: pc.box(
                    pc.link(
                        pc.text(
                            saved_filter.name_,
                            padding="0 0 0 1rem",
                            on_click=lambda: State.set_by_saved_filter(saved_filter),
                            font_size="1rem",
                        ),
                        href="/filters",
                    ),
                    padding="0.2rem 0",
                    color="#00000080",
                    _hover={
                        "color": "#000000",
                        "cursor": "pointer",
                    },
                ),
            ),
            padding_top="1rem",
        ),
        width="20%",
        min_width="240px",
        height="100%",
        padding="1rem 1rem 0 0",
        border_right=f"0.07rem solid {style.Color.border}",
    )


def saved_filter_content(State, ModalState):
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


def query_content(State, ModalState):
    return pc.box(
        pc.flex(
            pc.heading("Query", size="lg"),
            pc.spacer(),
            pc.text(
                "Save",
                font_size="sm",
                color=style.get_color("gray", 500),
                _hover={
                    "color": "#000000",
                    "cursor": "pointer",
                },
                on_click=lambda: ModalState.toggle_show(),
            ),
            margin="0 0 1rem 0",
            align_items="flex-end",
        ),
        pc.heading("Labels", size="md", padding="1rem 0"),
        pc.hstack(
            pc.input(value=State.label, on_change=State.set_label),
            pc.button(
                pc.icon(tag="AddIcon"),
                color_scheme="green",
                on_click=lambda: State.add_label(),
            ),
        ),
        pc.text(
            State.labels.length()
            + " items",  # comment(heumsi): It seems that f-string is not supported yet.
            margin_top="0.5rem",
            font_size="xs",
            color=style.get_color("gray", 500),
        ),
        pc.box(
            pc.foreach(
                State.labels,
                lambda label: pc.hstack(
                    pc.box(
                        pc.text(label),
                        width="fit-content",
                        margin="0.5rem",
                        margin_right="0rem",
                        padding="0.5rem",
                        display="inline-block",
                        bg=style.get_color("gray", 50),
                        font_size="sm",
                    ),
                    pc.icon(
                        tag="CloseIcon",
                        margin="0",
                        pading="0",
                        color=style.get_color("gray", 300),
                        font_size="0.5rem",
                        _hover={
                            "color": "#000000",
                            "cursor": "pointer",
                        },
                        on_click=lambda: State.remove_label(label),
                    ),
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
        pc.modal(
            pc.modal_overlay(
                pc.modal_content(
                    pc.modal_header("Save"),
                    pc.modal_body(
                        pc.vstack(
                            pc.form_control(
                                pc.form_label("Name"),
                                pc.input(
                                    placeholder="Name",
                                    value=ModalState.name,
                                    on_change=ModalState.set_name,
                                ),
                                pc.form_helper_text(
                                    "This value will appear in the saved filter list"
                                ),
                                is_required=True,
                            ),
                            pc.form_control(
                                pc.form_label("Description"),
                                pc.input(
                                    placeholder="Description",
                                    value=ModalState.description,
                                    on_change=ModalState.set_description,
                                ),
                                pc.form_helper_text(
                                    "Write it down so that others can understand it"
                                ),
                            ),
                            spacing="1rem",
                            align_items="flex-start",
                        ),
                    ),
                    pc.modal_footer(
                        pc.hstack(
                            pc.button(
                                "Done",
                                color_scheme="green",
                                on_click=ModalState.done,
                            ),
                            pc.button("Cancel", on_click=ModalState.cancel),
                        ),
                    ),
                )
            ),
            is_open=ModalState.show,
        ),
        width="80%",
        height="100%",
        padding="1rem",
    )


def body(sidebar, content):
    return pc.hstack(
        sidebar,
        content,
        width="100%",
        height="100%",
        padding_inline="5rem",
        align_itrems="flex-start",
        spacing="0",
        bg=style.Color.body_bg,
    )
