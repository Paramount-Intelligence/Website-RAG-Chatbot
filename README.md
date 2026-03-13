# Paramount Nexus - AI Intelligence Assistant

<div align="center">

![Paramount Nexus](https://img.shields.io/badge/Paramount-Nexus-7209b7?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.14-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0+-green?style=for-the-badge&logo=flask)
![FAISS](https://img.shields.io/badge/FAISS-Vector_Search-orange?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**Advanced RAG-powered AI assistant for Paramount Intelligence**

[Features](#features) • [Quick Start](#quick-start) • [Setup](#setup) • [Architecture](#architecture) • [Contributing](#contributing)

</div>

---

## 🌟 Overview

**Paramount Nexus** is a production-ready, intelligent chatbot system designed specifically for Paramount Intelligence company. Built with cutting-edge RAG (Retrieval-Augmented Generation) technology, it provides accurate, context-aware responses about company information, services, and team members.

### Why Paramount Nexus?

- **🎯 Accurate & Contextual**: Retrieval-Augmented Generation ensures responses are grounded in your actual company data
- **⚡ Lightning Fast**: FAISS-powered vector search delivers results in milliseconds
- **🔒 Privacy First**: All data stays local - no external vector database APIs required
- **🎨 Modern UI**: Beautiful, professional interface designed for enterprise use
- **🐍 Python 3.14**: Fully compatible with the latest Python version
- **📱 Responsive**: Works flawlessly on desktop, tablet, and mobile devices

---

## ✨ Features

### Core Capabilities
- 🤖 **Intelligent Q&A**: Natural language understanding powered by Google Gemini
- 📚 **Knowledge Base**: Comprehensive information about company, services, and team
- 🔍 **Semantic Search**: FAISS vector similarity search for accurate retrieval
- 💬 **Conversational**: Context-aware responses with personality
- ⚡ **Real-time**: Instant responses with typing indicators
- 🎯 **Quick Suggestions**: Pre-loaded queries for common questions

### Technical Features
- **Local Vector Database**: FAISS for fast, offline similarity search
- **No API Keys Required**: Only needs Google Gemini for LLM (vector search is local)
- **Python 3.14 Compatible**: Latest Python version supported
- **Scalable Architecture**: Handles thousands of documents efficiently
- **Easy Deployment**: Simple Flask-based architecture
- **Extensible**: Easy to add new data sources and features

---

## 🚀 Quick Start

### Prerequisites
- Python 3.14+ (or Python 3.10+)
- Google Gemini API key ([Get one here](https://ai.google.dev/))
- 500MB disk space for embeddings

### Installation

1. **Clone or download the project**
   ```bash
   cd "D:\RAG chatbot"
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   # Create .env file
   echo GOOGLE_API_KEY=your_api_key_here > .env
   ```

4. **Prepare your data**
   
   Place your JSON files in the `data/` folder:
   - `paramount_company_rag.json`
   - `paramount_services_rag.json`
   - `paramount_team_rag.json`

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the chatbot**
   
   Open your browser to: http://localhost:5000

---

## 📁 Project Structure

```
RAG chatbot/
├── app.py                      # Flask application entry point
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (create this)
├── data/                       # Data directory
│   ├── paramount_company_rag.json
│   ├── paramount_services_rag.json
│   ├── paramount_team_rag.json
│   └── faiss_index/           # Auto-generated FAISS index
│       ├── index.faiss
│       └── metadata.pkl
├── modules/                    # Core RAG pipeline
│   ├── embeddings.py          # Embedding generation
│   ├── vectorstore.py         # FAISS vector database
│   ├── retriever.py           # Document retrieval
│   ├── generator.py           # Response generation
│   └── rag_pipeline.py        # Main RAG orchestration
├── static/                     # Frontend assets
│   ├── css/
│   │   └── style.css          # Modern UI styling
│   └── js/
│       └── chatbot.js         # Interactive chat logic
├── templates/                  # HTML templates
│   └── index.html             # Main chat interface
└── FAISS_SETUP.md             # Detailed setup guide
```

---

## 🏗️ Architecture

### RAG Pipeline

```
User Query
    ↓
[1] Embedding Generation (SentenceTransformers)
    ↓
[2] Vector Search (FAISS)
    ↓
[3] Context Retrieval (Top-K Documents)
    ↓
[4] Prompt Construction
    ↓
[5] LLM Generation (Google Gemini)
    ↓
Final Response
```

### Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|----------|
| **Backend** | Flask 3.0+ | Web framework |
| **LLM** | Google Gemini 2.5 Flash | Response generation |
| **Embeddings** | SentenceTransformers | Text vectorization |
| **Vector DB** | FAISS | Similarity search |
| **Frontend** | HTML/CSS/JS | User interface |
| **Language** | Python 3.14 | Core implementation |

---

## 🎨 UI/UX Features

- **Modern Glassmorphism Design**: Sleek, professional appearance
- **Gradient Backgrounds**: Dynamic, eye-catching visuals
- **Smooth Animations**: Polished user interactions
- **Quick Suggestions**: One-click access to common queries
- **Typing Indicators**: Real-time feedback during response generation
- **Responsive Layout**: Optimized for all screen sizes
- **Accessible**: Keyboard navigation and screen reader support

---

## 📊 Data Format

Your JSON files should follow this structure:

```json
[
  {
    "text": "Paramount Intelligence is a leading provider of AI solutions...",
    "metadata": {
      "source": "company_overview",
      "category": "about",
      "last_updated": "2026-03-01"
    }
  },
  {
    "text": "Our team consists of experienced professionals in AI and ML...",
    "metadata": {
      "source": "team_info",
      "category": "team",
      "last_updated": "2026-03-01"
    }
  }
]
```

---

## 🔧 Configuration

### Environment Variables (.env)

```bash
GOOGLE_API_KEY=your_google_gemini_api_key_here
```

### Config Settings (config.py)

```python
# FAISS Configuration
FAISS_INDEX_DIR = "data/faiss_index"

# RAG Configuration
TOP_K_CHUNKS = 5  # Number of documents to retrieve

# Model Configuration
GENERATION_MODEL = "gemini-2.5-flash"
```

---

## 🔄 Updating Data

To refresh the knowledge base:

1. Update your JSON files in `data/`
2. Delete the `data/faiss_index/` folder
3. Restart the application

The app will automatically rebuild the vector index on startup.

---

## 🐛 Troubleshooting

### Common Issues

**Q: "Vector DB is empty" error**
- Ensure JSON files are in `data/` folder
- Check JSON format is valid
- Verify files contain `"text"` fields

**Q: Slow first startup**
- First run downloads embedding model (~90MB)
- Subsequent runs are instant
- Be patient during initial setup

**Q: LLM errors**
- Verify `GOOGLE_API_KEY` is set correctly
- Check internet connection
- Ensure API key has proper permissions

See [FAISS_SETUP.md](FAISS_SETUP.md) for detailed troubleshooting.

---

## 🚀 Deployment

### Development
```bash
python app.py
```

### Production
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker (Optional)
```dockerfile
FROM python:3.14-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

---

## 🤝 Contributing

We welcome contributions! Areas for improvement:

- [ ] Add authentication and user management
- [ ] Implement conversation history
- [ ] Add multi-language support
- [ ] Create admin dashboard for data management
- [ ] Add analytics and usage tracking
- [ ] Implement caching layer
- [ ] Add A/B testing framework

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👥 Credits

**Paramount Nexus** is developed and maintained for Paramount Intelligence.

### Technologies Used
- [Flask](https://flask.palletsprojects.com/) - Web framework
- [FAISS](https://github.com/facebookresearch/faiss) - Vector similarity search
- [SentenceTransformers](https://www.sbert.net/) - Text embeddings
- [Google Gemini](https://ai.google.dev/) - Language model
- [Inter Font](https://rsms.me/inter/) - Typography

---

## 📞 Support

For questions or issues:
- 📧 Email: support@paramountintelligence.com
- 📖 Documentation: [FAISS_SETUP.md](FAISS_SETUP.md)
- 🐛 Issues: GitHub Issues (if applicable)

---

<div align="center">

Made with ❤️ for Paramount Intelligence

**Paramount Nexus** - Connecting Intelligence, Empowering Decisions

</div>
