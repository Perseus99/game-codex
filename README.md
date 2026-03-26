# 🎲 The Game Codex
A fully offline RAG-powered board game rules assistant built with Streamlit, LangChain, ChromaDB, and Ollama.

**Supported Games:** UNO · Monopoly · Monopoly Deal · Catan · Root · Betrayal at House on the Hill · Sushi Go! · Pandemic · Ticket to Ride · Risk

---

## Setup

**Requirements:** Python 3.11.9, [Ollama](https://ollama.com/download)

### 1. Create a virtual environment
In VS Code, create a `.venv` using Python 3.11.9.

### 2. Pull Ollama models
```bash
ollama pull phi3:mini
ollama pull nomic-embed-text
```

### 3. Build the vector database
Open `GameCodex.ipynb`, select the `.venv` kernel, and run all cells in order. This installs dependencies, loads the 10 rulebook PDFs from the `pdfs/` folder, and creates the `chroma_db/` vector database.

> ⚠️ The embedding step (Cell 6) may take a few minutes. Only needs to be run once.

### 4. Launch the app
```bash
streamlit run app.py
```

---

## Adding Custom Rulebooks
Drop additional PDFs into the `pdfs/` folder, delete `chroma_db/`, and re-run the notebook from Cell 3.

---

*Built by The Mickey Mavericks*
