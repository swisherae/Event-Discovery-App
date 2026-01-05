from pydantic import BaseModel
from datetime import date

class EventCreate(BaseModel):
    name: str
    location: str
    date: date
