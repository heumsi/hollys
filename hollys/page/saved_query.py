import pynecone as pc

from hollys.layout import page
from hollys.state import SavedQueryState
from hollys.style import get_color


def content():
    return pc.box(
        pc.flex(
            pc.heading(SavedQueryState.name_, size="lg"),
            pc.spacer(),
            pc.text(
                "Delete",
                font_size="sm",
                color=get_color("gray", 500),
                _hover={
                    "color": "#000000",
                    "cursor": "pointer",
                },
                on_click=SavedQueryState.delete,
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
                pc.heading("Nodes", size="sm", padding="1rem 0"),
                pc.text(
                    SavedQueryState.nodes.length()
                    + " items",  # comment(heumsi): It seems that f-string is not supported yet.
                    margin_top="-0.5rem",
                    font_size="xs",
                    color=get_color("gray", 500),
                ),
                pc.box(
                    pc.foreach(
                        SavedQueryState.nodes,
                        lambda node: pc.box(
                            pc.skeleton(
                                pc.text(node),
                                is_loaded=SavedQueryState.is_loaded,
                            ),
                            width="fit-content",
                            margin="0.5rem 0.5rem 0.5rem 0",
                            padding="0.5rem",
                            display="inline-block",
                            bg=get_color("gray", 50),
                            font_size="sm",
                        ),
                    ),
                    min_height="50px",
                    padding="1rem 0",
                ),
                padding_left="1rem",
            ),
        ),
        width="80%",
        height="100%",
        padding="1rem",
    )


def index():
    return page(content())