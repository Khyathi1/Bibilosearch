from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from search import search_books

app = FastAPI(title="Bibliosearch API")

# ── Allow React frontend to call this API ──────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Request model ──────────────────────────────────────────────
class SearchRequest(BaseModel):
    query:         str
    genre:         Optional[List[str]] = []
    reading_level: Optional[str]       = None
    language:      Optional[str]       = None
    year_min:      Optional[int]       = None
    year_max:      Optional[int]       = None
    author:        Optional[str]       = None
    top_k:         Optional[int]       = 10

# ── Routes ─────────────────────────────────────────────────────
@app.get("/")
def root():
    return {"status": "Bibliosearch API is running"}

@app.post("/search")
def search(req: SearchRequest):
    filters = {
        "genre":         req.genre,
        "reading_level": req.reading_level,
        "language":      req.language,
        "year_min":      req.year_min,
        "year_max":      req.year_max,
        "author":        req.author,
    }
    results = search_books(req.query, filters, req.top_k)
    return {"query": req.query, "results": results, "count": len(results)}

@app.get("/genres")
def get_genres():
    return {"genres": [
        "adventure", "biography", "children", "classic",
        "detective", "epic", "fantasy", "gothic", "historical",
        "horror", "humor", "mythology", "mystery", "philosophy",
        "poetry", "political", "romance", "satire", "sci-fi",
        "thriller", "tragedy", "war"
    ]}

@app.get("/filters")
def get_filters():
    return {
        "genres": [
            "adventure", "biography", "children", "classic",
            "detective", "epic", "fantasy", "gothic", "historical",
            "horror", "humor", "mythology", "mystery", "philosophy",
            "poetry", "political", "romance", "satire", "sci-fi",
            "thriller", "tragedy", "war"
        ],
        "reading_levels": ["beginner", "intermediate", "advanced"],
        "languages":      ["English"],
        "year_range":     {"min": -800, "max": 1927}
    }