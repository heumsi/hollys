import pynecone as pc

from hollys.layout import page
from hollys.state import QueryState, SaveModalState
from hollys.style import get_color


def content():
    return pc.box(
        pc.flex(
            pc.heading("Query", size="lg"),
            pc.spacer(),
            pc.hstack(
                pc.text(
                    "Reset",
                    font_size="sm",
                    color=get_color("gray", 500),
                    _hover={
                        "color": "#000000",
                        "cursor": "pointer",
                    },
                    on_click=lambda: QueryState.reset(),
                ),
                pc.text(
                    "Save",
                    font_size="sm",
                    color=get_color("gray", 500),
                    _hover={
                        "color": "#000000",
                        "cursor": "pointer",
                    },
                    on_click=lambda: SaveModalState.toggle_show(),
                ),
                spacing="1rem",
            ),
            margin="0 0 1rem 0",
            align_items="flex-end",
        ),
        pc.heading("Labels", size="md", padding="1rem 0"),
        pc.hstack(
            pc.input(value=QueryState.label, on_change=QueryState.set_label),
            pc.button(
                pc.icon(tag="AddIcon"),
                color_scheme="green",
                on_click=[
                    QueryState.add_label,
                    QueryState.reset_label,
                    QueryState.refresh_nodes,
                ],
            ),
        ),
        pc.text(
            # comment(heumsi): It seems that f-string is not supported yet.
            QueryState.labels.length() + " items",
            margin_top="0.5rem",
            font_size="xs",
            color=get_color("gray", 500),
        ),
        pc.box(
            pc.foreach(
                QueryState.labels,
                lambda label: pc.hstack(
                    pc.box(
                        pc.text(label),
                        width="fit-content",
                        margin="0.5rem",
                        margin_right="0rem",
                        padding="0.5rem",
                        display="inline-block",
                        bg=get_color("gray", 50),
                        font_size="sm",
                    ),
                    pc.icon(
                        tag="CloseIcon",
                        margin="0",
                        pading="0",
                        color=get_color("gray", 300),
                        font_size="0.5rem",
                        _hover={
                            "color": "#000000",
                            "cursor": "pointer",
                        },
                        on_click=lambda: QueryState.remove_label(label),
                    ),
                ),
            ),
            min_height="50px",
            padding="1rem",
        ),
        pc.heading("Taints", size="md", padding="1rem 0"),
        pc.hstack(
            pc.input(value=QueryState.taint, on_change=QueryState.set_taint),
            pc.button(
                pc.icon(tag="AddIcon"),
                color_scheme="green",
                on_click=[
                    QueryState.add_taint,
                    QueryState.reset_taint,
                    QueryState.refresh_nodes,
                ],
            ),
        ),
        pc.text(
            # comment(heumsi): It seems that f-string is not supported yet.
            QueryState.taints.length() + " items",
            margin_top="0.5rem",
            font_size="xs",
            color=get_color("gray", 500),
        ),
        pc.box(
            pc.foreach(
                QueryState.taints,
                lambda taint: pc.hstack(
                    pc.box(
                        pc.text(taint),
                        width="fit-content",
                        margin="0.5rem",
                        margin_right="0rem",
                        padding="0.5rem",
                        display="inline-block",
                        bg=get_color("gray", 50),
                        font_size="sm",
                    ),
                    pc.icon(
                        tag="CloseIcon",
                        margin="0",
                        pading="0",
                        color=get_color("gray", 300),
                        font_size="0.5rem",
                        _hover={
                            "color": "#000000",
                            "cursor": "pointer",
                        },
                        on_click=lambda: QueryState.remove_taint(taint),
                    ),
                ),
            ),
            min_height="50px",
            padding="1rem",
        ),
        pc.heading("Nodes", size="md", padding="1rem 0"),
        pc.text(
            QueryState.nodes.length()
            + " items",  # comment(heumsi): It seems that f-string is not supported yet.
            margin_top="-0.5rem",
            font_size="xs",
            color=get_color("gray", 500),
        ),
        pc.box(
            pc.foreach(
                QueryState.nodes,
                lambda node: pc.box(
                    pc.skeleton(
                        pc.text(node),
                        is_loaded=QueryState.is_loaded,
                    ),
                    width="fit-content",
                    margin="0.5rem",
                    padding="0.5rem",
                    display="inline-block",
                    bg=get_color("gray", 50),
                    font_size="sm",
                ),
            ),
            min_height="50px",
            padding="1rem",
        ),
        save_modal(),
        width="80%",
        height="100%",
        padding="1rem",
    )


def save_modal():
    return pc.modal(
        pc.modal_overlay(
            pc.modal_content(
                pc.modal_header("Save"),
                pc.modal_body(
                    pc.vstack(
                        pc.form_control(
                            pc.form_label("Name"),
                            pc.input(
                                placeholder="Name",
                                value=SaveModalState.name,
                                on_change=SaveModalState.set_name,
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
                                value=SaveModalState.description,
                                on_change=SaveModalState.set_description,
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
                            on_click=lambda: SaveModalState.done(
                                QueryState.labels, QueryState.taints
                            ),
                        ),
                        pc.button("Cancel", on_click=SaveModalState.cancel),
                    ),
                ),
            )
        ),
        is_open=SaveModalState.show,
    )


def index():
    return page(content())
