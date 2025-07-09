import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # --- ZMODYFIKOWANA SEKCJA KONFIGURACJI BAZY DANYCH ---
    # Pobiera DATABASE_URL ze środowiska (np. z Railway).
    db_url = os.getenv('DATABASE_URL')
    
    # Jeśli zmienna istnieje (czyli jesteśmy na serwerze produkcyjnym jak Railway)
    if db_url:
        # Railway używa "postgres://" w URL, a SQLAlchemy wymaga "postgresql://"
        # Ta linia dokonuje niezbędnej zamiany.
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    
    # Ustawia URL bazy danych na ten z Railway. 
    # Jeśli go nie ma (bo uruchamiasz apkę lokalnie), użyje lokalnego pliku SQLite.
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url or 'sqlite:///' + os.path.join(basedir, '..', 'budzet.db')
    # --- KONIEC ZMODYFIKOWANEJ SEKCJI ---
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    CORS(app)
    db.init_app(app)

    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    if GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)

    from .routes import bp as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    with app.app_context():
        db.create_all()

    @app.route('/')
    def main_page():
        return "<h1>Serwer Menedżera Budżetu działa!</h1>"

    return app