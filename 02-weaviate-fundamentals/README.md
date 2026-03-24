# 02 - Weaviate Fundamentals

## Aim

Explore vector database capabilities using Weaviate Cloud and a movies dataset. The project covers the full workflow from collection design and data ingestion to various search strategies and retrieval-augmented generation.

## What I Did

1. **Collection design** - Created collections (`Movie`, `Review`, `Synopsis`) with cross-references between them
2. **Data ingestion** - Imported movie data including properties and inter-collection references, using a rate-limited `BatchImporter` utility to stay within API limits
3. **Search strategies** - Experimented with keyword (BM25), vector (semantic), filtered, and hybrid search
4. **RAG** - Used Weaviate's generative module to run retrieval-augmented generation queries directly against the collection

## Search Strategies

| Strategy | Description |
|----------|-------------|
| Keyword (BM25) | Exact token matching with optional wildcard filters |
| Vector | Semantic similarity via embeddings |
| Hybrid | Weighted blend of keyword and vector (`alpha` controls the balance) |
| Filtered | Any search narrowed by property conditions |
| RAG | Retrieval + generation via `collection.generate` |

## Technology

| Component | Tool |
|-----------|------|
| Vector database | Weaviate Cloud |
| Vectorizer | Gemini (`text2vec-google`) |
| Generative module | Gemini |
| Dataset | Movies (CSV) |

---

## Results & Takeaways

<!-- Results and takeaways go here -->
