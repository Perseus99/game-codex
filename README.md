# 🎲 The Game Codex

The Game Codex is a fully local Retrieval-Augmented Generation (RAG) system that answers board game rule questions using official rulebooks.

Instead of flipping through rulebooks mid-game, users can ask questions in natural language and get instant, grounded answers.

---

## 🚀 Features

- Supports 10 board games out of the box  
- Fully local — no APIs or cloud dependencies  
- Answers grounded in rulebooks using RAG  
- Per-game filtering to prevent cross-game confusion  
- Conversational chat with short-term memory  
- Fast retrieval using Max Marginal Relevance (MMR)  

---

## 🎮 Supported Games

- UNO  
- Monopoly  
- Monopoly Deal  
- Catan  
- Root  
- Betrayal at House on the Hill  
- Sushi Go!  
- Pandemic  
- Ticket to Ride  
- Risk  

---

## 🧠 How It Works

- Rulebook PDFs are loaded  
- Text is split into chunks  
- Chunks are converted into embeddings  
- Stored in ChromaDB  
- Relevant chunks are retrieved using MMR  
- A local LLM generates the final answer  

At query time:
- Only the selected game's rules are searched  
- Recent chat history is included for context  
- The response is generated conversationally  

---

## 🧱 Tech Stack

- Streamlit — UI  
- LangChain — orchestration  
- ChromaDB — vector database  
- Ollama — local LLM runtime  
- phi3:mini — chat model  
- nomic-embed-text — embeddings  

---

## ⚙️ Setup Instructions

- Clone the repository:

    git clone https://github.com/YOUR_USERNAME/game-codex.git  
    cd game-codex  

- Create a virtual environment:

    python -m venv .venv  
    .\.venv\Scripts\activate  

- Install dependencies:

    pip install -r requirements.txt  

- Install Ollama:  
  https://ollama.com/download  

- Pull required models:

    ollama pull phi3:mini  
    ollama pull nomic-embed-text  

- Create a `pdfs/` folder and add rulebooks:

    pdfs/  
        uno_official.pdf  
        monopoly_official.pdf  
        catan_official.pdf  

- Build the vector database:

    python scripts/build_chroma.py  

- Run the app:

    streamlit run app.py  

---

## 💬 Example Queries

- Can you stack Draw 2 in UNO?  
- What happens if you land on a mortgaged property in Monopoly?  
- How does the robber work in Catan?  

---

## 📁 Project Structure

    game-codex/
    │
    ├── app.py
    ├── README.md
    ├── requirements.txt
    ├── .gitignore
    │
    ├── scripts/
    │   └── build_chroma.py
    │
    ├── pdfs/
    └── chroma_db/

---

## 📌 Notes

- Runs completely offline after setup  
- `chroma_db/` is not included in the repo and must be built locally  
- Add new games by placing PDFs in `pdfs/` and rebuilding  

---

## 👨‍💻 Authors

Perseus99