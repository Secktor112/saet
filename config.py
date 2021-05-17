class Configuration(object):
    DEBUG       = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://secktor:123321@localhost/saet'
    SECRET_KEY = 'secret aga'