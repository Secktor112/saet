from flask_login import UserMixin

from app import db, manager
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


# class Users(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(50), unique=True)
#     email = db.Column(db.String(50), unique=True)
#     psw = db.Column(db.String(500), nullable=False)
#     date = db.Column(db.DateTime, default=datetime.utcnow)
#
#     def __repr__(self):
#         return '<Users %r>' % self.id
#
#
# class Profiles(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), nullable=False)
#     email = db.Column(db.String(50), unique=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#
#     def __repr__(self):
#         return '<Profiles %r>' % self.id


class User (db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True)
    role = db.Column(db.Integer, default=0)
    image = db.Column(db.String(256), default='static/css/images/2.png')


class Instruments (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('type.id'))
    family_id = db.Column(db.Integer, db.ForeignKey('family.id'))
    photo = db.Column(db.String(300))
    price = db.Column(db.Numeric(7, 2), nullable=False)
    options = db.Column(db.String(128), nullable=False, default='base')
    vendor = db.Column(db.String(300), nullable=False, default='noname')
    disc = db.Column(db.Text)


class Type (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    name_ru = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return '<Type %r>' % self.id


class Family (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    name_ru = db.Column(db.String(128), nullable=False)


class Cart (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    inst_id = db.Column(db.Integer, db.ForeignKey('instruments.id'))

    def __repr__(self):
        return '<Cart %r>' % self.id

    def commit(self):
        try:
            db.session.commit()
            self.success = True
            return True
        except:
            self.success = False
            return False

    def delete(self):
        db.session.delete(self)
        self.commit()


@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)