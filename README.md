# AI-Powered Compliance & Policy Auditor (Interactive Desktop App)

This project is an **AI-powered desktop application** designed to simplify compliance and policy auditing. It allows users to **upload and index various policy documents** (PDFs, TXT, MD) and then ask an AI intelligent questions about their content directly through a **user-friendly graphical interface**.

## What It Does

This system helps organizations quickly find information, identify contradictions, and get summaries from large policy documents, saving time and reducing errors in compliance efforts. It's built to run entirely **locally and offline**, ensuring data privacy and no deployment costs.

## How It Works (Key Technologies)

The application uses a **modular architecture** based on the **Model Context Protocol (MCP)**. This means:

* **GUI (Streamlit):** The user interacts with an intuitive web-based interface (runs locally in your browser).
* **AI Agent (LangChain + LLM):** An intelligent AI (powered by a Large Language Model like GPT-3.5 or a local alternative) understands user questions and decides what actions to take.
* **MCP Client:** Built into the GUI, this client connects to specialized backend servers.
* **MCP Servers:** These are separate Python processes that provide specific "tools" for the AI:
    * **Document Ingestion:** Processes uploaded documents, breaks them into small pieces, and stores them in a **local vector database (ChromaDB)**.
    * **Semantic Search & Analysis:** Queries the vector database to find relevant information and performs other text analysis tasks.

This setup enables **Retrieval-Augmented Generation (RAG)**, allowing the AI to generate accurate answers by retrieving real-time information from your private documents.

## Impressive Aspects

* **Interactive GUI:** Provides a professional and easy-to-use interface for a complex AI system, enhancing user experience.
* **Modular Design (MCP):** Demonstrates advanced architectural thinking, making the system highly extensible and maintainable.
* **Retrieval-Augmented Generation (RAG):** Showcases a key technique for giving LLMs up-to-date, domain-specific knowledge, crucial for practical AI applications.
* **Local & Secure:** All processing is done offline, which is ideal for sensitive data and highlights your ability to build private AI solutions without cloud dependencies.
* **Solves a Real Problem:** Addresses a significant, costly challenge in compliance and legal fields, demonstrating practical problem-solving.

---

## Getting Started

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/ai-compliance-auditor.git
    cd ai-compliance-auditor
    ```
    (Remember to replace `yourusername/ai-compliance-auditor.git` with your actual GitHub repository URL).

2.  **Install Packages:**
    Make sure you have a `requirements.txt` file in your root directory listing all necessary packages (e.g., `streamlit`, `langchain`, `litellm`, `mcp[cli]`, `pypdf`, `sentence-transformers`, `chromadb`, etc.). Then, run:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set Up API Keys:**
    For your LLM (e.g., OpenAI's GPT-3.5/4), ensure your API key (`OPENAI_API_KEY`) is set as an **environment variable** on your system or placed in a `.env` file at the project root (and ensure `.env` is in your `.gitignore`).

4.  **Run MCP Servers:**
    Open **two separate terminal windows** and start each MCP server process:
    ```bash
    # Terminal 1: For Document Ingestion
    uv run servers/ingestion_server.py

    # Terminal 2: For Semantic Search & Analysis
    uv run servers/analysis_server.py
    ```
    Keep these terminals running in the background.

5.  **Run GUI:**
    In a **third terminal window**, navigate to the project root and start the Streamlit application:
    ```bash
    streamlit run app.py
    ```
    Your default web browser should automatically open a new tab to the application's interface (typically `http://localhost:8501`).

## Project Structure

```
ai-compliance-auditor/
├── data/
│   ├── chromadb/         # Local Chroma DB persistence
│   └── uploaded_docs/    # Temporary storage for uploaded documents
├── config/               # New: For application-wide configuration
│   └── __init__.py
│   └── settings.py       # All app settings (API keys, model names, etc.)
├── models/               # New: For Pydantic models, custom data structures
│   └── __init__.py
│   └── app_models.py     # e.g., for IngestionRequest, QueryResponse
├── services/             # New: Core reusable functionalities (embedding, vector store, Stagehand client)
│   ├── __init__.py
│   ├── embeddings.py
│   ├── vector_store.py
│   └── stagehand.py      # Your StagehandClient and related utilities
├── pipelines/            # New: Orchestrates ingestion and RAG flows
│   ├── __init__.py
│   ├── ingestion.py      # Contains all ingestion logic (loaders, splitters, processors)
│   └── rag.py            # Contains core RAG logic (retrieval, LLM calls, tool orchestration)
├── main.py               # Streamlit entry point (Home page or just redirects)
├── pages/
│   ├── chat.py           # Uses `pipelines.rag`
│   ├── settings.py       # Interacts with `config.settings`
│   └── upload.py         # Uses `pipelines.ingestion`
├── pyproject.toml
├── README.md
└── uv.lock
```
