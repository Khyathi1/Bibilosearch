import os
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME     = os.getenv("DB_NAME", "bibliosearch")

client     = MongoClient(MONGODB_URI)
collection = client[DB_NAME]["books"]

print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("Model ready.")

def search_books(query: str, filters: dict = {}, top_k: int = 10):
    query_embedding = model.encode(query).tolist()

    # ── Build metadata filter ──────────────────────────────────
    meta_filter = {}

    if filters.get("genre"):
        meta_filter["genre"] = {"$in": filters["genre"]}

    if filters.get("reading_level"):
        meta_filter["reading_level"] = filters["reading_level"]

    if filters.get("language"):
        meta_filter["language"] = filters["language"]

    if filters.get("year_min") or filters.get("year_max"):
        meta_filter["year_published"] = {}
        if filters.get("year_min"):
            meta_filter["year_published"]["$gte"] = int(filters["year_min"])
        if filters.get("year_max"):
            meta_filter["year_published"]["$lte"] = int(filters["year_max"])

    if filters.get("author"):
        meta_filter["author"] = {"$regex": filters["author"], "$options": "i"}

    # ── Build pipeline ────────────────────────────────────────
    vector_search = {
        "$vectorSearch": {
            "index":       "book_vector_index",
            "path":        "embedding",
            "queryVector": query_embedding,
            "numCandidates": 200,
            "limit":       top_k * 3,  # fetch more, deduplicate by book below
        }
    }

    if meta_filter:
        vector_search["$vectorSearch"]["filter"] = meta_filter

    pipeline = [
        vector_search,
        {
            "$project": {
                "book_title":    1,
                "author":        1,
                "genre":         1,
                "year_published":1,
                "language":      1,
                "reading_level": 1,
                "chunk_text":    1,
                "score": {"$meta": "vectorSearchScore"},
            }
        }
    ]

    results = list(collection.aggregate(pipeline))

    # ── Deduplicate: one result per book, best chunk wins ──────
    seen   = {}
    unique = []
    for r in results:
        title = r["book_title"]
        if title not in seen:
            seen[title] = True
            r["_id"] = str(r["_id"])
            unique.append(r)
        if len(unique) >= top_k:
            break

    return unique