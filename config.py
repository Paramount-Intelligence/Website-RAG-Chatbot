import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- API KEY ---
# IMPORTANT: Replace 'YOUR_GEMINI_API_KEY' with your actual key or set it in a .env file.
# The Gemini API key is used for both embeddings and the LLM.
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "Your_api_key")


# --- FAISS CONFIGURATION ---
# Directory where FAISS index and metadata will be stored
FAISS_INDEX_DIR = "data/faiss_index"

# --- RAG CONFIGURATION ---
# The number of top-k chunks to retrieve from the vector store.
TOP_K_CHUNKS = 5

# --- MODEL CONFIGURATION ---
# Embedding model name
EMBEDDING_MODEL = "models/embedding-001"
# LLM model name for generation
GENERATION_MODEL = "gemini-pro"

# --- FLASK CONFIGURATION ---
# Secret key for Flask sessions (can be anything for this simple app)
SECRET_KEY = os.urandom(24)

# Validate Gemini API key
if GOOGLE_API_KEY == "YOUR_GEMINI_API_KEY":
    print("!!! WARNING: Using default API key. Please set GOOGLE_API_KEY in your .env file or config.py !!!")

