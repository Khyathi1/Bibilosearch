import { useState, useCallback } from "react";
import "./App.css";

const API = "http://localhost:8000";

const GENRES = [
  "adventure","biography","children","classic","detective",
  "epic","fantasy","gothic","historical","horror","humor",
  "mythology","mystery","philosophy","poetry","political",
  "romance","satire","sci-fi","thriller","tragedy","war"
];

const LEVELS = ["beginner", "intermediate", "advanced"];

function BookCard({ book, index }) {
  const [expanded, setExpanded] = useState(false);
  const score = Math.round(book.score * 100);
  const year = book.year_published < 0
    ? `${Math.abs(book.year_published)} BC`
    : book.year_published;

  return (
    <div className="book-card" style={{ animationDelay: `${index * 50}ms` }}>
      <div className="book-spine" />
      <div className="book-body">
        <div className="book-header">
          <div className="book-meta">
            <h3 className="book-title">{book.book_title}</h3>
            <p className="book-author">by {book.author} · {year}</p>
          </div>
          <span className="book-score">{score}% match</span>
        </div>

        <div className="book-tags">
          {book.genre.map(g => <span key={g} className="tag">{g}</span>)}
          <span className="tag tag-level">{book.reading_level}</span>
        </div>

        <div className={`book-excerpt ${expanded ? "expanded" : ""}`}>
          <p>{book.chunk_text}</p>
        </div>

        <button className="expand-btn" onClick={() => setExpanded(e => !e)}>
          {expanded ? "▲ Hide passage" : "▼ Read passage"}
        </button>
      </div>
    </div>
  );
}

export default function App() {
  const [query, setQuery]       = useState("");
  const [results, setResults]   = useState([]);
  const [loading, setLoading]   = useState(false);
  const [searched, setSearched] = useState(false);
  const [error, setError]       = useState(null);
  const [filters, setFilters]   = useState({ genre: [] });

  const setFilter = (key, val) => setFilters(f => ({ ...f, [key]: val }));

  const toggleGenre = (g) => {
    setFilters(f => {
      const cur = f.genre || [];
      return { ...f, genre: cur.includes(g) ? cur.filter(x => x !== g) : [...cur, g] };
    });
  };

  const clearFilters = () => setFilters({ genre: [] });

  const search = useCallback(async (q = query) => {
    if (!q.trim()) return;
    setLoading(true);
    setError(null);
    setSearched(true);
    try {
      const res = await fetch(`${API}/search`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          query: q,
          genre:         filters.genre?.length ? filters.genre : undefined,
          reading_level: filters.reading_level || undefined,
          year_min:      filters.year_min ? parseInt(filters.year_min) : undefined,
          year_max:      filters.year_max ? parseInt(filters.year_max) : undefined,
          author:        filters.author || undefined,
          top_k: 10,
        }),
      });
      const data = await res.json();
      setResults(data.results || []);
    } catch {
      setError("Cannot reach the backend. Make sure it is running on port 8000.");
    } finally {
      setLoading(false);
    }
  }, [query, filters]);

  const activeFilterCount =
    (filters.genre?.length || 0) +
    (filters.reading_level ? 1 : 0) +
    (filters.year_min || filters.year_max ? 1 : 0) +
    (filters.author ? 1 : 0);

  return (
    <div className="app">

      {/* ── Top bar ── */}
      <header className="topbar">
        <div className="topbar-brand">
          <span className="brand-icon">📖</span>
          <span className="brand-name">Bibliosearch</span>
        </div>
        <div className="topbar-search">
          <input
            className="search-input"
            type="text"
            placeholder="Search by theme, scene, or feeling — e.g. a quest for revenge"
            value={query}
            onChange={e => setQuery(e.target.value)}
            onKeyDown={e => e.key === "Enter" && search()}
          />
          <button className="search-btn" onClick={() => search()} disabled={loading}>
            {loading ? "…" : "Search"}
          </button>
        </div>
      </header>

      {/* ── Body ── */}
      <div className="body">

        {/* ── Left: Filters ── */}
        <aside className="sidebar">
          <div className="sidebar-header">
            <span className="sidebar-title">Filters</span>
            {activeFilterCount > 0 && (
              <button className="clear-btn" onClick={clearFilters}>
                Clear {activeFilterCount}
              </button>
            )}
          </div>

          {/* Genre */}
          <div className="filter-group">
            <p className="filter-label">Genre</p>
            <div className="chip-grid">
              {GENRES.map(g => (
                <button
                  key={g}
                  className={`chip ${(filters.genre || []).includes(g) ? "chip-on" : ""}`}
                  onClick={() => toggleGenre(g)}
                >{g}</button>
              ))}
            </div>
          </div>

          {/* Reading level */}
          <div className="filter-group">
            <p className="filter-label">Reading Level</p>
            <div className="chip-grid">
              {LEVELS.map(l => (
                <button
                  key={l}
                  className={`chip ${filters.reading_level === l ? "chip-on" : ""}`}
                  onClick={() => setFilter("reading_level", filters.reading_level === l ? null : l)}
                >{l}</button>
              ))}
            </div>
          </div>

          {/* Year */}
          <div className="filter-group">
            <p className="filter-label">Year Published</p>
            <div className="year-row">
              <input
                className="year-input" type="number" placeholder="From"
                value={filters.year_min || ""}
                onChange={e => setFilter("year_min", e.target.value)}
              />
              <span className="year-dash">–</span>
              <input
                className="year-input" type="number" placeholder="To"
                value={filters.year_max || ""}
                onChange={e => setFilter("year_max", e.target.value)}
              />
            </div>
          </div>

          {/* Author */}
          <div className="filter-group">
            <p className="filter-label">Author</p>
            <input
              className="text-input" type="text" placeholder="e.g. Jules Verne"
              value={filters.author || ""}
              onChange={e => setFilter("author", e.target.value)}
            />
          </div>
        </aside>

        {/* ── Right: Results ── */}
        <main className="results-area">

          {/* Empty / welcome */}
          {!searched && !loading && (
            <div className="state-box">
              <div className="state-icon">🕯️</div>
              <p className="state-title">Find your next read</p>
              <p className="state-sub">Try <em>"forbidden love in a gothic castle"</em> or <em>"dragons and ancient prophecies"</em></p>
              <div className="suggestion-row">
                {["revenge and betrayal","sea monsters","detective solving a murder","man vs nature","political corruption","journey to the underworld"].map(s => (
                  <button key={s} className="sug-chip" onClick={() => { setQuery(s); search(s); }}>{s}</button>
                ))}
              </div>
            </div>
          )}

          {/* Loading */}
          {loading && (
            <div className="state-box">
              <div className="spinner" />
              <p className="state-sub">Searching 110 classics…</p>
            </div>
          )}

          {/* Error */}
          {error && <div className="error-banner">{error}</div>}

          {/* No results */}
          {!loading && searched && results.length === 0 && !error && (
            <div className="state-box">
              <div className="state-icon">🔍</div>
              <p className="state-title">No results found</p>
              <p className="state-sub">Try a broader query or remove some filters</p>
            </div>
          )}

          {/* Results */}
          {!loading && results.length > 0 && (
            <>
              <p className="results-meta">
                Showing <strong>{results.length}</strong> results for <em>"{query}"</em>
              </p>
              <div className="results-list">
                {results.map((book, i) => (
                  <BookCard key={book._id} book={book} index={i} />
                ))}
              </div>
            </>
          )}

        </main>
      </div>
    </div>
  );
}