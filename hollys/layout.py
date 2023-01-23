import pynecone as pc

from hollys import style
from hollys.state import SavedFilterState, SidebarState


def header():
    return pc.box(
        pc.heading("Hollys", size="lg"),
        width="100%",
        padding="1rem 5rem",
        bg=style.Color.navbar_bg,
        border_bottom=f"0.07rem solid {style.Color.border}",
    )


def sidebar():
    return pc.box(
        pc.box(
            pc.link(pc.text("Query", font_size="1em"), href="/query"),
        ),
        pc.box(
            pc.text("Saved filters", font_size="xs", margin="0 0 1rem 0"),
            pc.foreach(
                SidebarState.saved_filters,
                lambda saved_filter: pc.box(
                    pc.link(
                        pc.text(
                            saved_filter.name_,
                            padding="0 0 0 1rem",
                            on_click=lambda: SavedFilterState.set_by_model(
                                saved_filter
                            ),
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


def body(content):
    return pc.hstack(
        sidebar(),
        content,
        width="100%",
        height="100%",
        padding_inline="5rem",
        align_itrems="flex-start",
        spacing="0",
        bg=style.Color.body_bg,
    )


def page(content):
    return pc.vstack(
        header(),
        body(content),
        spacing="0",
        width="100vw",
        height="100vh",
    )
