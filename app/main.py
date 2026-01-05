from fastapi import FastAPI
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Event Discovery API")


def get_conn():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
    )


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/events")
def get_events():
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, name, location, date FROM events ORDER BY date ASC;")
        rows = cur.fetchall()
        return [
            {"id": r[0], "name": r[1], "location": r[2], "date": r[3].isoformat()}
            for r in rows
        ]
    finally:
        conn.close()
