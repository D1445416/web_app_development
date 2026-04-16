from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Ensure we import all models so SQLAlchemy knows about them
from .subject import Subject
from .note import Note
from .tag import Tag
from .note_tag import NoteTag
from .share_link import ShareLink
from .admin import Admin
