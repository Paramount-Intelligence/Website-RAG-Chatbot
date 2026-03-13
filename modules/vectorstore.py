import os
import json
import pickle
import faiss
import numpy as np
from modules.embeddings import generate_embedding
from config import FAISS_INDEX_DIR, TOP_K_CHUNKS

# ----------------------------------------
# FAISS INDEX PATHS
# ----------------------------------------
INDEX_FILE = os.path.join(FAISS_INDEX_DIR, "index.faiss")
METADATA_FILE = os.path.join(FAISS_INDEX_DIR, "metadata.pkl")

# Ensure directory exists
os.makedirs(FAISS_INDEX_DIR, exist_ok=True)


# ----------------------------------------
# LOAD OR CREATE FAISS INDEX
# ----------------------------------------
def get_or_create_index():
    """Get existing FAISS index or create a new one."""
    try:
        if os.path.exists(INDEX_FILE) and os.path.exists(METADATA_FILE):
            print(f"[INFO] Loading existing FAISS index from {FAISS_INDEX_DIR}")
            index = faiss.read_index(INDEX_FILE)
            with open(METADATA_FILE, "rb") as f:
                metadata = pickle.load(f)
            return index, metadata
        else:
            print(f"[INFO] Creating new FAISS index")
            # FAISS index for 384-dimensional embeddings (all-MiniLM-L6-v2)
            index = faiss.IndexFlatL2(384)
            metadata = []
            return index, metadata
    except Exception as e:
        print(f"[ERROR] Failed to load/create index: {e}")
        raise


# ----------------------------------------
# SAVE FAISS INDEX
# ----------------------------------------
def save_index(index, metadata):
    """Save FAISS index and metadata to disk."""
    try:
        faiss.write_index(index, INDEX_FILE)
        with open(METADATA_FILE, "wb") as f:
            pickle.dump(metadata, f)
        print(f"[INFO] Index saved to {FAISS_INDEX_DIR}")
    except Exception as e:
        print(f"[ERROR] Failed to save index: {e}")
        raise


# ----------------------------------------
# LOAD MULTIPLE JSON DATASETS
# ----------------------------------------
def load_all_rag_files():
    data_dir = "data"

    json_files = [
        "paramount_company_rag.json",
        "paramount_services_rag.json",
        "paramount_team_rag.json"
    ]

    all_docs = []

    for file in json_files:
        path = os.path.join(data_dir, file)

        if not os.path.exists(path):
            print(f"[WARNING] File not found: {path}")
            continue

        try:
            with open(path, "r", encoding="utf-8") as f:
                docs = json.load(f)
                print(f"[INFO] Loaded {len(docs)} docs from {file}")
                all_docs.extend(docs)
        except Exception as e:
            print(f"[ERROR] Could not read {file}: {e}")

    print(f"[INFO] Total documents loaded: {len(all_docs)}")
    return all_docs


# ----------------------------------------
# INITIALIZE VECTOR DATABASE
# ----------------------------------------
def initialize_vector_db():
    """Initialize and populate the FAISS vector database."""
    try:
        index, metadata = get_or_create_index()

        # Skip rebuild if DB already populated
        if index.ntotal > 0:
            print(f"[INFO] Vector DB already initialized with {index.ntotal} embeddings.")
            return

        documents = load_all_rag_files()

        if not documents:
            print("[ERROR] No documents found. Cannot build vector DB.")
            return

        print(f"[INFO] Building vector DB with {len(documents)} documents...")

        embeddings = []
        metadata_list = []

        for i, doc in enumerate(documents):
            # ----------------------------------------
            # TEXT
            # ----------------------------------------
            text = doc.get("text", "").strip()
            if not text:
                continue

            # ----------------------------------------
            # GENERATE EMBEDDING
            # ----------------------------------------
            embedding = generate_embedding(text)
            if not embedding:
                print(f"[WARNING] Failed to embed text: {text[:40]}...")
                continue

            embeddings.append(embedding)

            # ----------------------------------------
            # METADATA CLEANING
            # ----------------------------------------
            meta = doc.get("metadata", {})

            if not isinstance(meta, dict):
                meta = {}

            clean_meta = {}
            for key, val in meta.items():
                # Convert list → comma-separated string
                if isinstance(val, list):
                    clean_meta[key] = ", ".join([str(v) for v in val])
                # Convert nested dict → JSON string
                elif isinstance(val, dict):
                    clean_meta[key] = json.dumps(val)
                # Valid types → keep
                else:
                    clean_meta[key] = val

            # Add guaranteed metadata
            clean_meta["source"] = doc.get("source", "paramount_rag_data")
            clean_meta["text"] = text  # Store the full text

            metadata_list.append(clean_meta)

        # ----------------------------------------
        # ADD VECTORS TO FAISS
        # ----------------------------------------
        if embeddings:
            embeddings_array = np.array(embeddings, dtype=np.float32)
            index.add(embeddings_array)
            metadata.extend(metadata_list)
            
            # Save index and metadata
            save_index(index, metadata)
            print(f"[SUCCESS] Vector DB initialization complete with {len(embeddings)} documents.")
        else:
            print("[ERROR] No valid embeddings to add.")

    except Exception as e:
        print(f"[ERROR] Vector DB initialization failed: {e}")
        raise


# ----------------------------------------
# SEARCH MODULE
# ----------------------------------------
def search_similar(query_embedding, top_k):
    """Search for similar documents in the FAISS vector store."""
    try:
        index, metadata = get_or_create_index()

        if not query_embedding:
            print("[ERROR] Empty query embedding.")
            return []

        if index.ntotal == 0:
            print("[ERROR] Vector DB is empty. Initialize it first.")
            return []

        # Convert query embedding to numpy array
        query_array = np.array([query_embedding], dtype=np.float32)

        # Search in FAISS
        distances, indices = index.search(query_array, min(top_k, index.ntotal))

        output = []
        for idx in indices[0]:
            if idx >= 0 and idx < len(metadata):
                meta = metadata[idx]
                text = meta.get("text", "")
                
                # Remove 'text' from metadata to avoid duplication
                meta_clean = {k: v for k, v in meta.items() if k != "text"}
                
                output.append({
                    "text": text,
                    "metadata": meta_clean
                })

        return output

    except Exception as e:
        print(f"[ERROR] Similarity search failed: {e}")
        return []

