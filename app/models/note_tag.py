from . import db

class NoteTag(db.Model):
    __tablename__ = 'note_tags'

    note_id = db.Column(db.Integer, db.ForeignKey('notes.id', ondelete='CASCADE'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True)

    @classmethod
    def create(cls, note_id, tag_id):
        new_relation = cls(note_id=note_id, tag_id=tag_id)
        db.session.add(new_relation)
        db.session.commit()
        return new_relation

    @classmethod
    def delete_relation(cls, note_id, tag_id):
        relation = cls.query.filter_by(note_id=note_id, tag_id=tag_id).first()
        if relation:
            db.session.delete(relation)
            db.session.commit()
            return True
        return False
