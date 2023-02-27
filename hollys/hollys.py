import pynecone as pc
from kubernetes import config

from hollys.state import QueryState, SavedQueryState

# comment(heumsi): kube config needs to be loaded first before any other packages are imported.
try:
    config.load_kube_config()
except:
    config.load_incluster_config()


from hollys import state
from hollys.page import query, saved_query

app = pc.App(state=state.BaseState)
app.add_page(query.index, route="/", on_load=QueryState.init)
app.add_page(query.index, route="/query", on_load=QueryState.init)
app.add_page(saved_query.index, route="/queries/[name]")
app.compile()
