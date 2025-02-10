import sqlite3
import os
import json

DB_FILE = "osint.db"

def init_db():

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS intel_collection (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT,
            title TEXT,
            url TEXT,
            content TEXT,
            named_entities TEXT,
            sentiment REAL,
            risk_score INTEGER
        )
    """)
    conn.commit()
    conn.close()

def save_document(doc):

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    named_ents_json = json.dumps(doc.get("named_entities", []))
    cursor.execute("""
        INSERT INTO intel_collection (source, title, url, content, named_entities, sentiment, risk_score)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        doc.get("source"),
        doc.get("title"),
        doc.get("url"),
        doc.get("content"),
        named_ents_json,
        doc.get("sentiment", 0.0),
        doc.get("risk_score", 0)
    ))
    conn.commit()
    conn.close()

def get_latest_documents(limit=10):

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT source, title, url, content, named_entities, sentiment, risk_score
        FROM intel_collection
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()

    docs = []
    for (source, title, url, content, named_ents_json, sentiment, risk_score) in rows:
        named_ents = json.loads(named_ents_json or "[]")
        docs.append({
            "source": source,
            "title": title,
            "url": url,
            "content": content,
            "named_entities": named_ents,
            "sentiment": sentiment,
            "risk_score": risk_score
        })
    return docs
