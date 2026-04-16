from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

class Admin(db.Model):
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    @classmethod
    def create(cls, username, password):
        hashed_pw = generate_password_hash(password)
        new_admin = cls(username=username, password_hash=hashed_pw)
        db.session.add(new_admin)
        db.session.commit()
        return new_admin

    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def change_password(self, new_password):
        self.password_hash = generate_password_hash(new_password)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
