import os

import pynecone as pc

config = pc.Config(
    app_name="hollys",
    port=os.getenv("PORT", "3000"),
    # api_url=os.getenv("API_URL", "ws:localhost:8000"),
    db_url=os.getenv("DB_URL", "sqlite:///pynecone.db"),
)
