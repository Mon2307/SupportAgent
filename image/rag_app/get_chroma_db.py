import os
import shutil
import sys

CHROMA_PATH = "chroma"
IS_USING_IMAGE_RUNTIME = bool(os.environ.get("IS_USING_IMAGE_RUNTIME", False))
CHROMA_DB_INSTANCE = None

# Must happen before langchain_chroma is imported, since it imports chromadb
# at module load time, and chromadb checks the sqlite3 version on import.
if IS_USING_IMAGE_RUNTIME:
    __import__("pysqlite3")
    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

from langchain_chroma import Chroma
from rag_app.get_embedding_function import get_embedding_function


def get_chroma_db():
    global CHROMA_DB_INSTANCE
    if not CHROMA_DB_INSTANCE:
        if IS_USING_IMAGE_RUNTIME:
            copy_chroma_to_tmp()

        CHROMA_DB_INSTANCE = Chroma(
            persist_directory=get_runtime_chroma_path(),
            embedding_function=get_embedding_function(),
        )
        print(f"✅ Init ChromaDB {CHROMA_DB_INSTANCE} from {get_runtime_chroma_path()}")

    return CHROMA_DB_INSTANCE


def copy_chroma_to_tmp():
    dst_chroma_path = get_runtime_chroma_path()

    if not os.path.exists(dst_chroma_path):
        os.makedirs(dst_chroma_path)

    tmp_contents = os.listdir(dst_chroma_path)
    if len(tmp_contents) == 0:
        print(f"Copying ChromaDB from {CHROMA_PATH} to {dst_chroma_path}")
        shutil.copytree(CHROMA_PATH, dst_chroma_path, dirs_exist_ok=True)
    else:
        print(f"✅ ChromaDB already exists in {dst_chroma_path}")


def get_runtime_chroma_path():
    if IS_USING_IMAGE_RUNTIME:
        return f"/tmp/{CHROMA_PATH}"
    else:
        return CHROMA_PATH