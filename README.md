# SupportAgent

RAG support agent: builds a Chroma vector store from markdown docs, embedded
via Amazon Bedrock (Titan).

## Setup

```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install "unstructured[md]"
```

AWS credentials for Bedrock must be available via the default credential
chain (env vars, `~/.aws/credentials`, or an SSO profile) — no `.env`
file is required.

## Run

1. Drop your `.md` source files under `data/` (gitignored — sync/copy it
   in separately), then build the vector store:

    ```sh
    python create_database.py
    ```

2. Query it:

    ```sh
    python -m rag_app.query_rag
    ```

   Run this as a module (`-m rag_app.query_rag`) from the repo root —
   running `python rag_app/query_rag.py` directly breaks its internal
   package imports.
