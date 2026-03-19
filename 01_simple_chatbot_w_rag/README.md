# 01 - Simple Chatbot with RAG

## Aim

Build a minimal RAG (Retrieval-Augmented Generation) pipeline from scratch to understand the core mechanics: document ingestion, embedding, retrieval, and generation. The project also experiments with three query enhancement techniques to see their effect on retrieval quality.

## How it works

1. **Ingest** - PDF documents are loaded, split into overlapping text chunks, deduplicated, and embedded
2. **Store** - Embeddings are persisted in a local ChromaDB vector store
3. **Query** - User query is embedded and used to retrieve the top-k most similar chunks
4. **Generate** - Retrieved context is passed to a local LLM (Llama 3 via Ollama) to produce an answer

## Query Enhancement Techniques

| Flag | Technique | Description |
|------|-----------|-------------|
| `--HyDE` | Hypothetical Document Embedding | Generate a hypothetical answer first, then use it as the query embedding |
| `--query_exp` | Query Expansion | Expand the query with 10 related terms before retrieval |
| `--keyw_extr` | Keyword Extraction | Strip filler words using KeyBERT, keep only keywords for retrieval |

## Technology

| Component | Tool |
|-----------|------|
| Embeddings | `sentence-transformers` (`all-MiniLM-L6-v2`) |
| Vector store | ChromaDB (persistent, local) |
| LLM | Llama 3 via Ollama (local) |
| PDF parsing | pypdf |
| Keyword extraction | KeyBERT |

## Usage

```bash
# Ingest documents from ./data
python main.py --ingest

# Interactive chat
python main.py

# Single query
python main.py --query "What is X?"

# With query enhancement
python main.py --HyDE
python main.py --query_exp
python main.py --keyw_extr
```

---

## Results & Takeaways

<!-- Results and takeaways go here -->