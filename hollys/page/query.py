import pynecone as pc

from hollys.component.node_detail_modal import node_detail_modal
from hollys.layout import page
from hollys.state import NodeDetailModalState, QueryState, SaveModalState
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
                    on_click=[
                        QueryState.reset_label,
                        QueryState.reset_labels,
                        QueryState.reset_taint,
                        QueryState.reset_taints,
                        lambda: QueryState.set_is_loaded(False),
                        QueryState.refresh_nodes,
                        lambda: QueryState.set_is_loaded(True),
                    ],
                ),
                pc.text(
                    "Save",
                    font_size="sm",
                    color=get_color("gray", 500),
                    _hover={
                        "color": "#000000",
                        "cursor": "pointer",
                    },
                    on_click=SaveModalState.toggle_show,
                ),
                spacing="1rem",
            ),
            margin="0 0 1rem 0",
            align_items="flex-end",
        ),
        pc.box(
            pc.heading("Filter", size="md", padding="1rem 0"),
            pc.box(
                pc.heading("Labels", size="sm", padding="1rem 0"),
                pc.hstack(
                    pc.input(
                        placeholder="key=value",
                        value=QueryState.label,
                        on_change=QueryState.set_label,
                    ),
                    pc.button(
                        pc.icon(tag="add"),
                        color_scheme="green",
                        on_click=[
                            QueryState.add_label,
                            QueryState.reset_label,
                            lambda: QueryState.set_is_loaded(False),
                            QueryState.refresh_nodes,
                            lambda: QueryState.set_is_loaded(True),
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
                                pc.box(
                                    pc.text(label),
                                    width="fit-content",
                                    margin="0.5rem 0.5rem 0.5rem 0",
                                    padding="0.5rem",
                                    display="inline-block",
                                    bg=get_color("gray", 50),
                                    font_size="sm",
                                ),
                                pc.icon(
                                    tag="close",
                                    margin="0",
                                    pading="0",
                                    display="inline-block",
                                    color=get_color("gray", 300),
                                    font_size="0.5rem",
                                    _hover={
                                        "color": "#000000",
                                        "cursor": "pointer",
                                    },
                                    on_click=[
                                        lambda: QueryState.remove_label(label),
                                        lambda: QueryState.set_is_loaded(False),
                                        QueryState.refresh_nodes,
                                        lambda: QueryState.set_is_loaded(True),
                                    ],
                                ),
                                margin_right="0.5rem",
                            ),
                            display="inline-block",
                        ),
                    ),
                    min_height="50px",
                    padding="1rem 0",
                ),
                pc.heading("Taints", size="sm", padding="1rem 0"),
                pc.hstack(
                    pc.input(
                        placeholder="key(=value):effect",
                        value=QueryState.taint,
                        on_change=QueryState.set_taint,
                    ),
                    pc.button(
                        pc.icon(tag="add"),
                        color_scheme="green",
                        on_click=[
                            QueryState.add_taint,
                            QueryState.reset_taint,
                            lambda: QueryState.set_is_loaded(False),
                            QueryState.refresh_nodes,
                            lambda: QueryState.set_is_loaded(True),
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
                                pc.box(
                                    pc.text(taint),
                                    width="fit-content",
                                    margin="0.5rem 0.5rem 0.5rem 0",
                                    padding="0.5rem",
                                    display="inline-block",
                                    bg=get_color("gray", 50),
                                    font_size="sm",
                                ),
                                pc.icon(
                                    tag="close",
                                    margin="0",
                                    pading="0",
                                    display="inline-block",
                                    color=get_color("gray", 300),
                                    font_size="0.5rem",
                                    _hover={
                                        "color": "#000000",
                                        "cursor": "pointer",
                                    },
                                    on_click=[
                                        lambda: QueryState.remove_taint(taint),
                                        lambda: QueryState.set_is_loaded(False),
                                        QueryState.refresh_nodes,
                                        lambda: QueryState.set_is_loaded(True),
                                    ],
                                ),
                                margin_right="0.5rem",
                            ),
                            display="inline-block",
                        ),
                    ),
                    min_height="50px",
                    padding="1rem 0",
                ),
                padding_left="1rem",
            ),
        ),
        pc.box(
            pc.heading("Result", size="md", padding="1rem 0"),
            pc.box(
                pc.hstack(
                    pc.heading("Nodes", size="sm", padding="1rem 0"),
                    # comment(heumsi):
                    # Having the icon and tooltip nested inside copy_to_clipboard didn't work, so I separated them.
                    pc.copy_to_clipboard(
                        pc.icon(
                            tag="copy",
                            color="#00000080",
                            _hover={
                                "color": "#000000",
                                "cursor": "pointer",
                            },
                            on_click=lambda: QueryState.set_is_copied_tooltip_opened(
                                True
                            ),
                            on_mouse_out=lambda: QueryState.set_is_copied_tooltip_opened(
                                False
                            ),
                        ),
                        text=QueryState.nodes_as_str,
                    ),
                    pc.tooltip(
                        pc.text(""),
                        label="Copied",
                        is_open=QueryState.is_copied_tooltip_opened,
                    ),
                    spacing="0.5rem",
                ),
                pc.text(
                    QueryState.nodes.length()
                    + " items",  # comment(heumsi): It seems that f-string is not supported yet.
                    margin_top="-0.5rem",
                    font_size="xs",
                    color=get_color("gray", 500),
                ),
                pc.box(
                    pc.cond(
                        QueryState.is_loaded,
                        pc.foreach(
                            QueryState.nodes,
                            lambda node: pc.box(
                                pc.text(node),
                                width="fit-content",
                                margin="0.5rem 0.5rem 0.5rem 0",
                                padding="0.5rem",
                                display="inline-block",
                                bg=get_color("gray", 50),
                                font_size="sm",
                                on_click=[
                                    NodeDetailModalState.toggle_show,
                                    lambda: NodeDetailModalState.set_is_loaded(False),
                                    lambda: NodeDetailModalState.set_by_node_name(node),
                                    lambda: NodeDetailModalState.set_is_loaded(True),
                                ],
                                _hover={
                                    "cursor": "pointer",
                                    "background_color": get_color("gray", 200),
                                },
                            ),
                        ),
                        pc.center(
                            pc.spinner(size="lg"),
                            margin_top="3rem",
                        ),
                    ),
                    min_height="50px",
                    padding="1rem 0",
                ),
                padding_left="1rem",
            ),
        ),
        save_modal(),
        node_detail_modal(),
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
                                "This value will appear in the saved query list"
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
