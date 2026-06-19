import requests
import sqlite3
import threading


class DictionaryDataBase:
    def __init__(self, filename: str = "dictionary.db") -> None:
        self.filename = filename
        self.conn = None
        self.cursor = None
        self._lock = threading.Lock()   # FIX: thread safety for shared connection
        self.connect()
        self.create_tables()

    def connect(self):
        # FIX: check_same_thread=False is required because the GUI spawns a worker
        # thread that calls searchdict() while the main thread owns this connection.
        # Without this flag, SQLite raises "objects created in a thread can only be
        # used in that same thread."
        self.conn = sqlite3.connect(self.filename, check_same_thread=False)
        self.cursor = self.conn.cursor()
        print(f"Connected to {self.filename}")

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS dictionary (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                word    TEXT    UNIQUE NOT NULL,
                meaning TEXT    NOT NULL,
                type    TEXT
            )
        """)
        self.conn.commit()
        print("Table created/verified")

    def search_offline(self, word: str) -> tuple:
        try:
            with self._lock:
                self.cursor.execute(
                    "SELECT meaning, type FROM dictionary WHERE word = ?", (word,)
                )
                row = self.cursor.fetchone()
            return (row[0], row[1]) if row else None
        except Exception as e:
            print(f"Database error: {e}")
            return None

    def upload_data(self, data: tuple) -> bool:
        try:
            with self._lock:
                self.cursor.execute(
                    "INSERT INTO dictionary (word, meaning, type) VALUES (?, ?, ?)",
                    (data[0], data[1], data[2] if len(data) == 3 else "Not Defined"),
                )
                self.conn.commit()
        except Exception as e:
            print(f"Error occurred: {e}")
            return False
        else:
            print("Data pushed successfully.")
            return True

    def searchdict(self, word: str) -> tuple:
        if not word or not isinstance(word, str):
            return ("Invalid input.", "N/A")

        word = word.strip().lower()

        if len(word) > 100:
            return ("Word too long.", "N/A")

        if not all(c.isalnum() or c == "-" for c in word):
            return ("Invalid word format.", "N/A")

        # Check local DB first
        offline = self.search_offline(word)
        if offline:
            return offline

        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        try:
            response = requests.get(url, timeout=5)

            # FIX: Check 404 explicitly BEFORE raise_for_status().
            # Previously, raise_for_status() converted 404 into an HTTPError,
            # so the user saw "API error: 404" instead of "Word not found."
            # The if/else block after raise_for_status was also dead code —
            # raise_for_status() means the code below it is always status 200.
            if response.status_code == 404:
                return ("Word not found.", "N/A")

            response.raise_for_status()

            api_data = response.json()
            meaning = api_data[0]["meanings"][0]["definitions"][0]["definition"]

            # FIX: Actually capture the word type from the API response.
            # Previously upload_data() was called with a 2-tuple so type was
            # always saved as "Not Defined", ignoring the partOfSpeech field.
            wtype = api_data[0]["meanings"][0].get("partOfSpeech", "Not Defined")

            self.upload_data((word, meaning, wtype))
            return (meaning, wtype)

        except requests.Timeout:
            return ("Request timed out. Check your connection.", "Network Issue")
        except requests.ConnectionError:
            return ("No internet connection.", "Network Issue")
        except requests.HTTPError as e:
            return (f"API error: {e.response.status_code}", "N/A")
        except (KeyError, IndexError):
            return ("Could not parse API response.", "N/A")
        except Exception:
            return ("An unexpected error occurred.", "N/A")

    def edit_data(self, word: str, meaning: str = "", wtype: str = "") -> bool:
        try:
            with self._lock:
                if meaning and wtype:
                    self.cursor.execute(
                        "UPDATE dictionary SET meaning = ?, type = ? WHERE word = ?",
                        (meaning, wtype, word),
                    )
                elif wtype:
                    self.cursor.execute(
                        "UPDATE dictionary SET type = ? WHERE word = ?", (wtype, word)
                    )
                elif meaning:
                    self.cursor.execute(
                        "UPDATE dictionary SET meaning = ? WHERE word = ?",
                        (meaning, word),
                    )
                else:
                    raise ValueError("Provide at least one of: meaning, wtype.")
                self.conn.commit()
            return True
        except Exception as e:
            print(f"Edit error: {e}")
            return False

    def delete_word(self, word: str) -> bool:
        try:
            with self._lock:
                self.cursor.execute(
                    "DELETE FROM dictionary WHERE word = ?", (word,)
                )
                self.conn.commit()
            return True
        except Exception as e:
            print(f"Delete error: {e}")
            return False

    def show_dictionary(self) -> list:
        with self._lock:
            self.cursor.execute("SELECT * FROM dictionary")
            return self.cursor.fetchall()

    def close(self):
        # FIX: previously only closed cursor, leaving the connection open.
        try:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
        except Exception as e:
            print(f"Error closing database: {e}")