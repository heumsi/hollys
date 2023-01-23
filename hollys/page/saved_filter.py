import pynecone as pc

from hollys.layout import body, header, saved_filter_content, sidebar
from hollys.state import ModalState, State


def index():
    return pc.vstack(
        header(),
        body(sidebar(State), saved_filter_content(State, ModalState)),
        spacing="0",
        width="100vw",
        height="100vh",
    )
