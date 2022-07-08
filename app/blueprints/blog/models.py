from app import db
from datetime import datetime


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title= db.Column(db.String(200))
    content = db.Column(db.String(300))
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow )
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<Post {self.id}|{self.title}>"

    def to_dict(self):
        from app.blueprints.auth.models import User
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'date_created': self.date_created,
            'author': User.query.get(self.user_id).to_dict()
        }

    def update(self, data):
        for field in data:
            if field not in {'title', 'content', 'user_id'}:
                continue
            setattr(self, field, data[field])
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        