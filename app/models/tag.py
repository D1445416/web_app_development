from . import db

class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(20), nullable=True)

    @classmethod
    def create(cls, name, color=None):
        new_tag = cls(name=name, color=color)
        db.session.add(new_tag)
        db.session.commit()
        return new_tag

    @classmethod
    def get_all(cls):
        return cls.query.order_by(cls.name).all()

    @classmethod
    def get_by_id(cls, tag_id):
        return cls.query.get(tag_id)

    def update(self, name=None, color=None):
        if name is not None:
            self.name = name
        if color is not None:
            self.color = color
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
