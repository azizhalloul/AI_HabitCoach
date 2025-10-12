"""
storage.py — Local SQL storage for AI Habit Coach

What this module does:
----------------------------------------
This module manages the local database that stores all user entries.

Each entry contains:
- timestamp (when the reflection was submitted)
- text (user's journal text)
- text_emotion (emotion detected from text)
- face_emotion (emotion detected from face, if any)
- mood_score (combined mood number)
- feedback (the message generated for the user)

It uses SQLite for local storage and SQLAlchemy ORM to interact with the database.
SQLite is chosen for:
Simplicity — no external database server needed
Privacy — stays 100% on your machine
Scalability — easy to query and extend later

----------------------------------------
"""

"""
storage.py
-----------
This module handles all data persistence for the AI Habit Coach app.

It uses SQLAlchemy with a local SQLite database (entries.db) to store:
- timestamp (when the user made an entry)
- text (journal content)
- text_emotion (JSON string from NLP analysis)
- face_emotion (JSON string from facial emotion detection)
- mood_score (numerical combined mood score)
- feedback (AI-generated message)

All data is stored locally for privacy — nothing is sent to the cloud.
"""

from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, Float, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
import os
import json  # <-- important for safely storing dicts as strings

# -------------------------------------------------------------------------
# 1️⃣ Database setup
# -------------------------------------------------------------------------

# Create a data directory if it doesn’t exist (local, privacy-first)
os.makedirs("data", exist_ok=True)

# Define where our local database lives
DB_PATH = os.path.join("data", "entries.db")

# Create a database engine (SQLite = file-based, very lightweight)
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)

# Base class for SQLAlchemy models
Base = declarative_base()


# -------------------------------------------------------------------------
# 2️⃣ Define the database model (table schema)
# -------------------------------------------------------------------------

class Entry(Base):
    """
    Represents a single user journal entry and emotional analysis.
    """
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.now)
    text = Column(Text)
    text_emotion = Column(Text)  # stored as JSON string
    face_emotion = Column(Text)  # stored as JSON string
    mood_score = Column(Float)
    feedback = Column(Text)


# -------------------------------------------------------------------------
# 3️⃣ Initialize the database
# -------------------------------------------------------------------------

Base.metadata.create_all(engine)

# Create a session factory (so we can write/read entries)
Session = sessionmaker(bind=engine)


# -------------------------------------------------------------------------
# 4️⃣ Save a new entry (called by the Streamlit app)
# -------------------------------------------------------------------------

def save_entry(text, feedback_obj, fusion_result, text_result, face_result):
    """
    Saves a new journal entry to the database.

    - text_result and face_result are dicts → we serialize them to JSON strings.
    - fusion_result contains the mood_score (a float).
    - feedback_obj contains the AI-generated message.
    """
    session = Session()
    try:
        entry = Entry(
            timestamp=datetime.now(),
            text=text,
            text_emotion=json.dumps(text_result),  # dict → JSON string
            face_emotion=json.dumps(face_result),  # dict → JSON string
            mood_score=float(fusion_result.get("mood_score", 0.0)),
            feedback=feedback_obj.get("message", "")
        )

        session.add(entry)
        session.commit()
        print("✅ Entry saved successfully!")
    except Exception as e:
        print("❌ Error saving entry:", e)
        session.rollback()
    finally:
        session.close()


# -------------------------------------------------------------------------
# 5️⃣ Read all saved entries (used to display trends)
# -------------------------------------------------------------------------

def load_entries():
    """
    Loads all previous journal entries from the database.
    Returns a list of Entry objects (most recent first).
    """
    session = Session()
    entries = session.query(Entry).order_by(Entry.timestamp.desc()).all()
    session.close()
    return entries
