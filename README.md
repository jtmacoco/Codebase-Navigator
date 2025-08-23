# Codebase-Navigator
> An AI web app that helps you explore, search, and understand github codebaes using a RAG pipeline

## Features
- Semantic search (dense vector search using Pinecone) across repositories 
- RAG for context-aware Q&A about code
- Per-repo Pinecone indexing for fast retrieval

## Tech Stack
- Frontend: Next.js, Tailwind
- Backend: FastAPI 
- Vector DB: Pinecone
- Embedding: Hugginface

## Instilation 

1. Clone Repo
```bash
git clone git@github.com:jtmacoco/Codebase-Navigator.git
cd Codebase-Navigator
```
2. Start backend
```bash
cd backend
pip install -r requirements.txt
python server.py
```
3. Start Frontend
```bash
cd frontend
npm install
npm run dev
```

