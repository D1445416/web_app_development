from datetime import datetime, timezone
from . import db

class Subject(db.Model):
    __tablename__ = 'subjects'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationship
    notes = db.relationship('Note', backref='subject', lazy=True, cascade='all, delete-orphan')

    @classmethod
    def create(cls, name):
        new_subject = cls(name=name)
        db.session.add(new_subject)
        db.session.commit()
        return new_subject

    @classmethod
    def get_all(cls):
        return cls.query.order_by(cls.created_at.desc()).all()

    @classmethod
    def get_by_id(cls, subject_id):
        return cls.query.get(subject_id)

    def update(self, name):
        self.name = name
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
