# LLM Demos

A collection of experiments and demonstrations exploring large language models and related AI technologies.

## Overview

This repository serves as a hands-on playground for building with LLMs and adjacent tools. Projects here range from quick proof-of-concept scripts to more complete integrations, covering topics such as:

- Prompt engineering and evaluation
- LLM API integrations (Anthropic, OpenAI, etc.)
- Retrieval-augmented generation (RAG)
- Agents and tool use
- Fine-tuning and embeddings
- Multimodal applications

## Structure

Projects are organized into subdirectories. Each subdirectory contains its own `README.md` with setup instructions and details.

```
llm-demos/
├── README.md
├── 01-local-rag-pipeline
│   ├── README.md
│   └── ...
└── 02-weaviate-fundamentals
    ├── README.md
    └── ...
```

## Setup

After cloning the repo, run the following once from the root to make shared utilities importable across all subprojects:

```bash
pip install -e .
```

Then install dependencies for the specific subproject you want to run:

```bash
cd <subproject-folder>
pip install -r requirements.txt
```

## Prerequisites

Requirements vary by project. Common dependencies include:

- Python 3.10+
- API keys for relevant providers. Set this in .env.