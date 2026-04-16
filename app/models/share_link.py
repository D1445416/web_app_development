from datetime import datetime, timezone
import uuid
from . import db

class ShareLink(db.Model):
    __tablename__ = 'share_links'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    note_id = db.Column(db.Integer, db.ForeignKey('notes.id', ondelete='CASCADE'), nullable=False)
    token = db.Column(db.String(255), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    permission = db.Column(db.String(20), nullable=False) # 'edit' or 'read'
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    @classmethod
    def create(cls, note_id, permission):
        new_link = cls(note_id=note_id, permission=permission)
        db.session.add(new_link)
        db.session.commit()
        return new_link

    @classmethod
    def get_by_token(cls, token):
        return cls.query.filter_by(token=token).first()

    @classmethod
    def get_all(cls):
        return cls.query.order_by(cls.created_at.desc()).all()

    def update_permission(self, permission):
        self.permission = permission
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
