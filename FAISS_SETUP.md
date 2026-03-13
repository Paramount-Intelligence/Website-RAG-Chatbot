# FAISS Setup Guide for RAG Chatbot

## Overview
FAISS (Facebook AI Similarity Search) is a **local vector database** that requires **NO API keys**. All embeddings and indexes are stored on your machine.

## Prerequisites
- Python 3.14.3+ ✓ (fully compatible!)
- Paramount data JSON files in `data/` folder
- ~500MB disk space for embeddings (grows with data)

## Step 1: Install Dependencies

Dependencies are already listed in `requirements.txt`:
```
faiss-cpu>=1.8.0
numpy>=1.24.0
sentence-transformers>=2.2.0
```

Install them:
```powershell
pip install -r requirements.txt
```

## Step 2: Configure Environment

Create `.env` file in the root directory:
```
GOOGLE_API_KEY=your_google_gemini_api_key_here
```

You only need your **Google Gemini API key** for LLM generation. FAISS needs no credentials.

Optional: Copy from template:
```powershell
Copy-Item .env.example .env
# Then edit .env with just your Google API key
```

## Step 3: Prepare Data Files

Make sure you have these files in the `data/` folder:
- `paramount_employees_rag.json`
- `paramount_master_rag.json`
- `paramount_pdf_rag.json`

If you have files with different names, update them in `modules/vectorstore.py` lines 62-65:
```python
json_files = [
    "paramount_employees_rag.json",
    "paramount_master_rag.json",
    "paramount_pdf_rag.json"
]
```

## Step 4: Run the Application

```powershell
python app.py
```

**On first run:**
1. Loads and embeds all documents (2-5 minutes depending on data size)
2. Creates FAISS index in `data/faiss_index/`
3. Saves metadata in `data/faiss_index/metadata.pkl`
4. Starts the Flask server on `http://localhost:5000`

**On subsequent runs:**
- Loads the pre-built index instantly (< 1 second)

## What Gets Stored Locally

```
data/
└── faiss_index/
    ├── index.faiss      # Vector index (binary, ~100-500MB)
    └── metadata.pkl     # Document metadata and text
```

All data stays on your machine. No external APIs or cloud services involved!

## Advantages of FAISS

✓ **No API keys needed** - Zero configuration
✓ **Completely local** - Your data never leaves your computer
✓ **Fast** - Similarity search in milliseconds
✓ **Scalable** - Handles thousands of documents efficiently
✓ **Python 3.14 compatible** - Works perfectly!
✓ **Free** - Open source, no billing
✓ **Simple** - Just pass embedding vectors and search

## Troubleshooting

### "File not found" error for JSON files
- Make sure your files are in the `data/` folder with exact names
- Check file extension is `.json` (not `.txt` or `.csv`)
- Update file names in `modules/vectorstore.py` if different

### "Vector DB is empty" on search
- Make sure your JSON files have valid `"text"` fields
- Check the initialization completed successfully
- Delete `data/faiss_index/` folder to rebuild

### Slow first run
- First run generates embeddings from scratch (normal, 2-5 min)
- Download time for `all-MiniLM-L6-v2` model (~90MB)
- Subsequent runs are instant

### "No documents found"
- Verify JSON files exist in `data/` folder
- Ensure JSON format is valid (use `python -m json.tool file.json`)
- Check documents have `"text"` field not empty

## Switching Organizations

To use documents from a different organization:

1. Update file names in `modules/vectorstore.py` (lines 62-65)
2. Delete `data/faiss_index/` folder
3. Run `python app.py` to rebuild index

Example for a new organization:
```python
json_files = [
    "neworg_employees_rag.json",
    "neworg_master_rag.json",
    "neworg_pdf_rag.json"
]
```

## Performance Tuning

If you have **many documents** (1M+):
- FAISS supports GPU acceleration with `faiss-gpu`
- For CPU: FAISS is still very fast for search

To use GPU (optional):
```powershell
pip uninstall faiss-cpu
pip install faiss-gpu
```

## Testing the Setup

Once running, test at `http://localhost:5000`:
```
Query: "Tell me about [employee name]"
```

You should get results from your Paramount data!

---

**Resources**:
- FAISS GitHub: https://github.com/facebookresearch/faiss
- FAISS Wiki: https://github.com/facebookresearch/faiss/wiki
- Sentence Transformers: https://www.sbert.net/
- Google Gemini API: https://ai.google.dev/
