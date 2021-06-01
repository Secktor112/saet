from flask import session, render_template
from app import db
from models import User
from enum import Enum


def get_template(template, **kwargs):
    if session['userid']:
        return render_template(template, prof=True, **kwargs)
    return render_template(template, prof=False, **kwargs)


def get_role(id):
    user = User.query.filter_by(id=id).first()
    if user:
        return user.role
    return -1


class Inst_type(Enum):
    GUITAR = 'Guitar'
    UKULELE = 'Ukulele'
    PIANO = 'Piano'
    VIOLIN = 'Violin'

    # def get_type(self, type):
    #     if type == 'Гитара':
    #         return Inst_type.GUITAR
    #
    #     if type == 'Укулеле':
    #         return Inst_type.UKULELE
    #
    #     if type == 'Фортепиано':
    #         return Inst_type.PIANO
    #
    #     if type == 'Скрипка':
    #         return Inst_type.VIOLIN


class Inst_family(Enum):
    STRINGS = 'Strings'
    KEYBOARDS = 'Keyboard'
    WINDS = 'Winds'
    PERCUSSION = 'Percussion'
    STRINGED_BOWED = 'Stringed Bowed'

