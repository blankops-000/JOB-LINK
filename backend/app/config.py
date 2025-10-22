import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_default_secret_key'
    DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///site.db'
    DEBUG = os.environ.get('DEBUG', 'False') == 'True'
    TESTING = os.environ.get('TESTING', 'False') == 'True'