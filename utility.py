from flask import session, render_template
from app import db
from models import User


def get_template(template, **kwargs):
    if session['userid']:
        return render_template(template, prof=True, **kwargs)
    return render_template(template, prof=False, **kwargs)


def get_role(id):
    user = User.query.filter_by(id=id).first()
    if user:
        return user.role
    return -1

