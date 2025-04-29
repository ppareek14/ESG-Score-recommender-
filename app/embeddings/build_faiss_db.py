# --- build_faiss_db.py ---

from pathlib import Path
from sentence_transformers import SentenceTransformer
import faiss
import pandas as pd
import pickle
from tqdm import tqdm

# Load BGE-small model (local embeddings)
model_name = "BAAI/bge-small-en"
model = SentenceTransformer(model_name)

# Define paths dynamically
script_path = Path(__file__).resolve()
app_folder = script_path.parent.parent

extracted_texts_folder = app_folder / "extracted_texts"
embedding_folder = app_folder / "embeddings"
embedding_folder.mkdir(parents=True, exist_ok=True)

# Parameters
chunk_size = 500  # number of characters per chunk (approx ~300-500 tokens)
overlap_size = 50  # to allow slight overlap between chunks (for context)

# Prepare data
documents = []
metadata = []

for txt_file in tqdm(list(extracted_texts_folder.glob("*.txt")), desc="Reading documents"):
    with open(txt_file, "r", encoding="utf-8") as f:
        text = f.read()

    company_name = txt_file.stem.split("_")[0]
    file_name = txt_file.stem

    # Chunk the text
    for i in range(0, len(text), chunk_size - overlap_size):
        chunk = text[i:i + chunk_size]
        if chunk.strip():  # avoid empty chunks
            documents.append(chunk)
            metadata.append({
                "company": company_name,
                "source_file": file_name
            })

# Create embeddings
print(f"Total chunks to embed: {len(documents)}")
embeddings = model.encode(documents, show_progress_bar=True, batch_size=32, normalize_embeddings=True)

# Build FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# Save FAISS index
faiss.write_index(index, str(embedding_folder / "forced_labour_faiss.index"))

# Save metadata separately
with open(embedding_folder / "forced_labour_metadata.pkl", "wb") as f:
    pickle.dump(metadata, f)

print("FAISS vector database built and saved successfully!")
