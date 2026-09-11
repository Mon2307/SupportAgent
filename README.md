# SupportAgent

RAG support agent: builds a Chroma vector store from markdown docs, embedded
via Amazon Bedrock (Titan).

## Getting Started (local)

### Installing requirements

```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install "unstructured[md]"
```

AWS credentials for Bedrock (`amazon.titan-embed-text-v2:0`) must be
available via the default credential chain (env vars, `~/.aws/credentials`,
or an SSO profile) — no `.env` file is required.

### Populate the database

Drop your `.md` source files under `data/` (this repo's `data/` is
gitignored — sync/copy it in separately), then run:

```sh
python create_database.py
```

This loads every `.md` file under `data/`, splits it into chunks, embeds
each chunk via Bedrock Titan, and (re)builds the `chroma/` vector store.
