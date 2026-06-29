import os
import re
import time
from pathlib import Path
from dotenv import load_dotenv
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer

# ── Load environment ───────────────────────────────────────────
load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME     = os.getenv("DB_NAME", "bibliosearch")

# ── Connect to MongoDB ─────────────────────────────────────────
client     = MongoClient(MONGODB_URI)
db         = client[DB_NAME]
collection = db["books"]

# ── Load embedding model (downloads once, ~90MB) ───────────────
print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("Model ready.\n")

# ── Book metadata (matches your 110 downloaded books) ──────────
BOOK_METADATA = {
    "Dracula":                                  {"author": "Bram Stoker",               "genre": ["horror", "gothic"],                  "year": 1897, "reading_level": "intermediate"},
    "Frankenstein":                             {"author": "Mary Shelley",              "genre": ["horror", "sci-fi"],                  "year": 1818, "reading_level": "intermediate"},
    "The Strange Case of Dr Jekyll and Mr Hyde":{"author": "Robert Louis Stevenson",    "genre": ["horror", "thriller"],                "year": 1886, "reading_level": "intermediate"},
    "The Picture of Dorian Gray":               {"author": "Oscar Wilde",               "genre": ["horror", "gothic", "classic"],        "year": 1890, "reading_level": "intermediate"},
    "The Dunwich Horror":                       {"author": "H.P. Lovecraft",            "genre": ["horror", "gothic"],                  "year": 1929, "reading_level": "advanced"},
    "The Call of Cthulhu":                      {"author": "H.P. Lovecraft",            "genre": ["horror", "gothic"],                  "year": 1928, "reading_level": "advanced"},
    "The Turn of the Screw":                    {"author": "Henry James",               "genre": ["horror", "gothic"],                  "year": 1898, "reading_level": "advanced"},
    "Ghost Stories of an Antiquary":            {"author": "M.R. James",               "genre": ["horror", "gothic"],                  "year": 1904, "reading_level": "intermediate"},
    "The Monk":                                 {"author": "Matthew Gregory Lewis",     "genre": ["horror", "gothic"],                  "year": 1796, "reading_level": "advanced"},
    "Carmilla":                                 {"author": "J. Sheridan Le Fanu",       "genre": ["horror", "gothic"],                  "year": 1872, "reading_level": "intermediate"},
    "The Time Machine":                         {"author": "H.G. Wells",               "genre": ["sci-fi"],                            "year": 1895, "reading_level": "intermediate"},
    "The War of the Worlds":                    {"author": "H.G. Wells",               "genre": ["sci-fi", "adventure"],               "year": 1898, "reading_level": "intermediate"},
    "The Invisible Man":                        {"author": "H.G. Wells",               "genre": ["sci-fi", "thriller"],                "year": 1897, "reading_level": "intermediate"},
    "The Island of Doctor Moreau":              {"author": "H.G. Wells",               "genre": ["sci-fi", "horror"],                  "year": 1896, "reading_level": "intermediate"},
    "The First Men in the Moon":                {"author": "H.G. Wells",               "genre": ["sci-fi", "adventure"],               "year": 1901, "reading_level": "intermediate"},
    "Twenty Thousand Leagues Under the Sea":    {"author": "Jules Verne",              "genre": ["sci-fi", "adventure"],               "year": 1870, "reading_level": "intermediate"},
    "From the Earth to the Moon":               {"author": "Jules Verne",              "genre": ["sci-fi", "adventure"],               "year": 1865, "reading_level": "intermediate"},
    "The Land That Time Forgot":                {"author": "Edgar Rice Burroughs",     "genre": ["sci-fi", "adventure"],               "year": 1918, "reading_level": "intermediate"},
    "A Princess of Mars":                       {"author": "Edgar Rice Burroughs",     "genre": ["sci-fi", "fantasy", "adventure"],    "year": 1912, "reading_level": "intermediate"},
    "The Sleeper Awakes":                       {"author": "H.G. Wells",               "genre": ["sci-fi"],                            "year": 1910, "reading_level": "intermediate"},
    "Thuvia Maid of Mars":                      {"author": "Edgar Rice Burroughs",     "genre": ["sci-fi", "fantasy"],                 "year": 1916, "reading_level": "intermediate"},
    "Treasure Island":                          {"author": "Robert Louis Stevenson",   "genre": ["adventure"],                         "year": 1883, "reading_level": "beginner"},
    "Moby Dick":                                {"author": "Herman Melville",          "genre": ["adventure", "classic"],              "year": 1851, "reading_level": "advanced"},
    "Robinson Crusoe":                          {"author": "Daniel Defoe",             "genre": ["adventure", "classic"],              "year": 1719, "reading_level": "intermediate"},
    "The Count of Monte Cristo":                {"author": "Alexandre Dumas",          "genre": ["adventure", "thriller"],             "year": 1844, "reading_level": "intermediate"},
    "Around the World in 80 Days":              {"author": "Jules Verne",              "genre": ["adventure"],                         "year": 1872, "reading_level": "beginner"},
    "The Three Musketeers":                     {"author": "Alexandre Dumas",          "genre": ["adventure", "thriller", "classic"],  "year": 1844, "reading_level": "intermediate"},
    "Twenty Years After":                       {"author": "Alexandre Dumas",          "genre": ["adventure", "thriller"],             "year": 1845, "reading_level": "intermediate"},
    "The Scarlet Pimpernel":                    {"author": "Baroness Orczy",           "genre": ["thriller", "adventure"],             "year": 1905, "reading_level": "intermediate"},
    "King Solomons Mines":                      {"author": "H. Rider Haggard",         "genre": ["adventure"],                         "year": 1885, "reading_level": "intermediate"},
    "She":                                      {"author": "H. Rider Haggard",         "genre": ["adventure", "fantasy"],              "year": 1887, "reading_level": "intermediate"},
    "The Prisoner of Zenda":                    {"author": "Anthony Hope",             "genre": ["adventure", "thriller"],             "year": 1894, "reading_level": "intermediate"},
    "Kidnapped":                                {"author": "Robert Louis Stevenson",   "genre": ["adventure", "classic"],              "year": 1886, "reading_level": "intermediate"},
    "The Adventures of Sherlock Holmes":        {"author": "Arthur Conan Doyle",       "genre": ["mystery", "detective"],              "year": 1892, "reading_level": "intermediate"},
    "The Hound of the Baskervilles":            {"author": "Arthur Conan Doyle",       "genre": ["mystery", "detective"],              "year": 1902, "reading_level": "intermediate"},
    "The Memoirs of Sherlock Holmes":           {"author": "Arthur Conan Doyle",       "genre": ["mystery", "detective"],              "year": 1894, "reading_level": "intermediate"},
    "The Return of Sherlock Holmes":            {"author": "Arthur Conan Doyle",       "genre": ["mystery", "detective"],              "year": 1905, "reading_level": "intermediate"},
    "The Moonstone":                            {"author": "Wilkie Collins",           "genre": ["mystery", "detective"],              "year": 1868, "reading_level": "advanced"},
    "The Woman in White":                       {"author": "Wilkie Collins",           "genre": ["mystery", "thriller"],               "year": 1859, "reading_level": "advanced"},
    "The Casebook of Sherlock Holmes":          {"author": "Arthur Conan Doyle",       "genre": ["mystery", "detective"],              "year": 1927, "reading_level": "intermediate"},
    "Pride and Prejudice":                      {"author": "Jane Austen",              "genre": ["romance", "classic"],                "year": 1813, "reading_level": "intermediate"},
    "Sense and Sensibility":                    {"author": "Jane Austen",              "genre": ["romance", "classic"],                "year": 1811, "reading_level": "intermediate"},
    "Emma":                                     {"author": "Jane Austen",              "genre": ["romance", "classic"],                "year": 1815, "reading_level": "intermediate"},
    "Persuasion":                               {"author": "Jane Austen",              "genre": ["romance", "classic"],                "year": 1818, "reading_level": "intermediate"},
    "Jane Eyre":                                {"author": "Charlotte Bronte",         "genre": ["romance", "classic"],                "year": 1847, "reading_level": "intermediate"},
    "Wuthering Heights":                        {"author": "Emily Bronte",             "genre": ["romance", "gothic", "classic"],      "year": 1847, "reading_level": "intermediate"},
    "Anna Karenina":                            {"author": "Leo Tolstoy",              "genre": ["romance", "classic"],                "year": 1878, "reading_level": "advanced"},
    "Northanger Abbey":                         {"author": "Jane Austen",              "genre": ["romance", "satire", "classic"],      "year": 1817, "reading_level": "intermediate"},
    "Tess of the dUrbervilles":                 {"author": "Thomas Hardy",             "genre": ["romance", "classic", "tragedy"],     "year": 1891, "reading_level": "advanced"},
    "Far from the Madding Crowd":               {"author": "Thomas Hardy",             "genre": ["romance", "classic"],                "year": 1874, "reading_level": "advanced"},
    "The Sorrows of Young Werther":             {"author": "Johann Wolfgang von Goethe","genre": ["romance", "classic", "philosophy"], "year": 1774, "reading_level": "intermediate"},
    "The Odyssey":                              {"author": "Homer",                    "genre": ["mythology", "epic", "fantasy"],      "year": -800, "reading_level": "advanced"},
    "The Iliad":                                {"author": "Homer",                    "genre": ["mythology", "epic", "war"],          "year": -750, "reading_level": "advanced"},
    "Beowulf":                                  {"author": "Unknown",                  "genre": ["fantasy", "epic", "mythology"],      "year": 1000, "reading_level": "advanced"},
    "The Divine Comedy":                        {"author": "Dante Alighieri",          "genre": ["epic", "mythology", "classic"],      "year": 1320, "reading_level": "advanced"},
    "Metamorphoses":                            {"author": "Ovid",                     "genre": ["mythology", "epic", "classic"],      "year": 8,    "reading_level": "advanced"},
    "The Aeneid":                               {"author": "Virgil",                   "genre": ["mythology", "epic", "war"],          "year": -19,  "reading_level": "advanced"},
    "Crime and Punishment":                     {"author": "Fyodor Dostoevsky",        "genre": ["classic", "thriller", "philosophy"], "year": 1866, "reading_level": "advanced"},
    "The Brothers Karamazov":                   {"author": "Fyodor Dostoevsky",        "genre": ["classic", "philosophy"],             "year": 1880, "reading_level": "advanced"},
    "Notes from the Underground":               {"author": "Fyodor Dostoevsky",        "genre": ["philosophy", "classic"],             "year": 1864, "reading_level": "advanced"},
    "Don Quixote":                              {"author": "Miguel de Cervantes",      "genre": ["classic", "adventure", "satire"],    "year": 1605, "reading_level": "advanced"},
    "Les Miserables":                           {"author": "Victor Hugo",              "genre": ["classic", "historical"],             "year": 1862, "reading_level": "advanced"},
    "War and Peace":                            {"author": "Leo Tolstoy",              "genre": ["classic", "war", "historical"],      "year": 1869, "reading_level": "advanced"},
    "The Idiot":                                {"author": "Fyodor Dostoevsky",        "genre": ["classic", "philosophy"],             "year": 1869, "reading_level": "advanced"},
    "Thus Spoke Zarathustra":                   {"author": "Friedrich Nietzsche",      "genre": ["philosophy"],                        "year": 1883, "reading_level": "advanced"},
    "Alice in Wonderland":                      {"author": "Lewis Carroll",            "genre": ["fantasy", "children", "classic"],    "year": 1865, "reading_level": "beginner"},
    "Through the Looking Glass":                {"author": "Lewis Carroll",            "genre": ["fantasy", "children", "classic"],    "year": 1871, "reading_level": "beginner"},
    "The Wonderful Wizard of Oz":               {"author": "L. Frank Baum",            "genre": ["fantasy", "children"],               "year": 1900, "reading_level": "beginner"},
    "Peter Pan":                                {"author": "J.M. Barrie",             "genre": ["fantasy", "children", "classic"],    "year": 1911, "reading_level": "beginner"},
    "The Wind in the Willows":                  {"author": "Kenneth Grahame",          "genre": ["fantasy", "children", "classic"],    "year": 1908, "reading_level": "beginner"},
    "The Jungle Book":                          {"author": "Rudyard Kipling",          "genre": ["fantasy", "children", "adventure"],  "year": 1894, "reading_level": "beginner"},
    "The Blue Fairy Book":                      {"author": "Andrew Lang",              "genre": ["fantasy", "children", "mythology"],  "year": 1889, "reading_level": "beginner"},
    "A Tale of Two Cities":                     {"author": "Charles Dickens",          "genre": ["historical", "classic", "thriller"], "year": 1859, "reading_level": "intermediate"},
    "Oliver Twist":                             {"author": "Charles Dickens",          "genre": ["historical", "classic"],             "year": 1837, "reading_level": "intermediate"},
    "Great Expectations":                       {"author": "Charles Dickens",          "genre": ["historical", "classic"],             "year": 1861, "reading_level": "intermediate"},
    "David Copperfield":                        {"author": "Charles Dickens",          "genre": ["historical", "classic"],             "year": 1850, "reading_level": "intermediate"},
    "Ivanhoe":                                  {"author": "Walter Scott",             "genre": ["historical", "adventure"],           "year": 1820, "reading_level": "advanced"},
    "The Scarlet Letter":                       {"author": "Nathaniel Hawthorne",      "genre": ["historical", "classic", "romance"],  "year": 1850, "reading_level": "advanced"},
    "Ben-Hur A Tale of the Christ":             {"author": "Lew Wallace",              "genre": ["historical", "adventure", "classic"],"year": 1880, "reading_level": "intermediate"},
    "Quo Vadis":                                {"author": "Henryk Sienkiewicz",       "genre": ["historical", "romance", "adventure"],"year": 1896, "reading_level": "intermediate"},
    "Adventures of Huckleberry Finn":           {"author": "Mark Twain",               "genre": ["satire", "adventure", "classic"],    "year": 1884, "reading_level": "intermediate"},
    "The Adventures of Tom Sawyer":             {"author": "Mark Twain",               "genre": ["satire", "adventure", "children"],   "year": 1876, "reading_level": "beginner"},
    "Gullivers Travels":                        {"author": "Jonathan Swift",           "genre": ["satire", "fantasy", "classic"],      "year": 1726, "reading_level": "intermediate"},
    "The Man Who Was Thursday":                 {"author": "G.K. Chesterton",          "genre": ["satire", "thriller", "philosophy"],  "year": 1908, "reading_level": "intermediate"},
    "Three Men in a Boat":                      {"author": "Jerome K. Jerome",         "genre": ["satire", "humor", "adventure"],      "year": 1889, "reading_level": "beginner"},
    "The Art of War":                           {"author": "Sun Tzu",                  "genre": ["war", "philosophy", "classic"],      "year": -500, "reading_level": "intermediate"},
    "The Prince":                               {"author": "Niccolo Machiavelli",      "genre": ["philosophy", "political", "classic"],"year": 1532, "reading_level": "advanced"},
    "The Republic":                             {"author": "Plato",                    "genre": ["philosophy", "political", "classic"],"year": -380, "reading_level": "advanced"},
    "Leviathan":                                {"author": "Thomas Hobbes",            "genre": ["philosophy", "political"],           "year": 1651, "reading_level": "advanced"},
    "Common Sense":                             {"author": "Thomas Paine",             "genre": ["political", "philosophy", "classic"],"year": 1776, "reading_level": "intermediate"},
    "The Communist Manifesto":                  {"author": "Karl Marx",                "genre": ["political", "philosophy"],           "year": 1848, "reading_level": "advanced"},
    "The Complete Poetical Works of Edgar Allan Poe": {"author": "Edgar Allan Poe",   "genre": ["horror", "poetry", "gothic"],        "year": 1849, "reading_level": "intermediate"},
    "The Works of Edgar Allan Poe Vol 1":       {"author": "Edgar Allan Poe",          "genre": ["horror", "mystery", "gothic"],       "year": 1840, "reading_level": "intermediate"},
    "Fairy Tales by Hans Christian Andersen":   {"author": "Hans Christian Andersen",  "genre": ["fantasy", "children", "classic"],    "year": 1835, "reading_level": "beginner"},
    "Grimms Fairy Tales":                       {"author": "Brothers Grimm",           "genre": ["fantasy", "children", "mythology"],  "year": 1812, "reading_level": "beginner"},
    "Aesops Fables":                            {"author": "Aesop",                    "genre": ["classic", "children", "mythology"],  "year": -600, "reading_level": "beginner"},
    "Leaves of Grass":                          {"author": "Walt Whitman",             "genre": ["poetry", "classic"],                 "year": 1855, "reading_level": "intermediate"},
    "The Arabian Nights":                       {"author": "Anonymous",                "genre": ["fantasy", "mythology", "classic"],   "year": 1706, "reading_level": "intermediate"},
    "Narrative of the Life of Frederick Douglass": {"author": "Frederick Douglass",   "genre": ["biography", "historical", "classic"],"year": 1845, "reading_level": "intermediate"},
    "The Souls of Black Folk":                  {"author": "W.E.B. Du Bois",           "genre": ["biography", "philosophy", "historical"],"year": 1903,"reading_level": "advanced"},
    "The Lost World":                           {"author": "Arthur Conan Doyle",       "genre": ["sci-fi", "adventure"],               "year": 1912, "reading_level": "intermediate"},
    "Heart of Darkness":                        {"author": "Joseph Conrad",            "genre": ["classic", "adventure", "philosophy"],"year": 1899, "reading_level": "advanced"},
    "The Secret Garden":                        {"author": "Frances Hodgson Burnett",  "genre": ["children", "classic"],               "year": 1911, "reading_level": "beginner"},
    "Little Women":                             {"author": "Louisa May Alcott",        "genre": ["romance", "classic", "children"],    "year": 1868, "reading_level": "beginner"},
    "The Call of the Wild":                     {"author": "Jack London",              "genre": ["adventure", "classic"],              "year": 1903, "reading_level": "beginner"},
    "White Fang":                               {"author": "Jack London",              "genre": ["adventure", "classic"],              "year": 1906, "reading_level": "intermediate"},
    "The Jungle":                               {"author": "Upton Sinclair",           "genre": ["historical", "classic", "political"],"year": 1906, "reading_level": "intermediate"},
    "Ethan Frome":                              {"author": "Edith Wharton",            "genre": ["classic", "romance", "tragedy"],     "year": 1911, "reading_level": "intermediate"},
}

# ── Helper: clean Gutenberg header/footer ──────────────────────
def clean_gutenberg_text(text):
    # Remove header
    start_markers = [
        "*** START OF THE PROJECT GUTENBERG",
        "***START OF THE PROJECT GUTENBERG",
        "*** START OF THIS PROJECT GUTENBERG",
    ]
    for marker in start_markers:
        idx = text.find(marker)
        if idx != -1:
            text = text[idx:]
            text = text[text.find("\n") + 1:]
            break

    # Remove footer
    end_markers = [
        "*** END OF THE PROJECT GUTENBERG",
        "***END OF THE PROJECT GUTENBERG",
        "*** END OF THIS PROJECT GUTENBERG",
    ]
    for marker in end_markers:
        idx = text.find(marker)
        if idx != -1:
            text = text[:idx]
            break

    return text.strip()

# ── Helper: split text into chunks ────────────────────────────
def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    start  = 0
    while start < len(words):
        end   = min(start + chunk_size, len(words))
        chunk = " ".join(words[start:end])
        if len(chunk.strip()) > 100:   # skip tiny chunks
            chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

# ── Helper: derive title from filename ────────────────────────
def filename_to_title(filename):
    return filename.replace(".txt", "").replace("_", " ")

# ── Main ingestion ─────────────────────────────────────────────
def ingest_all():
    books_dir = Path(__file__).parent / "books"
    txt_files = list(books_dir.glob("*.txt"))

    if not txt_files:
        print("❌ No .txt files found in books/ folder!")
        return

    print(f"📚 Found {len(txt_files)} books to ingest\n")

    # Drop existing collection to start fresh
    collection.drop()
    print("🗑️  Cleared existing collection\n")

    total_chunks = 0

    for i, filepath in enumerate(txt_files, 1):
        title = filename_to_title(filepath.name)
        meta  = BOOK_METADATA.get(title, {
            "author":        "Unknown",
            "genre":         ["classic"],
            "year":          1900,
            "reading_level": "intermediate",
        })

        print(f"[{i:03d}/{len(txt_files)}] {title}")

        # Read & clean
        try:
            raw  = filepath.read_text(encoding="utf-8", errors="ignore")
            text = clean_gutenberg_text(raw)
        except Exception as e:
            print(f"  ❌ Read error: {e}")
            continue

        # Chunk
        chunks = chunk_text(text)
        print(f"  → {len(chunks)} chunks", end=" ", flush=True)

        # Embed all chunks at once (batch = faster)
        try:
            embeddings = model.encode(
                chunks,
                batch_size=32,
                show_progress_bar=False
            )
        except Exception as e:
            print(f"\n  ❌ Embedding error: {e}")
            continue

        # Build MongoDB documents
        docs = []
        for j, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            docs.append({
                "book_title":    title,
                "author":        meta["author"],
                "genre":         meta["genre"],
                "year_published": meta["year"],
                "language":      "English",
                "reading_level": meta["reading_level"],
                "chunk_index":   j,
                "chunk_text":    chunk,
                "embedding":     embedding.tolist(),
            })

        # Insert into MongoDB
        try:
            collection.insert_many(docs, ordered=False)
            total_chunks += len(docs)
            print(f"✅ uploaded")
        except Exception as e:
            print(f"\n  ❌ Insert error: {e}")

    print(f"\n{'='*55}")
    print(f"✅  Done! {total_chunks:,} total chunks across {len(txt_files)} books")
    print(f"📦  Collection: {DB_NAME}.books")
   

if __name__ == "__main__":
    ingest_all()