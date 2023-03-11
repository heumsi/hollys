import pynecone as pc

from hollys.layout import page
from hollys.state import GlobalState, SavedQueryState, SidebarState, SnippetModalState
from hollys.style import get_color


def content():
    return pc.box(
        pc.flex(
            pc.heading(SavedQueryState.name_, size="lg"),
            pc.spacer(),
            pc.hstack(
                pc.text(
                    "Snippet",
                    font_size="sm",
                    color=get_color("gray", 500),
                    _hover={
                        "color": "#000000",
                        "cursor": "pointer",
                    },
                    on_click=SnippetModalState.toggle_show,
                ),
                pc.text(
                    "Delete",
                    font_size="sm",
                    color=get_color("gray", 500),
                    _hover={
                        "color": "#000000",
                        "cursor": "pointer",
                    },
                    on_click=[
                        SavedQueryState.delete,
                        lambda: GlobalState.redirect("/"),
                    ],
                ),
                spacing="1rem",
            ),
            margin="0 0 1rem 0",
            align_items="flex-end",
        ),
        pc.text(
            SavedQueryState.description_,
            margin_top="-0.5rem",
            min_height="2rem",
            font_size="xs",
            color=get_color("gray", 500),
        ),
        pc.box(
            pc.heading("Filter", size="md", padding="1rem 0"),
            pc.box(
                pc.heading("Labels", size="sm", padding="1rem 0"),
                pc.text(
                    SavedQueryState.labels.length()
                    + " items",  # comment(heumsi): It seems that f-string is not supported yet.
                    margin_top="-0.5rem",
                    font_size="xs",
                    color=get_color("gray", 500),
                ),
                pc.box(
                    pc.foreach(
                        SavedQueryState.labels,
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
                                margin_right="0.5rem",
                            ),
                            display="inline-block",
                        ),
                    ),
                    min_height="50px",
                    padding="1rem 0",
                ),
                pc.heading("Taints", size="sm", padding="1rem 0"),
                pc.text(
                    SavedQueryState.taints.length()
                    + " items",  # comment(heumsi): It seems that f-string is not supported yet.
                    margin_top="-0.5rem",
                    font_size="xs",
                    color=get_color("gray", 500),
                ),
                pc.box(
                    pc.foreach(
                        SavedQueryState.taints,
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
                            on_click=lambda: SavedQueryState.set_is_copied_tooltip_opened(
                                True
                            ),
                            on_mouse_out=lambda: SavedQueryState.set_is_copied_tooltip_opened(
                                False
                            ),
                        ),
                        text=SavedQueryState.nodes_as_str,
                    ),
                    pc.tooltip(
                        pc.text(""),
                        label="Copied",
                        is_open=SavedQueryState.is_copied_tooltip_opened,
                    ),
                    spacing="0.5rem",
                ),
                pc.text(
                    SavedQueryState.nodes.length()
                    + " items",  # comment(heumsi): It seems that f-string is not supported yet.
                    margin_top="-0.5rem",
                    font_size="xs",
                    color=get_color("gray", 500),
                ),
                pc.box(
                    pc.cond(
                        SavedQueryState.is_loaded,
                        pc.foreach(
                            SavedQueryState.nodes,
                            lambda node: pc.box(
                                pc.text(node),
                                width="fit-content",
                                margin="0.5rem 0.5rem 0.5rem 0",
                                padding="0.5rem",
                                display="inline-block",
                                bg=get_color("gray", 50),
                                font_size="sm",
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
        snippet_modal(),
        width="80%",
        height="100%",
        padding="1rem",
    )


def snippet_modal():
    return pc.modal(
        pc.modal_overlay(
            pc.modal_content(
                pc.modal_header("Snippet"),
                pc.modal_body(
                    pc.box(
                        pc.box(
                            pc.heading("For Nodes", size="sm", padding="0.5rem 0"),
                            pc.text(
                                "If you want the node to be included in this query, run kubectl taints and labels command.",
                                padding="0.5rem 0",
                            ),
                            pc.heading(
                                "Labels",
                                size="xs",
                                padding="0.5rem 0",
                            ),
                            pc.cond(
                                SavedQueryState.labels_empty,
                                pc.markdown("```\nThere is nothing to run."),
                                pc.markdown(
                                    SavedQueryState.labels_as_kubectl,
                                    padding="0.5rem 0",
                                ),
                            ),
                            pc.heading(
                                "Taints",
                                size="xs",
                                padding="0.5rem 0",
                            ),
                            pc.cond(
                                SavedQueryState.taints_empty,
                                pc.markdown("```\nThere is nothing to run."),
                                pc.markdown(
                                    SavedQueryState.taints_as_kubectl,
                                    padding="0.5rem 0",
                                ),
                            ),
                        ),
                        pc.box(
                            pc.heading("For Pods", size="sm", padding="0.5rem 0"),
                            pc.text(
                                "If you want pods to be scheduled in these nodes, add following in pods' spec",
                                padding="0.5rem 0",
                            ),
                            pc.heading(
                                "Node affinity",
                                size="xs",
                                padding="0.5rem 0",
                            ),
                            pc.cond(
                                SavedQueryState.labels_empty,
                                pc.markdown("```\nThere is nothing to add."),
                                pc.markdown(SavedQueryState.labels_as_node_affinity),
                            ),
                            pc.heading(
                                "Tolerations",
                                size="xs",
                                padding="0.5rem 0",
                            ),
                            pc.cond(
                                SavedQueryState.taints_empty,
                                pc.markdown("```\nThere is nothing to add."),
                                pc.markdown(SavedQueryState.taints_as_tolerations),
                            ),
                            padding="2rem 0 0 0",
                        ),
                        spacing="1rem",
                    ),
                ),
                pc.modal_footer(
                    pc.button("Close", on_click=SnippetModalState.toggle_show)
                ),
            ),
        ),
        size="2xl",
        is_open=SnippetModalState.show,
        close_on_esc=True,
    )


def index():
    return page(content())
