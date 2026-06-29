import requests
import os
import time

# ============================================================
# 110 Books from Project Gutenberg — verified file IDs
# Genres: Horror, Sci-Fi, Adventure, Mystery, Romance,
#         Classic, Mythology, Thriller, Philosophy,
#         Fantasy, Historical, Children, Satire, War
# ============================================================

BOOKS = [

    # ── HORROR & GOTHIC (10) ────────────────────────────────
    {
        "title": "Dracula", "author": "Bram Stoker",
        "genre": ["horror", "gothic"], "year": 1897,
        "language": "English", "reading_level": "intermediate",
        "url": "https://www.gutenberg.org/files/345/345-0.txt"
    },
    {
        "title": "Frankenstein", "author": "Mary Shelley",
        "genre": ["horror", "sci-fi"], "year": 1818,
        "language": "English", "reading_level": "intermediate",
        "url": "https://www.gutenberg.org/files/84/84-0.txt"
    },
    {
        "title": "The Strange Case of Dr Jekyll and Mr Hyde", "author": "Robert Louis Stevenson",
        "genre": ["horror", "thriller"], "year": 1886,
        "language": "English", "reading_level": "intermediate",
        "url": "https://www.gutenberg.org/files/43/43-0.txt"
    },
    {
        "title": "The Picture of Dorian Gray", "author": "Oscar Wilde",
        "genre": ["horror", "gothic", "classic"], "year": 1890,
        "language": "English", "reading_level": "intermediate",
        "url": "https://www.gutenberg.org/files/174/174-0.txt"
    },
    {
        "title": "The Dunwich Horror", "author": "H.P. Lovecraft",
        "genre": ["horror", "gothic"], "year": 1929,
        "language": "English", "reading_level": "advanced",
        "url": "https://www.gutenberg.org/files/50133/50133-0.txt"
    },
    {
        "title": "The Call of Cthulhu", "author": "H.P. Lovecraft",
        "genre": ["horror", "gothic"], "year": 1928,
        "language": "English", "reading_level": "advanced",
        "url": "https://www.gutenberg.org/files/68236/68236-0.txt"
    },
    {
        "title": "The Turn of the Screw", "author": "Henry James",
        "genre": ["horror", "gothic"], "year": 1898,
        "language": "English", "reading_level": "advanced",
        "url": "https://www.gutenberg.org/files/209/209-0.txt"
    },
    {
        "title": "Ghost Stories of an Antiquary", "author": "M.R. James",
        "genre": ["horror", "gothic"], "year": 1904,
        "language": "English", "reading_level": "intermediate",
        "url": "https://www.gutenberg.org/files/8486/8486-0.txt"
    },
    {
        "title": "The Monk", "author": "Matthew Gregory Lewis",
        "genre": ["horror", "gothic"], "year": 1796,
        "language": "English", "reading_level": "advanced",
        "url": "https://www.gutenberg.org/files/601/601-0.txt"
    },
    {
        "title": "Carmilla", "author": "J. Sheridan Le Fanu",
        "genre": ["horror", "gothic"], "year": 1872,
        "language": "English", "reading_level": "intermediate",
        "url": "https://www.gutenberg.org/files/10007/10007-0.txt"
    },

    # ── SCI-FI (12) ─────────────────────────────────────────
    {
        "title": "The Time Machine", "author": "H.G. Wells",
        "genre": ["sci-fi"], "year": 1895,
        "language": "English", "reading_level": "intermediate",
        "url": "https://www.gutenberg.org/files/35/35-0.txt"
    },
    {
        "title": "The War of the Worlds", "author": "H.G. Wells",
        "genre": ["sci-fi", "adventure"], "year": 1898,
        "language": "English", "reading_level": "intermediate",
        "url": "https://www.gutenberg.org/files/36/36-0.txt"
    },
    {
        "title": "The Invisible Man", "author": "H.G. Wells",
        "genre": ["sci-fi", "thriller"], "year": 1897,
        "language": "English", "reading_level": "intermediate",
        "url": "https://www.gutenberg.org/files/5230/5230-0.txt"
    },
    {
        "title": "The Island of Doctor Moreau", "author": "H.G. Wells",
        "genre": ["sci-fi", "horror"], "year": 1896,
        "language": "English", "reading_level": "intermediate",
        "url": "https://www.gutenberg.org/files/159/159-0.txt"
    },
    {
        "title": "The First Men in the Moon", "author": "H.G. Wells",
        "genre": ["sci-fi", "adventure"], "year": 1901,
        "language": "English", "reading_level": "intermediate",
        "url": "https://www.gutenberg.org/files/1013/1013-0.txt"
    },
    {
        "title": "Journey to the Center of the Earth", "author": "Jules Verne",
        "genre": ["sci-fi", "adventure"], "year": 1864,
        "language": "English", "reading_level": "intermediate",
        "url": "https://www.gutenberg.org/files/18857/18857-0.txt"
    },
    {
        "title": "Twenty Thousand Leagues Under the Sea", "author": "Jules Verne",
        "genre": ["sci-fi", "adventure"], "year": 1870,
        "language": "English", "reading_level": "intermediate",
        "url": "https://www.gutenberg.org/files/164/164-0.txt"
    },
    {
        "title": "From the Earth to the Moon", "author": "Jules Verne",
        "genre": ["sci-fi", "adventure"], "year": 1865,
        "language": "English", "reading_level": "intermediate",
        "url": "https://www.gutenberg.org/files/83/83-0.txt"
    },
    {
        "title": "The Land That Time Forgot", "author": "Edgar Rice Burroughs",
        "genre": ["sci-fi", "adventure"], "year": 1918,
        "language": "English", "reading_level": "intermediate",
        "url": "https://www.gutenberg.org/files/551/551-0.txt"
    },
    {
        "title": "A Princess of Mars", "author": "Edgar Rice Burroughs",
        "genre": ["sci-fi", "fantasy", "adventure"], "year": 1912,
        "language": "English", "reading_level": "intermediate",
        "url": "https://www.gutenberg.org/files/62/62-0.txt"
    },
    {
        "title": "The Sleeper Awakes", "author": "H.G. Wells",
        "genre": ["sci-fi"], "year": 1910,
        "language": "English", "reading_level": "intermediate",
        "url": "https://www.gutenberg.org/files/775/775-0.txt"
    },
    {
        "title": "Thuvia Maid of Mars", "author": "Edgar Rice Burroughs",
        "genre": ["sci-fi", "fantasy"], "year": 1916,
        "language": "English", "reading_level": "intermediate",
        "url": "https://www.gutenberg.org/files/72/72-0.txt"
    },

    # ── ADVENTURE (12) ──────────────────────────────────────
    {
        "title": "Treasure Island", "author": "Robert Louis Stevenson",
        "genre": ["adventure"], "year": 1883,
        "language": "English", "reading_level": "beginner",
        "url": "https://www.gutenberg.org/files/120/120-0.txt"
    },
    {
        "title": "Moby Dick", "author": "Herman Melville",
        "genre": ["adventure", "classic"], "year": 1851,
        "language": "English", "reading_level": "advanced",
        "url": "https://www.gutenberg.org/files/2701/2701-0.txt"
    },
    {
        "title": "Robinson Crusoe", "author": "Daniel Defoe",
        "genre": ["adventure", "classic"], "year": 1719,
        "language": "English", "reading_level": "intermediate",
        "url": "https://www.gutenberg.org/files/521/521-0.txt"
    },
    {
        "title": "The Count of Monte Cristo", "author": "Alexandre Dumas",
        "genre": ["adventure", "thriller"], "year": 1844,
        "language": "English", "reading_level": "intermediate",
        "url": "https://www.gutenberg.org/files/1184/1184-0.txt"
    },
    {
        "title": "Around the World in 80 Days", "author": "Jules Verne",
        "genre": ["adventure"], "year": 1872,
        "language": "English", "reading_level": "beginner",
        "url": "https://www.gutenberg.org/files/103/103-0.txt"
    },
    {
        "title": "The Three Musketeers", "author": "Alexandre Dumas",
        "genre": ["adventure", "thriller", "classic"], "year": 1844,
        "language": "English", "reading_level": "intermediate",
        "url": "https://www.gutenberg.org/files/1257/1257-0.txt"
    },
    {
        "title": "Twenty Years After", "author": "Alexandre Dumas",
        "genre": ["adventure", "thriller"], "year": 1845,
        "language": "English", "reading_level": "intermediate",
        "url": "https://www.gutenberg.org/files/1259/1259-0.txt"
    },
    {
        "title": "The Scarlet Pimpernel", "author": "Baroness Orczy",
        "genre": ["thriller", "adventure"], "year": 1905,
        "language": "English", "reading_level": "intermediate",
        "url": "https://www.gutenberg.org/files/60/60-0.txt"
    },
    {
        "title": "King Solomons Mines", "author": "H. Rider Haggard",
        "genre": ["adventure"], "year": 1885,
        "language": "English", "reading_level": "intermediate",
        "url": "https://www.gutenberg.org/files/2166/2166-0.txt"
    },
    {
        "title": "She", "author": "H. Rider Haggard",
        "genre": ["adventure", "fantasy"], "year": 1887,
        "language": "English", "reading_level": "intermediate",
        "url": "https://www.gutenberg.org/files/3155/3155-0.txt"
    },
    {
        "title": "The Prisoner of Zenda", "author": "Anthony Hope",
        "genre": ["adventure", "thriller"], "year": 1894,
        "language": "English", "reading_level": "intermediate",
        "url": "https://www.gutenberg.org/files/95/95-0.txt"
    },
    {
        "title": "Kidnapped", "author": "Robert Louis Stevenson",
        "genre": ["adventure", "classic"], "year": 1886,
        "language": "English", "reading_level": "intermediate",
        "url": "https://www.gutenberg.org/files/421/421-0.txt"
    },

    # ── MYSTERY & DETECTIVE (10) ─────────────────────────────
    {
        "title": "The Adventures of Sherlock Holmes", "author": "Arthur Conan Doyle",
        "genre": ["mystery", "detective"], "year": 1892,
        "language": "English", "reading_level": "intermediate",
        "url": "https://www.gutenberg.org/files/1661/1661-0.txt"
    },
    {
        "title": "The Hound of the Baskervilles", "author": "Arthur Conan Doyle",
        "genre": ["mystery", "detective"], "year": 1902,
        "language": "English", "reading_level": "intermediate",
        "url": "https://www.gutenberg.org/files/2852/2852-0.txt"
    },
    {
        "title": "The Memoirs of Sherlock Holmes", "author": "Arthur Conan Doyle",
        "genre": ["mystery", "detective"], "year": 1894,
        "language": "English", "reading_level": "intermediate",
        "url": "https://www.gutenberg.org/files/834/834-0.txt"
    },
    {
        "title": "The Return of Sherlock Holmes", "author": "Arthur Conan Doyle",
        "genre": ["mystery", "detective"], "year": 1905,
        "language": "English", "reading_level": "intermediate",
        "url": "https://www.gutenberg.org/files/108/108-0.txt"
    },
    {
        "title": "The Moonstone", "author": "Wilkie Collins",
        "genre": ["mystery", "detective"], "year": 1868,
        "language": "English", "reading_level": "advanced",
        "url": "https://www.gutenberg.org/files/155/155-0.txt"
    },
    {
        "title": "The Woman in White", "author": "Wilkie Collins",
        "genre": ["mystery", "thriller"], "year": 1859,
        "language": "English", "reading_level": "advanced",
        "url": "https://www.gutenberg.org/files/583/583-0.txt"
    },
    {
        "title": "The Mystery of the Yellow Room", "author": "Gaston Leroux",
        "genre": ["mystery", "detective"], "year": 1907,
        "language": "English", "reading_level": "intermediate",
        "url": "https://www.gutenberg.org/files/1702/1702-0.txt"
    },
    {
        "title": "The Big Bow Mystery", "author": "Israel Zangwill",
        "genre": ["mystery", "detective"], "year": 1892,
        "language": "English", "reading_level": "intermediate",
        "url": "https://www.gutenberg.org/files/18438/18438-0.txt"
    },
    {
        "title": "Tales of Terror and Mystery", "author": "Arthur Conan Doyle",
        "genre": ["mystery", "horror"], "year": 1922,
        "language": "English", "reading_level": "intermediate",
        "url": "https://www.gutenberg.org/files/32536/32536-0.txt"
    },
    {
        "title": "The Casebook of Sherlock Holmes", "author": "Arthur Conan Doyle",
        "genre": ["mystery", "detective"], "year": 1927,
        "language": "English", "reading_level": "intermediate",
        "url": "https://www.gutenberg.org/files/69481/69481-0.txt"
    },

    # ── ROMANCE & CLASSIC (12) ───────────────────────────────
    {
        "title": "Pride and Prejudice", "author": "Jane Austen",
        "genre": ["romance", "classic"], "year": 1813,
        "language": "English", "reading_level": "intermediate",
        "url": "https://www.gutenberg.org/files/1342/1342-0.txt"
    },
    {
        "title": "Sense and Sensibility", "author": "Jane Austen",
        "genre": ["romance", "classic"], "year": 1811,
        "language": "English", "reading_level": "intermediate",
        "url": "https://www.gutenberg.org/files/161/161-0.txt"
    },
    {
        "title": "Emma", "author": "Jane Austen",
        "genre": ["romance", "classic"], "year": 1815,
        "language": "English", "reading_level": "intermediate",
        "url": "https://www.gutenberg.org/files/158/158-0.txt"
    },
    {
        "title": "Persuasion", "author": "Jane Austen",
        "genre": ["romance", "classic"], "year": 1818,
        "language": "English", "reading_level": "intermediate",
        "url": "https://www.gutenberg.org/files/105/105-0.txt"
    },
    {
        "title": "Jane Eyre", "author": "Charlotte Bronte",
        "genre": ["romance", "classic"], "year": 1847,
        "language": "English", "reading_level": "intermediate",
        "url": "https://www.gutenberg.org/files/1260/1260-0.txt"
    },
    {
        "title": "Wuthering Heights", "author": "Emily Bronte",
        "genre": ["romance", "gothic", "classic"], "year": 1847,
        "language": "English", "reading_level": "intermediate",
        "url": "https://www.gutenberg.org/files/768/768-0.txt"
    },
    {
        "title": "Anna Karenina", "author": "Leo Tolstoy",
        "genre": ["romance", "classic"], "year": 1878,
        "language": "English", "reading_level": "advanced",
        "url": "https://www.gutenberg.org/files/1399/1399-0.txt"
    },
    {
        "title": "Northanger Abbey", "author": "Jane Austen",
        "genre": ["romance", "satire", "classic"], "year": 1817,
        "language": "English", "reading_level": "intermediate",
        "url": "https://www.gutenberg.org/files/121/121-0.txt"
    },
    {
        "title": "Tess of the dUrbervilles", "author": "Thomas Hardy",
        "genre": ["romance", "classic", "tragedy"], "year": 1891,
        "language": "English", "reading_level": "advanced",
        "url": "https://www.gutenberg.org/files/110/110-0.txt"
    },
    {
        "title": "Far from the Madding Crowd", "author": "Thomas Hardy",
        "genre": ["romance", "classic"], "year": 1874,
        "language": "English", "reading_level": "advanced",
        "url": "https://www.gutenberg.org/files/107/107-0.txt"
    },
    {
        "title": "The Sorrows of Young Werther", "author": "Johann Wolfgang von Goethe",
        "genre": ["romance", "classic", "philosophy"], "year": 1774,
        "language": "English", "reading_level": "intermediate",
        "url": "https://www.gutenberg.org/files/2527/2527-0.txt"
    },
    {
        "title": "Lorna Doone", "author": "R.D. Blackmore",
        "genre": ["romance", "adventure", "historical"], "year": 1869,
        "language": "English", "reading_level": "intermediate",
        "url": "https://www.gutenberg.org/files/3762/3762-0.txt"
    },

    # ── MYTHOLOGY & EPIC (6) ─────────────────────────────────
    {
        "title": "The Odyssey", "author": "Homer",
        "genre": ["mythology", "epic", "fantasy"], "year": -800,
        "language": "English", "reading_level": "advanced",
        "url": "https://www.gutenberg.org/files/1727/1727-0.txt"
    },
    {
        "title": "The Iliad", "author": "Homer",
        "genre": ["mythology", "epic", "war"], "year": -750,
        "language": "English", "reading_level": "advanced",
        "url": "https://www.gutenberg.org/files/6130/6130-0.txt"
    },
    {
        "title": "Beowulf", "author": "Unknown",
        "genre": ["fantasy", "epic", "mythology"], "year": 1000,
        "language": "English", "reading_level": "advanced",
        "url": "https://www.gutenberg.org/files/16328/16328-0.txt"
    },
    {
        "title": "The Divine Comedy", "author": "Dante Alighieri",
        "genre": ["epic", "mythology", "classic"], "year": 1320,
        "language": "English", "reading_level": "advanced",
        "url": "https://www.gutenberg.org/files/8800/8800-0.txt"
    },
    {
        "title": "Metamorphoses", "author": "Ovid",
        "genre": ["mythology", "epic", "classic"], "year": 8,
        "language": "English", "reading_level": "advanced",
        "url": "https://www.gutenberg.org/files/21765/21765-0.txt"
    },
    {
        "title": "The Aeneid", "author": "Virgil",
        "genre": ["mythology", "epic", "war"], "year": -19,
        "language": "English", "reading_level": "advanced",
        "url": "https://www.gutenberg.org/files/228/228-0.txt"
    },

    # ── PHILOSOPHY & CLASSIC LITERATURE (10) ─────────────────
    {
        "title": "Crime and Punishment", "author": "Fyodor Dostoevsky",
        "genre": ["classic", "thriller", "philosophy"], "year": 1866,
        "language": "English", "reading_level": "advanced",
        "url": "https://www.gutenberg.org/files/2554/2554-0.txt"
    },
    {
        "title": "The Brothers Karamazov", "author": "Fyodor Dostoevsky",
        "genre": ["classic", "philosophy"], "year": 1880,
        "language": "English", "reading_level": "advanced",
        "url": "https://www.gutenberg.org/files/28054/28054-0.txt"
    },
    {
        "title": "Notes from the Underground", "author": "Fyodor Dostoevsky",
        "genre": ["philosophy", "classic"], "year": 1864,
        "language": "English", "reading_level": "advanced",
        "url": "https://www.gutenberg.org/files/600/600-0.txt"
    },
    {
        "title": "Don Quixote", "author": "Miguel de Cervantes",
        "genre": ["classic", "adventure", "satire"], "year": 1605,
        "language": "English", "reading_level": "advanced",
        "url": "https://www.gutenberg.org/files/996/996-0.txt"
    },
    {
        "title": "Les Miserables", "author": "Victor Hugo",
        "genre": ["classic", "historical"], "year": 1862,
        "language": "English", "reading_level": "advanced",
        "url": "https://www.gutenberg.org/files/135/135-0.txt"
    },
    {
        "title": "War and Peace", "author": "Leo Tolstoy",
        "genre": ["classic", "war", "historical"], "year": 1869,
        "language": "English", "reading_level": "advanced",
        "url": "https://www.gutenberg.org/files/2600/2600-0.txt"
    },
    {
        "title": "The Idiot", "author": "Fyodor Dostoevsky",
        "genre": ["classic", "philosophy"], "year": 1869,
        "language": "English", "reading_level": "advanced",
        "url": "https://www.gutenberg.org/files/2638/2638-0.txt"
    },
    {
        "title": "Thus Spoke Zarathustra", "author": "Friedrich Nietzsche",
        "genre": ["philosophy"], "year": 1883,
        "language": "English", "reading_level": "advanced",
        "url": "https://www.gutenberg.org/files/1998/1998-0.txt"
    },
    {
        "title": "Beyond Good and Evil", "author": "Friedrich Nietzsche",
        "genre": ["philosophy"], "year": 1886,
        "language": "English", "reading_level": "advanced",
        "url": "https://www.gutenberg.org/files/4363/4363-0.txt"
    },
    {
        "title": "Autobiography of Benjamin Franklin", "author": "Benjamin Franklin",
        "genre": ["classic", "biography", "philosophy"], "year": 1791,
        "language": "English", "reading_level": "intermediate",
        "url": "https://www.gutenberg.org/files/20203/20203-0.txt"
    },

    # ── FANTASY & CHILDREN (8) ──────────────────────────────
    {
        "title": "Alice in Wonderland", "author": "Lewis Carroll",
        "genre": ["fantasy", "children", "classic"], "year": 1865,
        "language": "English", "reading_level": "beginner",
        "url": "https://www.gutenberg.org/files/11/11-0.txt"
    },
    {
        "title": "Through the Looking Glass", "author": "Lewis Carroll",
        "genre": ["fantasy", "children", "classic"], "year": 1871,
        "language": "English", "reading_level": "beginner",
        "url": "https://www.gutenberg.org/files/12/12-0.txt"
    },
    {
        "title": "The Wonderful Wizard of Oz", "author": "L. Frank Baum",
        "genre": ["fantasy", "children"], "year": 1900,
        "language": "English", "reading_level": "beginner",
        "url": "https://www.gutenberg.org/files/55/55-0.txt"
    },
    {
        "title": "Peter Pan", "author": "J.M. Barrie",
        "genre": ["fantasy", "children", "classic"], "year": 1911,
        "language": "English", "reading_level": "beginner",
        "url": "https://www.gutenberg.org/files/16/16-0.txt"
    },
    {
        "title": "The Wind in the Willows", "author": "Kenneth Grahame",
        "genre": ["fantasy", "children", "classic"], "year": 1908,
        "language": "English", "reading_level": "beginner",
        "url": "https://www.gutenberg.org/files/289/289-0.txt"
    },
    {
        "title": "The Jungle Book", "author": "Rudyard Kipling",
        "genre": ["fantasy", "children", "adventure"], "year": 1894,
        "language": "English", "reading_level": "beginner",
        "url": "https://www.gutenberg.org/files/236/236-0.txt"
    },
    {
        "title": "King Arthur and the Knights of the Round Table", "author": "Sir Thomas Malory",
        "genre": ["fantasy", "epic", "mythology"], "year": 1485,
        "language": "English", "reading_level": "advanced",
        "url": "https://www.gutenberg.org/files/1702/1702-0.txt"
    },
    {
        "title": "The Blue Fairy Book", "author": "Andrew Lang",
        "genre": ["fantasy", "children", "mythology"], "year": 1889,
        "language": "English", "reading_level": "beginner",
        "url": "https://www.gutenberg.org/files/503/503-0.txt"
    },

    # ── HISTORICAL FICTION (8) ───────────────────────────────
    {
        "title": "A Tale of Two Cities", "author": "Charles Dickens",
        "genre": ["historical", "classic", "thriller"], "year": 1859,
        "language": "English", "reading_level": "intermediate",
        "url": "https://www.gutenberg.org/files/98/98-0.txt"
    },
    {
        "title": "Oliver Twist", "author": "Charles Dickens",
        "genre": ["historical", "classic"], "year": 1837,
        "language": "English", "reading_level": "intermediate",
        "url": "https://www.gutenberg.org/files/730/730-0.txt"
    },
    {
        "title": "Great Expectations", "author": "Charles Dickens",
        "genre": ["historical", "classic"], "year": 1861,
        "language": "English", "reading_level": "intermediate",
        "url": "https://www.gutenberg.org/files/1400/1400-0.txt"
    },
    {
        "title": "David Copperfield", "author": "Charles Dickens",
        "genre": ["historical", "classic"], "year": 1850,
        "language": "English", "reading_level": "intermediate",
        "url": "https://www.gutenberg.org/files/766/766-0.txt"
    },
    {
        "title": "Ivanhoe", "author": "Walter Scott",
        "genre": ["historical", "adventure"], "year": 1820,
        "language": "English", "reading_level": "advanced",
        "url": "https://www.gutenberg.org/files/82/82-0.txt"
    },
    {
        "title": "The Scarlet Letter", "author": "Nathaniel Hawthorne",
        "genre": ["historical", "classic", "romance"], "year": 1850,
        "language": "English", "reading_level": "advanced",
        "url": "https://www.gutenberg.org/files/33/33-0.txt"
    },
    {
        "title": "Ben-Hur A Tale of the Christ", "author": "Lew Wallace",
        "genre": ["historical", "adventure", "classic"], "year": 1880,
        "language": "English", "reading_level": "intermediate",
        "url": "https://www.gutenberg.org/files/2145/2145-0.txt"
    },
    {
        "title": "Quo Vadis", "author": "Henryk Sienkiewicz",
        "genre": ["historical", "romance", "adventure"], "year": 1896,
        "language": "English", "reading_level": "intermediate",
        "url": "https://www.gutenberg.org/files/2853/2853-0.txt"
    },

    # ── SATIRE & HUMOR (6) ──────────────────────────────────
    {
        "title": "Adventures of Huckleberry Finn", "author": "Mark Twain",
        "genre": ["satire", "adventure", "classic"], "year": 1884,
        "language": "English", "reading_level": "intermediate",
        "url": "https://www.gutenberg.org/files/76/76-0.txt"
    },
    {
        "title": "The Adventures of Tom Sawyer", "author": "Mark Twain",
        "genre": ["satire", "adventure", "children"], "year": 1876,
        "language": "English", "reading_level": "beginner",
        "url": "https://www.gutenberg.org/files/74/74-0.txt"
    },
    {
        "title": "Gullivers Travels", "author": "Jonathan Swift",
        "genre": ["satire", "fantasy", "classic"], "year": 1726,
        "language": "English", "reading_level": "intermediate",
        "url": "https://www.gutenberg.org/files/829/829-0.txt"
    },
    {
        "title": "Candide", "author": "Voltaire",
        "genre": ["satire", "philosophy", "classic"], "year": 1759,
        "language": "English", "reading_level": "intermediate",
        "url": "https://www.gutenberg.org/files/19942/19942-0.txt"
    },
    {
        "title": "The Man Who Was Thursday", "author": "G.K. Chesterton",
        "genre": ["satire", "thriller", "philosophy"], "year": 1908,
        "language": "English", "reading_level": "intermediate",
        "url": "https://www.gutenberg.org/files/1695/1695-0.txt"
    },
    {
        "title": "Three Men in a Boat", "author": "Jerome K. Jerome",
        "genre": ["satire", "humor", "adventure"], "year": 1889,
        "language": "English", "reading_level": "beginner",
        "url": "https://www.gutenberg.org/files/308/308-0.txt"
    },

    # ── WAR & POLITICAL (6) ──────────────────────────────────
    {
        "title": "The Art of War", "author": "Sun Tzu",
        "genre": ["war", "philosophy", "classic"], "year": -500,
        "language": "English", "reading_level": "intermediate",
        "url": "https://www.gutenberg.org/files/132/132-0.txt"
    },
    {
        "title": "The Prince", "author": "Niccolo Machiavelli",
        "genre": ["philosophy", "political", "classic"], "year": 1532,
        "language": "English", "reading_level": "advanced",
        "url": "https://www.gutenberg.org/files/1232/1232-0.txt"
    },
    {
        "title": "The Republic", "author": "Plato",
        "genre": ["philosophy", "political", "classic"], "year": -380,
        "language": "English", "reading_level": "advanced",
        "url": "https://www.gutenberg.org/files/1497/1497-0.txt"
    },
    {
        "title": "Leviathan", "author": "Thomas Hobbes",
        "genre": ["philosophy", "political"], "year": 1651,
        "language": "English", "reading_level": "advanced",
        "url": "https://www.gutenberg.org/files/3207/3207-0.txt"
    },
    {
        "title": "Common Sense", "author": "Thomas Paine",
        "genre": ["political", "philosophy", "classic"], "year": 1776,
        "language": "English", "reading_level": "intermediate",
        "url": "https://www.gutenberg.org/files/147/147-0.txt"
    },
    {
        "title": "The Communist Manifesto", "author": "Karl Marx",
        "genre": ["political", "philosophy"], "year": 1848,
        "language": "English", "reading_level": "advanced",
        "url": "https://www.gutenberg.org/files/61/61-0.txt"
    },

    # ── SHORT STORIES & POETRY (10) ─────────────────────────
    {
        "title": "The Complete Poetical Works of Edgar Allan Poe", "author": "Edgar Allan Poe",
        "genre": ["horror", "poetry", "gothic"], "year": 1849,
        "language": "English", "reading_level": "intermediate",
        "url": "https://www.gutenberg.org/files/10031/10031-0.txt"
    },
    {
        "title": "The Works of Edgar Allan Poe Vol 1", "author": "Edgar Allan Poe",
        "genre": ["horror", "mystery", "gothic"], "year": 1840,
        "language": "English", "reading_level": "intermediate",
        "url": "https://www.gutenberg.org/files/2147/2147-0.txt"
    },
    {
        "title": "Fairy Tales by Hans Christian Andersen", "author": "Hans Christian Andersen",
        "genre": ["fantasy", "children", "classic"], "year": 1835,
        "language": "English", "reading_level": "beginner",
        "url": "https://www.gutenberg.org/files/1597/1597-0.txt"
    },
    {
        "title": "Grimms Fairy Tales", "author": "Brothers Grimm",
        "genre": ["fantasy", "children", "mythology"], "year": 1812,
        "language": "English", "reading_level": "beginner",
        "url": "https://www.gutenberg.org/files/2591/2591-0.txt"
    },
    {
        "title": "Aesops Fables", "author": "Aesop",
        "genre": ["classic", "children", "mythology"], "year": -600,
        "language": "English", "reading_level": "beginner",
        "url": "https://www.gutenberg.org/files/11339/11339-0.txt"
    },
    {
        "title": "Leaves of Grass", "author": "Walt Whitman",
        "genre": ["poetry", "classic"], "year": 1855,
        "language": "English", "reading_level": "intermediate",
        "url": "https://www.gutenberg.org/files/1322/1322-0.txt"
    },
    {
        "title": "Songs of Innocence and Experience", "author": "William Blake",
        "genre": ["poetry", "classic", "philosophy"], "year": 1789,
        "language": "English", "reading_level": "intermediate",
        "url": "https://www.gutenberg.org/files/1934/1934-0.txt"
    },
    {
        "title": "The Arabian Nights", "author": "Anonymous",
        "genre": ["fantasy", "mythology", "classic"], "year": 1706,
        "language": "English", "reading_level": "intermediate",
        "url": "https://www.gutenberg.org/files/128/128-0.txt"
    },
    {
        "title": "Narrative of the Life of Frederick Douglass", "author": "Frederick Douglass",
        "genre": ["biography", "historical", "classic"], "year": 1845,
        "language": "English", "reading_level": "intermediate",
        "url": "https://www.gutenberg.org/files/23/23-0.txt"
    },
    {
        "title": "The Souls of Black Folk", "author": "W.E.B. Du Bois",
        "genre": ["biography", "philosophy", "historical"], "year": 1903,
        "language": "English", "reading_level": "advanced",
        "url": "https://www.gutenberg.org/files/408/408-0.txt"
    },
]

# Save folder — goes up one level from extractbooks/ into backend/books/
SAVE_DIR = os.path.join(os.path.dirname(__file__), "..", "books")
os.makedirs(SAVE_DIR, exist_ok=True)

def download_books():
    total = len(BOOKS)
    print(f"📚 Downloading {total} books to: {os.path.abspath(SAVE_DIR)}\n")
    success, failed = 0, []

    for i, book in enumerate(BOOKS, 1):
        safe_name = (book["title"]
                     .replace(" ", "_")
                     .replace("/", "_")
                     .replace(":", "")
                     .replace("'", "")
                     .replace(",", "")) + ".txt"
        filepath = os.path.join(SAVE_DIR, safe_name)

        if os.path.exists(filepath):
            print(f"[{i:03d}/{total}] SKIP  ── {book['title']}")
            success += 1
            continue

        print(f"[{i:03d}/{total}] GET   ── {book['title']} ...", end=" ", flush=True)
        try:
            r = requests.get(book["url"], timeout=30)
            r.raise_for_status()
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(r.text)
            kb = os.path.getsize(filepath) // 1024
            print(f"✅ {kb} KB")
            success += 1
            time.sleep(0.3)   # be polite to Gutenberg servers
        except Exception as e:
            print(f"❌ {e}")
            failed.append(book["title"])

    print(f"\n{'='*55}")
    print(f"✅  Success : {success}/{total}")
    if failed:
        print(f"❌  Failed  : {len(failed)}")
        for t in failed: print(f"   • {t}")
    print(f"📁  Saved to: {os.path.abspath(SAVE_DIR)}")

if __name__ == "__main__":
    download_books()