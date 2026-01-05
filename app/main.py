from fastapi import FastAPI
import os
import psycopg2
from dotenv import load_dotenv
from pydantic import BaseModel
from datetime import date
from typing import Optional
from fastapi import Query

load_dotenv()

app = FastAPI(title="Event Discovery API")

class EventCreate(BaseModel):
    name: str
    location: str
    date: date

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
def get_events(
    location: Optional[str] = None,
    after: Optional[str] = None,
):
    conn = get_conn()
    try:
        cur = conn.cursor()
        query = "SELECT id, name, location, date FROM events WHERE 1=1"
        params = []

        if location:
            query += " AND location = %s"
            params.append(location)

        if after:
            query += " AND date >= %s"
            params.append(after)

        query += " ORDER BY date ASC"

        cur.execute(query, params)
        rows = cur.fetchall()

        return [
            {"id": r[0], "name": r[1], "location": r[2], "date": r[3].isoformat()}
            for r in rows
        ]
    finally:
        conn.close()

@app.post("/events")
def create_event(event: EventCreate):
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO events (name, location, date) VALUES (%s, %s, %s)",
            (event.name, event.location, event.date),
        )
        conn.commit()
        return {"status": "created"}
    finally:
        conn.close()
