from app import db
from datetime import datetime


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    success = True

    def __repr__(self):
        return '<Article %r>' % self.id

    def commit(self):
        try:
            db.session.commit()
            self.success = True
            return True
        except:
            self.success = False
            return False

    def update(self, title, intro, text):
        self.title = title
        self.intro = intro
        self.text = text

        return self.commit()

    def create(self):
        db.session.add(self)
        return self.commit()

    def delete(self):
        db.session.delete(self)
        self.commit()


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50), unique=True)
    psw = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Users %r>' % self.id


class Profiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer)
    city = db.Column(db.String(100))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Profiles %r>' % self.id