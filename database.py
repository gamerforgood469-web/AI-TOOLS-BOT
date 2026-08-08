import sqlite3

DATABASE = "content.db"


def initialize():
    db = sqlite3.connect(DATABASE)

    db.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            topic TEXT,
            content TEXT,
            post_format TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    db.commit()
    db.close()


def get_history(limit=100):
    db = sqlite3.connect(DATABASE)

    rows = db.execute("""
        SELECT title, topic, content, post_format
        FROM posts
        ORDER BY id DESC
        LIMIT ?
    """, (limit,)).fetchall()

    db.close()

    return rows


def save_post(title, topic, content, post_format):
    db = sqlite3.connect(DATABASE)

    db.execute("""
        INSERT INTO posts
        (title, topic, content, post_format)
        VALUES (?, ?, ?, ?)
    """, (
        title,
        topic,
        content,
        post_format
    ))

    db.commit()
    db.close()
