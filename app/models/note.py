from datetime import datetime, timezone
from . import db
from .note_tag import NoteTag # Import for relationship if needed

class Note(db.Model):
    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationship
    share_links = db.relationship('ShareLink', backref='note', lazy=True, cascade='all, delete-orphan')
    tags = db.relationship('Tag', secondary='note_tags', backref=db.backref('notes', lazy='dynamic'))

    @classmethod
    def create(cls, subject_id, title, content=''):
        new_note = cls(subject_id=subject_id, title=title, content=content)
        db.session.add(new_note)
        db.session.commit()
        return new_note

    @classmethod
    def get_all(cls):
        return cls.query.order_by(cls.created_at.desc()).all()

    @classmethod
    def get_by_id(cls, note_id):
        return cls.query.get(note_id)

    def update(self, title=None, content=None):
        if title is not None:
            self.title = title
        if content is not None:
            self.content = content
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
