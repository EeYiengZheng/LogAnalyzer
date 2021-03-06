import os
from secret import secret_key

basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = secret_key

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False

ALLOWED_EXTENSIONS = ['log', 'zip']  # <-- don't know where to put this? config.py
UPLOAD_FOLDER = 'uploads'
ANALYZED_CSV_FOLDER = 'analyzed'
