# app.py (WERSJA Z POPRAWIONĄ I PANCERNĄ INTEGRACJĄ GEMINI)

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from config import Config
import os
import pandas as pd
import re
from datetime import datetime
import google.generativeai as genai

# --- Konfiguracja Aplikacji i Bazy Danych ---
app = Flask(__name__)
app.config.from_object(Config)

# Konfiguracja klucza API do Gemini z pliku .env
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("!!! OSTRZEŻENIE KRYTYCZNE: Nie znaleziono klucza GEMINI_API_KEY w pliku .env. Kategoryzacja AI będzie wyłączona.")

db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'budzet.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# --- Modele Bazy Danych (Definicja Tabel) ---
class Transakcja(db.Model):
    __tablename__ = 'transakcje'
    id = db.Column(db.Integer, primary_key=True)
    typ = db.Column(db.String(20), nullable=False)
    miesiac = db.Column(db.String(50), nullable=True)
    kategoria = db.Column(db.String(100), nullable=True)
    opis = db.Column(db.String(255), nullable=True)
    kwota = db.Column(db.Float, nullable=False)
    czy_liczony_do_budzetu = db.Column(db.Boolean, default=True, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'typ': self.typ,
            'miesiac': self.miesiac,
            'kategoria': self.kategoria,
            'opis': self.opis,
            'kwota': self.kwota,
            'czy_liczony_do_budzetu': self.czy_liczony_do_budzetu
        }

# --- Logika AI Gemini (NOWA, POPRAWIONA WERSJA) ---
def kategoryzuj_z_gemini(opis_wydatku):
    """
    Wysyła opis wydatku do Gemini i prosi o przypisanie kategorii.
    """
    if not GEMINI_API_KEY:
        return "Inne (brak klucza API)"

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        lista_kategorii = "Jedzenie, Paliwo, Raty i Podatki, Inne, Fastfoody, Rozrywka, Dzieci, Ubrania, Zdrowie i Uroda"
        prompt = f"""
        Jesteś ekspertem od finansów osobistych w Polsce. Twoim zadaniem jest przypisanie jednej, najbardziej pasującej kategorii do opisu wydatku.
        Masz do wyboru tylko i wyłącznie kategorie z tej listy: {lista_kategorii}.
        Oto opis wydatku: "{opis_wydatku}"
        Zwróć jako odpowiedź *tylko i wyłącznie* nazwę jednej kategorii z podanej listy. Bez żadnych dodatkowych słów i wyjaśnień.
        """
        
        response = model.generate_content(prompt)

        # --- NOWY, POPRAWNY SPOSÓB ODCZYTU ODPOWIEDZI ---
        if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
            sugerowana_kategoria = response.candidates[0].content.parts[0].text.strip()
            
            if sugerowana_kategoria in lista_kategorii.split(', '):
                print(f"Info AI: Gemini zasugerował kategorię '{sugerowana_kategoria}' dla opisu '{opis_wydatku}'.")
                return sugerowana_kategoria
            else:
                print(f"Ostrzeżenie AI: Gemini zwrócił nieznaną kategorię: '{sugerowana_kategoria}'. Używam 'Inne'.")
                return "Inne"
        else:
            # Jeśli odpowiedź jest pusta lub ma złą strukturę
            print("Ostrzeżenie AI: Gemini zwrócił pustą lub nieprawidłową odpowiedź. Używam 'Inne'.")
            return "Inne"
            
    except Exception as e:
        print(f"BŁĄD AI: Wystąpił problem podczas komunikacji z Gemini: {e}")
        return "Inne (błąd API)"


# --- API Endpoints (Adresy URL) ---
@app.route('/api')
def index():
    return jsonify({
        "message": "API do budżetu - Wersja z poprawioną integracją AI.",
        "version": "8.1.0 - AI POPRAWIONE"
    })

@app.route('/api/transakcje', methods=['GET', 'POST'])
def handle_transakcje():
    if request.method == 'GET':
        wszystkie_transakcje = Transakcja.query.order_by(Transakcja.id.desc()).all()
        return jsonify([transakcja.to_dict() for transakcja in wszystkie_transakcje])
    
    if request.method == 'POST':
        dane = request.get_json()
        if not dane or not 'typ' in dane or not 'kwota' in dane or not 'opis' in dane:
            return jsonify({'error': 'Brak wymaganych pól: typ, kwota, opis'}), 400

        kategoria_finalna = dane.get('kategoria')
        if dane['typ'] == 'wydatek' and not kategoria_finalna:
            kategoria_finalna = kategoryzuj_z_gemini(dane['opis'])
        
        try:
            nowa_transakcja = Transakcja(
                typ=dane['typ'],
                kwota=float(dane['kwota']),
                opis=dane['opis'],
                miesiac=dane.get('miesiac', datetime.now().strftime("%B")),
                kategoria=kategoria_finalna,
                czy_liczony_do_budzetu=dane.get('czy_liczony_do_budzetu', True)
            )
            db.session.add(nowa_transakcja)
            db.session.commit()
            return jsonify(nowa_transakcja.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": f"Wystąpił błąd podczas zapisu do bazy danych: {str(e)}"}), 500

@app.route('/api/transakcje/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_jedna_transakcja(id):
    transakcja = Transakcja.query.get_or_404(id)

    if request.method == 'GET':
        return jsonify(transakcja.to_dict())

    if request.method == 'PUT':
        dane = request.get_json()
        if not dane: return jsonify({'error': 'Brak danych do aktualizacji'}), 400
        
        transakcja.typ = dane.get('typ', transakcja.typ)
        transakcja.kwota = float(dane.get('kwota', transakcja.kwota))
        transakcja.opis = dane.get('opis', transakcja.opis)
        transakcja.miesiac = dane.get('miesiac', transakcja.miesiac)
        transakcja.kategoria = dane.get('kategoria', transakcja.kategoria)
        transakcja.czy_liczony_do_budzetu = dane.get('czy_liczony_do_budzetu', transakcja.czy_liczony_do_budzetu)
        
        db.session.commit()
        return jsonify(transakcja.to_dict())

    if request.method == 'DELETE':
        db.session.delete(transakcja)
        db.session.commit()
        return jsonify({'success': True, 'message': f'Transakcja o ID {id} została usunięta.'})

# Komenda import-db pozostaje bez zmian, ale jest tutaj dla kompletności
@app.cli.command("import-db")
def importuj_dane():
    # Kod importu...
    pass

# Uruchomienie aplikacji
if __name__ == '__main__':
    app.run(debug=True, port=5000)
