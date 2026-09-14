from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_aws import BedrockEmbeddings
from langchain_chroma import Chroma
import shutil
import os

CHROMA_PATH = "chroma"
DATA_PATH = "data"


def main():
    generate_data_store()


def generate_data_store():
    documents = load_documents()
    chunks = split_text(documents)
    save_to_chroma(chunks)


def load_documents():
    loader = DirectoryLoader(
        DATA_PATH,
        glob="*.md",
        recursive=True,  # walk data/claude, data/hackerrank, data/visa, etc.
        silent_errors=True,
        show_progress=True,  # ← shows which files are being loaded
    )
    return loader.load()


def split_text(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True,
    )
    return text_splitter.split_documents(documents)


def get_embedding_function():
    return BedrockEmbeddings(model_id="amazon.titan-embed-text-v2:0")


def calculate_chunk_ids(chunks: list[Document]):
    for chunk in chunks:
        source = chunk.metadata.get("source")
        start_index = chunk.metadata.get("start_index")
        chunk.metadata["id"] = f"{source}:{start_index}"
    return chunks


def save_to_chroma(chunks: list[Document]):
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    chunks = calculate_chunk_ids(chunks)
    chunk_ids = [chunk.metadata["id"] for chunk in chunks]

    db = Chroma.from_documents(
        chunks,
        get_embedding_function(),
        persist_directory=CHROMA_PATH,
        ids=chunk_ids,
    )
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")


if __name__ == "__main__":
    main()
