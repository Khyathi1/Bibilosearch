<div align="center">

# 📖 Bibliosearch

**Semantic book search powered by RAG, MongoDB Atlas Vector Search, and local embeddings.**

Search 110 classic books by meaning, theme, or feeling — not just keywords.

[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=flat-square&logo=react&logoColor=black)](https://reactjs.org)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-47A248?style=flat-square&logo=mongodb&logoColor=white)](https://mongodb.com/atlas)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

</div>

---

## Overview

Bibliosearch is a full-stack RAG (Retrieval-Augmented Generation) application that lets users search through 110 public domain classics using natural language. Instead of matching keywords, it understands the *meaning* behind a query and returns the most semantically relevant passages and books.

| Query | Returns |
|---|---|
| *"a journey through the underworld"* | The Divine Comedy, The Odyssey, Beowulf |
| *"forbidden love and social class"* | Pride and Prejudice, Anna Karenina, Jane Eyre |
| *"sea monsters and ocean adventure"* | 20,000 Leagues, Moby Dick, The Odyssey |
| *"political power and corruption"* | The Prince, The Republic, Crime and Punishment |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        React Frontend                        │
│         Search Bar · Filter Panel · Book Result Cards        │
└───────────────────────────┬─────────────────────────────────┘
                            │ HTTP POST /search
┌───────────────────────────▼─────────────────────────────────┐
│                      FastAPI Backend                         │
│              search.py · main.py · CORS enabled              │
└───────────────────────────┬─────────────────────────────────┘
                            │
              ┌─────────────▼──────────────┐
              │   sentence-transformers     │
              │   all-MiniLM-L6-v2 (local) │
              │   384-dim embeddings        │
              └─────────────┬──────────────┘
                            │ cosine similarity
┌───────────────────────────▼─────────────────────────────────┐
│                  MongoDB Atlas Vector Search                  │
│         29,281 chunk embeddings · metadata filters           │
│         genre · year · reading level · author · language     │
└─────────────────────────────────────────────────────────────┘
```

---

## Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Frontend | React 18 | Search UI, filter panel, result cards |
| Backend | FastAPI + Uvicorn | REST API, query handling |
| Database | MongoDB Atlas M0 | Document storage + vector index |
| Vector Search | Atlas Vector Search | Cosine similarity over 384-dim embeddings |
| Embeddings | `all-MiniLM-L6-v2` | Local, free, no API key needed |
| Book Data | Project Gutenberg | 110 public domain books |

---

## Features

- **Semantic search** — understands meaning, not just keywords
- **29,281 indexed chunks** across 110 books
- **6 metadata filters** — genre, reading level, year range, author, language
- **Relevance scoring** — every result shows cosine similarity as a match percentage
- **Passage previews** — expandable excerpts showing the exact matching text
- **Zero embedding cost** — all embeddings generated locally, no OpenAI API needed
- **Free infrastructure** — runs entirely on MongoDB Atlas M0 free tier

---

## Project Structure

```
bibliosearch/
│
├── frontend/                        # React application
│   └── src/
│       ├── App.js                   # Main component — search, filters, results
│       └── App.css                  # Warm bookshop theme
│
└── backend/
    ├── main.py                      # FastAPI app — routes and CORS
    ├── search.py                    # Vector search + metadata filter logic
    ├── ingest.py                    # Ingestion pipeline: text → chunks → embeddings → MongoDB
    ├── .env                         # Environment variables (not committed)
    │
    ├── books/                       # 110 downloaded .txt files from Gutenberg
    │
    └── extractbooks/
        └── booksdownload.py         # Downloads all books from Project Gutenberg
```

---

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- A free [MongoDB Atlas](https://mongodb.com/atlas) account

---

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/bibliosearch.git
cd bibliosearch
```

---

### 2. Backend setup

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # Mac / Linux

# Install dependencies
pip install fastapi uvicorn pymongo sentence-transformers \
            pypdf langchain langchain-community python-dotenv
```

---

### 3. Configure MongoDB Atlas

1. Create a free **M0 cluster** at [mongodb.com/atlas](https://mongodb.com/atlas)
2. Under **Network Access** → add `0.0.0.0/0`
3. Under **Database Access** → create a user with **Atlas Admin** role
4. Click **Connect** → **Drivers** → copy the connection string

---

### 4. Set up your `.env` file

> ⚠️ **This file is not included in the repository.** Every person who clones this project must create their own `.env` file with their own MongoDB credentials. Never share or commit this file.

Create a file called `.env` inside the `backend/` folder:

```bash
# Windows
copy NUL backend\.env

# Mac / Linux
touch backend/.env
```

Open it and add your credentials:

```env
# backend/.env

# Your MongoDB Atlas connection string
# Get this from: Atlas Dashboard → Connect → Drivers
MONGODB_URI=mongodb+srv://<your_username>:<your_password>@cluster0.xxxxx.mongodb.net/bibliosearch?appName=Cluster0

# The database name (keep this as-is)
DB_NAME=bibliosearch
```

Replace:
- `<your_username>` — the database user you created in Atlas
- `<your_password>` — that user's password
- `cluster0.xxxxx` — your actual cluster hostname from Atlas

**Example of a real filled-in `.env`:**

```env
MONGODB_URI=mongodb+srv://john_doe:MySecurePass123@cluster0.ab1cd2.mongodb.net/bibliosearch?appName=Cluster0
DB_NAME=bibliosearch
```

> 🔒 The `.env` file is listed in `.gitignore` and will never be pushed to GitHub. Each developer needs their own MongoDB Atlas account and their own credentials.

---

### `.gitignore` — make sure `.env` is excluded

Check that your `backend/.gitignore` (or root `.gitignore`) contains:

```gitignore
# Environment variables — never commit this
.env

# Python
__pycache__/
*.pyc
venv/

# Books folder (large files)
backend/books/
```

---

### 5. Download books

```bash
python extractbooks/booksdownload.py
```

Downloads 110 public domain books from Project Gutenberg into `backend/books/`. Takes ~3 minutes.

---

### 6. Run the ingestion pipeline

```bash
python ingest.py
```

This will:
1. Read and clean all 110 `.txt` files (strips Gutenberg headers/footers)
2. Split each book into ~500-word overlapping chunks
3. Generate 384-dimensional embeddings locally using `all-MiniLM-L6-v2`
4. Upload all chunks with full metadata to MongoDB

> ⏱ Takes approximately 15–20 minutes. Uploads ~29,000 documents.

---

### 7. Create the Vector Search Index

In **MongoDB Atlas UI**:

1. Go to **Atlas Search** → **Create Search Index**
2. Select **Vector Search** → **Bring your own embeddings** → **JSON Editor**
3. Choose database `bibliosearch`, collection `books`
4. Set index name to `book_vector_index`
5. Paste the following definition:

```json
{
  "fields": [
    {
      "type": "vector",
      "path": "embedding",
      "numDimensions": 384,
      "similarity": "cosine"
    },
    { "type": "filter", "path": "genre" },
    { "type": "filter", "path": "year_published" },
    { "type": "filter", "path": "language" },
    { "type": "filter", "path": "reading_level" },
    { "type": "filter", "path": "author" }
  ]
}
```

6. Click **Create** and wait for status → **Active**

---

### 8. Start the backend

```bash
cd backend
python -m uvicorn main:app --reload --port 8000
```

- API: `http://localhost:8000`
- Interactive docs: `http://localhost:8000/docs`

---

### 9. Start the frontend

```bash
cd frontend
npm install
npm start
```

- App: `http://localhost:3000`

> Keep both terminals running simultaneously.

---

## API Reference

### `POST /search`

Search books by semantic query with optional metadata filters.

**Request body:**

```json
{
  "query": "revenge and betrayal",
  "genre": ["thriller", "classic"],
  "reading_level": "intermediate",
  "year_min": 1800,
  "year_max": 1920,
  "author": "Dumas",
  "top_k": 10
}
```

**Response:**

```json
{
  "query": "revenge and betrayal",
  "count": 10,
  "results": [
    {
      "book_title": "The Count of Monte Cristo",
      "author": "Alexandre Dumas",
      "genre": ["adventure", "thriller"],
      "year_published": 1844,
      "reading_level": "intermediate",
      "chunk_text": "...",
      "score": 0.847
    }
  ]
}
```

### `GET /filters`

Returns all valid filter values for the UI.

### `GET /`

Health check.

---

## MongoDB Document Schema

Each ingested chunk is stored as:

```json
{
  "_id":            "ObjectId",
  "book_title":     "Dracula",
  "author":         "Bram Stoker",
  "genre":          ["horror", "gothic"],
  "year_published": 1897,
  "language":       "English",
  "reading_level":  "intermediate",
  "chunk_index":    12,
  "chunk_text":     "The castle is on the very edge of a terrific precipice...",
  "embedding":      [0.023, -0.841, 0.204, ...]
}
```

---

## Book Collection

110 books across 12 genres, all public domain via Project Gutenberg:

| Genre | Count | Notable Titles |
|---|---|---|
| Horror & Gothic | 10 | Dracula, Frankenstein, Carmilla, Lovecraft |
| Sci-Fi | 12 | H.G. Wells × 5, Jules Verne × 3, Burroughs × 3 |
| Adventure | 12 | Treasure Island, Monte Cristo, Three Musketeers |
| Mystery & Detective | 10 | Sherlock Holmes × 4, Wilkie Collins × 2 |
| Romance & Classic | 12 | Jane Austen × 4, Brontë sisters, Tolstoy |
| Mythology & Epic | 6 | Homer, Virgil, Ovid, Dante, Beowulf |
| Philosophy | 10 | Dostoevsky × 4, Nietzsche × 2, Plato |
| Fantasy & Children | 8 | Lewis Carroll, Baum, Barrie, Kipling |
| Historical Fiction | 8 | Dickens × 4, Victor Hugo, Walter Scott |
| Satire & Humor | 6 | Mark Twain, Swift, Voltaire, Chesterton |
| War & Political | 6 | Sun Tzu, Machiavelli, Plato, Marx |
| Poetry & Stories | 10 | Poe, Whitman, Grimm, Andersen, Arabian Nights |

---

## How RAG Works Here

```
1. INGESTION (one-time)
   Book text → clean → split into 500-word chunks
   → embed each chunk (all-MiniLM-L6-v2, 384 dims)
   → store { text, embedding, metadata } in MongoDB

2. QUERY (real-time)
   User types "dragons and ancient prophecies"
   → embed query with same model
   → cosine similarity search over 29,281 embeddings
   → apply metadata filters (genre, year, etc.)
   → deduplicate: one result per book (best chunk wins)
   → return top 10 with relevance scores
```

---

## Roadmap

- [ ] Book cover images from Open Library API
- [ ] Save and export favourite results
- [ ] "More like this" — similar book recommendations
- [ ] Full book detail page with chapter navigation
- [ ] Deploy frontend to Vercel
- [ ] Deploy backend to Railway or Render

---

## License

All books are public domain, sourced from [Project Gutenberg](https://gutenberg.org).

Application code is licensed under the [MIT License](LICENSE).



