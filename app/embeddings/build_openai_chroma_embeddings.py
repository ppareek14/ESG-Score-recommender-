# --- build_openai_chroma_embeddings.py ---
from pathlib import Path
import openai
import os
from tqdm import tqdm
import json
from dotenv import load_dotenv
from chromadb import PersistentClient
from chromadb.config import Settings
import chromadb.utils.embedding_functions as embedding_functions
from math import ceil

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Paths
project_root = Path(__file__).resolve().parent.parent
jsonl_folder = project_root / "extracted_texts"
chroma_base_path = project_root / "chroma_store"
cache_path = project_root / "app" / "embeddings" / "embedding_cache.json"
cache_path.parent.mkdir(parents=True, exist_ok=True)
collection_name = "esg-forced-labour"

# Embedding function
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.getenv("CHROMA_OPENAI_API_KEY"),
    model_name="text-embedding-ada-002"
)

# Load or initialize embedding cache
if cache_path.exists():
    with open(cache_path, "r") as f:
        embedded_files = json.load(f)
else:
    embedded_files = {}

# Text chunker
def chunk_text(text, max_length=800, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + max_length, len(text))
        chunks.append(text[start:end])
        start += max_length - overlap
    return chunks

print("Starting upload to ChromaDB...")

for jsonl_file in tqdm(list(jsonl_folder.rglob("*.jsonl"))):
    if str(jsonl_file) in embedded_files:
        print(f"Skipping already embedded: {jsonl_file}")
        continue

    # Determine relative path (same as data/), and save to chroma_store/
    relative_path = jsonl_file.relative_to(jsonl_folder).parent
    company_chroma_path = chroma_base_path / relative_path
    company_chroma_path.mkdir(parents=True, exist_ok=True)

    # Initialize client & collection for this relative path
    client = PersistentClient(path=str(company_chroma_path), settings=Settings(allow_reset=True))
    collection = client.get_or_create_collection(
        name=collection_name,
        embedding_function=openai_ef
    )

    # Chunk & prepare documents
    ids, metadatas, documents = [], [], []
    with open(jsonl_file, "r", encoding="utf-8") as f:
        for line in f:
            entry = json.loads(line)
            page_num = entry["page"]
            for j, chunk in enumerate(chunk_text(entry["text"])):
                doc_id = f"{jsonl_file.stem}_p{page_num}_{j}"
                ids.append(doc_id)
                documents.append(chunk)
                metadatas.append({
                    "source": str(jsonl_file),
                    "page": page_num
                })

    # Upload in batches
    batch_size = 50
    total = len(documents)
    print(f"⬆ Uploading {total} chunks to ChromaDB for {relative_path}...")

    for i in range(0, total, batch_size):
        batch_docs = documents[i:i+batch_size]
        batch_ids = ids[i:i+batch_size]
        batch_meta = metadatas[i:i+batch_size]
        print(f"  Uploading batch {i//batch_size + 1} of {ceil(total/batch_size)}")
        collection.add(
            documents=batch_docs,
            metadatas=batch_meta,
            ids=batch_ids
        )

    # Mark file as embedded
    embedded_files[str(jsonl_file)] = True
    with open(cache_path, "w") as f:
        json.dump(embedded_files, f, indent=2)

    print(f"Completed uploading for {relative_path}")

print("\n All company embeddings uploaded successfully!")
