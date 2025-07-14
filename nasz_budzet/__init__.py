import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
import google.generativeai as genai
from sqlalchemy import text # Ważny import, aby móc wykonać surowy SQL

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # --- Konfiguracja bazy danych (bez zmian) ---
    db_url = os.getenv('DATABASE_URL')
    if db_url:
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url or 'sqlite:///' + os.path.join(basedir, '..', 'budzet.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    CORS(app)
    db.init_app(app)

    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    if GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)

    # --- TYMCZASOWY SKRYPT NAPRAWCZY ---
    # Ten kod uruchomi się raz, aby naprawić sekwencje w bazie danych.
    # Po jednym udanym wdrożeniu, ten cały blok od "with app.app_context():"
    # do "db.create_all()" powinien zostać usunięty!
    with app.app_context():
        # Sprawdzamy, czy na pewno łączymy się z bazą PostgreSQL
        if db.engine.url.drivername == 'postgresql':
            print("INFO: Wykryto PostgreSQL. Uruchamiam jednorazowy skrypt naprawczy dla sekwencji...")
            try:
                # Definiujemy nasz skrypt SQL do wykonania
                sql_script = """
                CREATE SEQUENCE IF NOT EXISTS kategorie_id_seq;
                ALTER TABLE kategorie ALTER COLUMN id SET DEFAULT nextval('kategorie_id_seq');
                SELECT setval('kategorie_id_seq', COALESCE((SELECT MAX(id) FROM kategorie) + 1, 1), false);

                CREATE SEQUENCE IF NOT EXISTS transakcje_id_seq;
                ALTER TABLE transakcje ALTER COLUMN id SET DEFAULT nextval('transakcje_id_seq');
                SELECT setval('transakcje_id_seq', COALESCE((SELECT MAX(id) FROM transakcje) + 1, 1), false);

                CREATE SEQUENCE IF NOT EXISTS szablony_transakcji_id_seq;
                ALTER TABLE szablony_transakcji ALTER COLUMN id SET DEFAULT nextval('szablony_transakcji_id_seq');
                SELECT setval('szablony_transakcji_id_seq', COALESCE((SELECT MAX(id) FROM szablony_transakcji) + 1, 1), false);
                """
                # Wykonujemy skrypt i zatwierdzamy zmiany
                db.session.execute(text(sql_script))
                db.session.commit()
                print("INFO: Skrypt naprawczy wykonany pomyślnie!")
            except Exception as e:
                print(f"BŁĄD podczas wykonywania skryptu naprawczego: {e}")
                db.session.rollback()
        
        # To polecenie tworzy tabele, jeśli nie istnieją.
        # Jest nieszkodliwe i może zostać.
        db.create_all()
    # --- KONIEC TYMCZASOWEGO SKRYPTU NAPRAWCZEGO ---

    from .routes import bp as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    @app.route('/')
    def main_page():
        return "<h1>Serwer Menedżera Budżetu działa!</h1>"

    return app
