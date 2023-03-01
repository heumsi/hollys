import os

import pynecone as pc

config = pc.Config(
    app_name="hollys",
    port=os.getenv("PORT", "3000"),
    api_url=os.getenv("API_URL", "http://localhost:8000"),
    bun_path=os.getenv("BUN_PATH", "$HOME/.bun/bin/bun"),
    db_url=os.getenv("DB_URL", "sqlite:///pynecone.db"),
)
