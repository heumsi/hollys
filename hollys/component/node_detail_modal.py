import pynecone as pc

from hollys.state import NodeDetailModalState
from hollys.style import get_color


def node_detail_modal():
    return pc.modal(
        pc.modal_overlay(
            pc.modal_content(
                pc.modal_header("Node Detail"),
                pc.modal_body(
                    pc.box(
                        pc.heading("Name", size="sm", padding="0.5rem 0"),
                        pc.cond(
                            NodeDetailModalState.is_loaded,
                            pc.box(
                                pc.text(NodeDetailModalState.name),
                                width="fit-content",
                                margin="0.5rem 0.5rem 0.5rem 0",
                                padding="0.5rem",
                                display="inline-block",
                                bg=get_color("gray", 50),
                                font_size="sm",
                            ),
                            pc.center(
                                pc.spinner(size="lg"),
                                margin_top="3rem",
                            ),
                        ),
                    ),
                    pc.box(
                        pc.heading("Labels", size="sm", padding="0.5rem 0"),
                        pc.cond(
                            NodeDetailModalState.is_loaded,
                            pc.box(
                                pc.foreach(
                                    NodeDetailModalState.labels,
                                    lambda label: pc.vstack(
                                        pc.box(
                                            pc.text(label),
                                            width="fit-content",
                                            margin="0.25rem 0",
                                            padding="0.5rem",
                                            display="inline-block",
                                            bg=get_color("gray", 50),
                                            font_size="sm",
                                        ),
                                        align_items="flex-start",
                                    ),
                                ),
                                min_height="50px",
                            ),
                            pc.center(
                                pc.spinner(size="lg"),
                                margin_top="3rem",
                            ),
                        ),
                        padding_top="1rem",
                    ),
                    pc.box(
                        pc.heading("Taints", size="sm", padding="0.5rem 0"),
                        pc.cond(
                            NodeDetailModalState.is_loaded,
                            pc.box(
                                pc.foreach(
                                    NodeDetailModalState.taints,
                                    lambda label: pc.vstack(
                                        pc.box(
                                            pc.text(label),
                                            width="fit-content",
                                            margin="0.25rem 0",
                                            padding="0.5rem",
                                            display="inline-block",
                                            bg=get_color("gray", 50),
                                            font_size="sm",
                                        ),
                                        align_items="flex-start",
                                    ),
                                ),
                                min_height="50px",
                            ),
                            pc.center(
                                pc.spinner(size="lg"),
                                margin_top="3rem",
                            ),
                        ),
                        padding_top="1rem",
                    ),
                ),
                pc.modal_footer(
                    pc.button(
                        "Close",
                        on_click=[
                            NodeDetailModalState.toggle_show,
                        ],
                    )
                ),
            ),
        ),
        size="2xl",
        is_open=NodeDetailModalState.show,
        close_on_esc=True,
    )
