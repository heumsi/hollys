import pynecone as pc
from kubernetes import config

from hollys.state import QueryState, SidebarState

# comment(heumsi): kube config needs to be loaded first before any other packages are imported.
try:
    config.load_kube_config()
except:
    config.load_incluster_config()


from hollys import state
from hollys.page import query, saved_query

meta = {
    "title": "Hollys",
}

app = pc.App(
    state=state.BaseState,
)
app.add_page(
    query.index,
    route="/",
    on_load=[
        # comment(heumsi): This does not working yet (I will fix this after pynecone version upgrade)
        # SidebarState.set_is_loaded(False)
        SidebarState.init,
        QueryState.init,
    ],
    **meta,
)
app.add_page(
    query.index,
    route="/query",
    on_load=[SidebarState.init, QueryState.init],
    **meta,
)
app.add_page(
    saved_query.index,
    route="/saved-queries/[id]",
    **meta,
)
app.compile()
