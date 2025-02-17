import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    # Указываем SQLite в качестве базы данных
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.dirname(__file__), 'planner.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False