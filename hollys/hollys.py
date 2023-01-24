import pynecone as pc
from kubernetes import config

# comment(heumsi): kube config needs to be loaded first before any other packages are imported.
try:
    config.load_kube_config()
except:
    config.load_incluster_config()


from hollys import state
from hollys.page import query, saved_query

app = pc.App(state=state.BaseState)
app.add_page(query.index, path="/")
app.add_page(query.index, path="/query")
app.add_page(saved_query.index, path="/queries")
app.compile()
