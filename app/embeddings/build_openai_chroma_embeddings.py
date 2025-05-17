# --- build_openai_chroma_embeddings.py (Batch Safe Version + Cache) ---

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

# Load API Key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set paths
project_root = Path(__file__).resolve().parent.parent
text_folder = project_root / "extracted_texts"
collection_name = "esg-forced-labour"
chroma_path = project_root / "chroma_store"
cache_path = project_root / "app" / "embeddings" / "embedding_cache.json"

# Ensure cache directory exists
cache_path.parent.mkdir(parents=True, exist_ok=True)

# Initialize Chroma DB client
client = PersistentClient(path=str(chroma_path), settings=Settings(allow_reset=True))

# Set embedding function
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.getenv("CHROMA_OPENAI_API_KEY"),
    model_name="text-embedding-ada-002"
)

# Create or get collection
collection = client.get_or_create_collection(
    name=collection_name,
    embedding_function=openai_ef
)

# Load or initialize embedding cache
if cache_path.exists():
    with open(cache_path, "r") as f:
        embedded_files = json.load(f)
else:
    embedded_files = {}

# Helper: Chunk text into ~800-char blocks
def chunk_text(text, max_length=800, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + max_length, len(text))
        chunks.append(text[start:end])
        start += max_length - overlap
    return chunks

# Prepare documents
ids = []
metadatas = []
documents = []

print("Loading and chunking documents...")
for i, txt_file in enumerate(tqdm(list(text_folder.glob("*.txt")))):
    if txt_file.name in embedded_files:
        print(f"Skipping already embedded file: {txt_file.name}")
        continue

    with open(txt_file, "r", encoding="utf-8") as f:
        text = f.read()

    company = txt_file.stem.split("_")[0]
    chunks = chunk_text(text)

    for j, chunk in enumerate(chunks):
        doc_id = f"{txt_file.stem}_{j}"
        ids.append(doc_id)
        documents.append(chunk)
        metadatas.append({"company": company, "source": txt_file.name})

    embedded_files[txt_file.name] = True

# Upload in safe batches
print("Uploading to Chroma DB with OpenAI embeddings (in batches)...")
batch_size = 50
total = len(documents)

for i in range(0, total, batch_size):
    batch_docs = documents[i:i+batch_size]
    batch_ids = ids[i:i+batch_size]
    batch_meta = metadatas[i:i+batch_size]

    print(f"Uploading batch {i//batch_size + 1} of {ceil(total/batch_size)}")
    collection.add(
        documents=batch_docs,
        metadatas=batch_meta,
        ids=batch_ids
    )

# Save updated cache
with open(cache_path, "w") as f:
    json.dump(embedded_files, f, indent=2)

print(f"Uploaded {len(documents)} new chunks to ChromaDB collection: '{collection_name}'")
# Remove invalid method call
# client.persist()