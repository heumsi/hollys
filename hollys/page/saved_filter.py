import pynecone as pc

from hollys.layout import page
from hollys.state import SavedFilterState
from hollys.style import get_color


def content():
    return pc.box(
        pc.flex(
            pc.heading(SavedFilterState.name_, size="lg"),
            pc.spacer(),
            pc.text(
                "Delete",
                font_size="sm",
                color=get_color("gray", 500),
                _hover={
                    "color": "#000000",
                    "cursor": "pointer",
                },
                on_click=SavedFilterState.delete,
            ),
            margin="0 0 1rem 0",
            align_items="flex-end",
        ),
        pc.text(
            SavedFilterState.description_,
            margin_top="-0.5rem",
            min_height="2rem",
            font_size="xs",
            color=get_color("gray", 500),
        ),
        pc.heading("Labels", size="md", padding="1rem 0"),
        pc.text(
            SavedFilterState.labels.length()
            + " items",  # comment(heumsi): It seems that f-string is not supported yet.
            margin_top="-0.5rem",
            font_size="xs",
            color=get_color("gray", 500),
        ),
        pc.box(
            pc.foreach(
                SavedFilterState.labels,
                lambda label: pc.box(
                    pc.text(label),
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
        pc.heading("Taints", size="md", padding="1rem 0"),
        pc.text(
            SavedFilterState.taints.length()
            + " items",  # comment(heumsi): It seems that f-string is not supported yet.
            margin_top="-0.5rem",
            font_size="xs",
            color=get_color("gray", 500),
        ),
        pc.box(
            pc.foreach(
                SavedFilterState.taints,
                lambda taint: pc.box(
                    pc.text(taint),
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
        pc.heading("Nodes", size="md", padding="1rem 0"),
        pc.text(
            SavedFilterState.nodes.length()
            + " items",  # comment(heumsi): It seems that f-string is not supported yet.
            margin_top="-0.5rem",
            font_size="xs",
            color=get_color("gray", 500),
        ),
        pc.box(
            pc.foreach(
                SavedFilterState.nodes,
                lambda node: pc.box(
                    pc.skeleton(
                        pc.text(node),
                        is_loaded=SavedFilterState.is_loaded,
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
        width="80%",
        height="100%",
        padding="1rem",
    )


def index():
    return page(content())
