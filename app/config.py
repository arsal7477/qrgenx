import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    FLASK_ENV = os.environ.get('FLASK_ENV') or 'development'
    FLASK_APP = 'app.py'
