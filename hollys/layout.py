import pynecone as pc

from hollys import style
from hollys.state import GlobalState, SavedQueryState, SidebarState


def header():
    return pc.box(
        pc.flex(
            pc.heading("Hollys", size="lg"),
            pc.badge(
                GlobalState.version,
                margin_left="0.5rem",
                font_weight="400",
                style={
                    "text-transform": "none",
                },
            ),
            align_items="flex-start",
        ),
        width="100%",
        padding="1rem 5rem",
        bg=style.Color.navbar_bg,
        border_bottom=f"0.07rem solid {style.Color.border}",
    )


def sidebar():
    return pc.box(
        pc.box(
            pc.link(
                pc.text("Query", font_size="md"),
                href="/query",
            ),
        ),
        pc.box(
            pc.text(
                "Saved Queries".upper(), font_size="xs", weight="300", margin="1rem 0"
            ),
            pc.cond(
                SidebarState.is_loaded,
                pc.foreach(
                    SidebarState.saved_queries,
                    lambda saved_query: pc.box(
                        pc.link(
                            pc.text(
                                saved_query.name_,
                                padding="0 0 0 0.5rem",
                                # comment(heumsi): Not used yet. but will be used after following issue is resolved.
                                # https://github.com/pynecone-io/pynecone/issues/609
                                # on_click=lambda: SavedQueryState.init,
                                on_click=[
                                    lambda: SavedQueryState.set_is_loaded(False),
                                    lambda: SavedQueryState.set_by_model(saved_query),
                                    SavedQueryState.refresh_nodes,
                                    lambda: SavedQueryState.set_is_loaded(True),
                                ],
                                font_size="sm",
                            ),
                            href="/saved-queries/" + saved_query.id,
                        ),
                        padding="0.2rem 0",
                        color="#00000080",
                        _hover={
                            "color": "#000000",
                            "cursor": "pointer",
                        },
                    ),
                ),
                pc.center(
                    pc.spinner(size="lg"),
                    margin_top="3rem",
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
