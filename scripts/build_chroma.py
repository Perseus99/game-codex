import os
import re
import glob

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma


# Paths (relative to project root)
PDF_DIR = "pdfs"
DB_DIR = "chroma_db"


def parse_game_from_filename(fname: str) -> str:
    base = os.path.splitext(fname)[0].lower()
    if base.endswith("_official"):
        base = base[:-len("_official")]
    base = re.sub(r"[^a-z0-9]+", "_", base)
    base = re.sub(r"_+", "_", base).strip("_")
    return base


def load_documents():
    pdf_paths = sorted(glob.glob(os.path.join(PDF_DIR, "*.pdf")))
    docs = []

    for path in pdf_paths:
        fname = os.path.basename(path)
        game = parse_game_from_filename(fname)

        print(f"Loading: {fname}")

        pages = PyPDFLoader(path).load()

        for page in pages:
            page.metadata.update({
                "game": game,
                "doc_type": "official_rules",
                "source_file": fname,
                "path": path
            })

        docs.extend(pages)

    print(f"Total pages loaded: {len(docs)}")
    return docs


def split_documents(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=300,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    chunks = splitter.split_documents(docs)
    print(f"Total chunks created: {len(chunks)}")
    return chunks


def build_chroma(chunks):
    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=DB_DIR
    )

    print(f"✅ ChromaDB created at: {DB_DIR}")
    print(f"✅ Total chunks indexed: {len(chunks)}")


def main():
    docs = load_documents()
    chunks = split_documents(docs)
    build_chroma(chunks)


if __name__ == "__main__":
    main()