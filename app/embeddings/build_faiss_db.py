# --- build_faiss_db.py ---

from pathlib import Path
from sentence_transformers import SentenceTransformer
import faiss
import pandas as pd
import pickle
import numpy as np
from tqdm import tqdm
import nltk
from nltk.tokenize import PunktSentenceTokenizer

# Download punkt if not already present
nltk.download('punkt')

# Load Punkt tokenizer manually (bypasses 'punkt_tab' bug)
tokenizer = PunktSentenceTokenizer()

# Load embedding model
model_name = "BAAI/bge-small-en"
model = SentenceTransformer(model_name)

# Set dynamic paths
script_path = Path(__file__).resolve()
app_folder = script_path.parent.parent

extracted_texts_folder = app_folder / "extracted_texts"
embedding_folder = app_folder / "embeddings"
embedding_folder.mkdir(parents=True, exist_ok=True)

# Cache file paths
embedding_path = embedding_folder / "forced_labour_embeddings.npy"
metadata_path = embedding_folder / "forced_labour_metadata.pkl"
faiss_path = embedding_folder / "forced_labour_faiss.index"

# Prepare documents
documents = []
metadata = []

for txt_file in tqdm(list(extracted_texts_folder.glob("*.txt")), desc="Reading documents"):
    with open(txt_file, "r", encoding="utf-8") as f:
        text = f.read()

    company_name = txt_file.stem.split("_")[0]
    file_name = txt_file.stem

    # Use smarter sentence tokenizer
    sentences = tokenizer.tokenize(text)

    chunk = ""
    for sentence in sentences:
        if len(chunk) + len(sentence) <= 5 00:  # target ~500-800 characters
            chunk += " " + sentence
        else:
            documents.append(chunk.strip())
            metadata.append({
                "company": company_name,
                "source_file": file_name
            })
            chunk = sentence

    if chunk:
        documents.append(chunk.strip())
        metadata.append({
            "company": company_name,
            "source_file": file_name
        })

# If cache exists, skip
if embedding_path.exists() and metadata_path.exists() and faiss_path.exists():
    print("Cached FAISS index and metadata found — skipping rebuild.")
else:
    print(f"Total chunks to embed: {len(documents)}")

    # Generate embeddings
    embeddings = model.encode(documents, show_progress_bar=True, batch_size=32, normalize_embeddings=True)

    # Save embeddings to .npy
    np.save(embedding_path, embeddings)

    # Save metadata
    with open(metadata_path, "wb") as f:
        pickle.dump(metadata, f)

    # Create FAISS index and save
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    faiss.write_index(index, str(faiss_path))

    print("FAISS vector database built and saved successfully.")
