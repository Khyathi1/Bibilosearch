import requests
import os
import time

# 8 replacement books with rock-solid Gutenberg URLs
REPLACEMENT_BOOKS = [
    {
        "title": "The Lost World", "author": "Arthur Conan Doyle",
        "genre": ["sci-fi", "adventure"], "year": 1912,
        "language": "English", "reading_level": "intermediate",
        "url": "https://www.gutenberg.org/files/139/139-0.txt"
    },
    {
        "title": "Heart of Darkness", "author": "Joseph Conrad",
        "genre": ["classic", "adventure", "philosophy"], "year": 1899,
        "language": "English", "reading_level": "advanced",
        "url": "https://www.gutenberg.org/files/219/219-0.txt"
    },
    {
        "title": "The Secret Garden", "author": "Frances Hodgson Burnett",
        "genre": ["children", "classic"], "year": 1911,
        "language": "English", "reading_level": "beginner",
        "url": "https://www.gutenberg.org/files/113/113-0.txt"
    },
    {
        "title": "Little Women", "author": "Louisa May Alcott",
        "genre": ["romance", "classic", "children"], "year": 1868,
        "language": "English", "reading_level": "beginner",
        "url": "https://www.gutenberg.org/files/514/514-0.txt"
    },
    {
        "title": "The Call of the Wild", "author": "Jack London",
        "genre": ["adventure", "classic"], "year": 1903,
        "language": "English", "reading_level": "beginner",
        "url": "https://www.gutenberg.org/files/215/215-0.txt"
    },
    {
        "title": "White Fang", "author": "Jack London",
        "genre": ["adventure", "classic"], "year": 1906,
        "language": "English", "reading_level": "intermediate",
        "url": "https://www.gutenberg.org/files/910/910-0.txt"
    },
    {
        "title": "The Jungle", "author": "Upton Sinclair",
        "genre": ["historical", "classic", "political"], "year": 1906,
        "language": "English", "reading_level": "intermediate",
        "url": "https://www.gutenberg.org/files/140/140-0.txt"
    },
    {
        "title": "Ethan Frome", "author": "Edith Wharton",
        "genre": ["classic", "romance", "tragedy"], "year": 1911,
        "language": "English", "reading_level": "intermediate",
        "url": "https://www.gutenberg.org/files/4517/4517-0.txt"
    },
]

SAVE_DIR = os.path.join(os.path.dirname(__file__), "..", "books")
os.makedirs(SAVE_DIR, exist_ok=True)

def download_replacements():
    total = len(REPLACEMENT_BOOKS)
    print(f"📚 Downloading {total} replacement books...\n")
    success, failed = 0, []

    for i, book in enumerate(REPLACEMENT_BOOKS, 1):
        safe_name = (book["title"]
                     .replace(" ", "_")
                     .replace("/", "_")
                     .replace(":", "")
                     .replace("'", "")
                     .replace(",", "")) + ".txt"
        filepath = os.path.join(SAVE_DIR, safe_name)

        if os.path.exists(filepath):
            print(f"[{i:02d}/{total}] SKIP  ── {book['title']} already exists")
            success += 1
            continue

        print(f"[{i:02d}/{total}] GET   ── {book['title']} ...", end=" ", flush=True)
        try:
            r = requests.get(book["url"], timeout=30)
            r.raise_for_status()
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(r.text)
            kb = os.path.getsize(filepath) // 1024
            print(f"✅ {kb} KB")
            success += 1
            time.sleep(0.3)
        except Exception as e:
            print(f"❌ {e}")
            failed.append(book["title"])

    print(f"\n{'='*50}")
    print(f"✅  Success : {success}/{total}")
    if failed:
        print(f"❌  Failed  : {', '.join(failed)}")
    else:
        print(f"🎉  All replacement books downloaded!")
    print(f"📁  Saved to: {os.path.abspath(SAVE_DIR)}")

if __name__ == "__main__":
    download_replacements()