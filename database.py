import sqlite3
import random
from kuis import QUIZ_AB

conn = sqlite3.connect("quiz.db")
cur = conn.cursor()

def init_db():
    cur.execute("""
    CREATE TABLE IF NOT EXISTS quiz (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        theme TEXT,
        question TEXT,
        A TEXT,
        B TEXT,
        resultA TEXT,
        resultB TEXT
    )
    """)
    conn.commit()

def seed_data():
    cur.execute("SELECT COUNT(*) FROM quiz")
    if cur.fetchone()[0] > 0: return

    for theme, questions in QUIZ_AB.items():
        for q in questions:
            cur.execute("""
            INSERT INTO quiz (theme, question, A, B, resultA, resultB)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (theme, q["q"], q["A"], q["B"], q["resultA"], q["resultB"]))
    conn.commit()

def get_quiz(theme):
    cur.execute("SELECT * FROM quiz WHERE theme=?", (theme,))
    rows = cur.fetchall()
    if not rows: return None
    row = random.choice(rows)
    return {"id": row[0], "q": row[2], "A": row[3], "B": row[4], "resultA": row[5], "resultB": row[6]}

init_db()
seed_data()
