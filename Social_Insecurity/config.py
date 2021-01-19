import os

# contains application-wide configuration, and is loaded in __init__.py

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret' # TODO: Use this with wtforms
    RECAPTCHA_PUBLIC_KEY = '6LdyfLwUAAAAAKlqTAeLbknwi9yo9_MLxWyZM2dt'
    RECAPTCHA_PRIVATE_KEY ='6LdyfLwUAAAAAN3RqGyH5MM66hby5eTCHyoAVtAb'
    DATABASE = 'database.db'
    UPLOAD_PATH = 'app/static/uploads'
    ALLOWED_EXTENSIONS = {} 