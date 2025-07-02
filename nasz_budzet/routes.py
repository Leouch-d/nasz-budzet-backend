from flask import Blueprint, request, jsonify, make_response
from sqlalchemy import distinct
from sqlalchemy.sql import func 
from . import db
from .models import Transakcja, KategoriaLimit, SzablonTransakcji, Kategoria
from .services import kategoryzuj_z_gemini, przetworz_paragon_z_gemini
from datetime import datetime
from collections import defaultdict
import traceback
import pandas as pd
import io
import json

bp = Blueprint('api', __name__)

# ... (endpointy scan-receipt, export, kategorie, transakcje bez zmian) ...
@bp.route('/scan-receipt', methods=['POST'])
def scan_receipt():
    if 'file' not in request.files:
        return jsonify({"error": "Brak pliku w żądaniu"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Nie wybrano pliku"}), 400
    if file:
        try:
            image_bytes = file.read()
            wynik_analizy = przetworz_paragon_z_gemini(image_bytes)
            if 'error' in wynik_analizy:
                return jsonify(wynik_analizy), 500
            return jsonify(wynik_analizy), 200
        except Exception as e:
            traceback.print_exc()
            return jsonify({"error": f"Wewnętrzny błąd serwera podczas przetwarzania obrazu: {str(e)}"}), 500

@bp.route('/export', methods=['GET'])
def export_transactions():
    try:
        transakcje = Transakcja.query.order_by(Transakcja.data_transakcji.asc()).all()
        if not transakcje:
            return jsonify({"error": "Brak transakcji do wyeksportowania"}), 404
        transakcje_lista = [t.to_dict() for t in transakcje]
        df = pd.DataFrame(transakcje_lista)
        df_export = df[['data_transakcji', 'typ', 'kategoria', 'opis', 'kwota', 'uzytkownik']]
        df_export.rename(columns={
            'data_transakcji': 'Data', 'typ': 'Typ', 'kategoria': 'Kategoria',
            'opis': 'Opis', 'kwota': 'Kwota (PLN)', 'uzytkownik': 'Użytkownik'
        }, inplace=True)
        output = io.StringIO()
        df_export.to_csv(output, index=False, encoding='utf-8-sig', sep=';')
        csv_data = output.getvalue()
        response = make_response(csv_data)
        response.headers["Content-Disposition"] = "attachment; filename=transakcje.csv"
        response.headers["Content-type"] = "text/csv; charset=utf-8-sig"
        return response
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": f"Wewnętrzny błąd serwera podczas eksportu: {str(e)}"}), 500

@bp.route('/kategorie', methods=['GET', 'POST'])
def handle_kategorie():
    if request.method == 'GET':
        try:
            kategorie_z_tabeli = {k.nazwa: k for k in Kategoria.query.all()}
            kategorie_z_transakcji = db.session.query(distinct(Transakcja.kategoria)).all()
            for kat_tuple in kategorie_z_transakcji:
                nazwa_kat = kat_tuple[0]
                if nazwa_kat and nazwa_kat not in kategorie_z_tabeli:
                    pass
            finalna_lista = sorted(list(kategorie_z_tabeli.values()), key=lambda x: (x.typ, x.nazwa))
            return jsonify([k.to_dict() for k in finalna_lista])
        except Exception as e:
            return jsonify({"error": f"Błąd bazy danych: {str(e)}"}), 500
    if request.method == 'POST':
        dane = request.get_json()
        if not dane or 'nazwa' not in dane or 'typ' not in dane:
            return jsonify({'error': 'Brakuje pól "nazwa" lub "typ"'}), 400
        istniejaca = Kategoria.query.filter_by(nazwa=dane['nazwa']).first()
        if istniejaca:
            return jsonify({'error': f'Kategoria "{dane["nazwa"]}" już istnieje.'}), 409
        nowa_kategoria = Kategoria(nazwa=dane['nazwa'], typ=dane['typ'])
        db.session.add(nowa_kategoria)
        db.session.commit()
        return jsonify(nowa_kategoria.to_dict()), 201

@bp.route('/kategorie/<int:kategoria_id>', methods=['DELETE'])
def handle_jedna_kategoria(kategoria_id):
    kategoria = Kategoria.query.get_or_404(kategoria_id)
    try:
        db.session.delete(kategoria)
        db.session.commit()
        return jsonify({'message': f'Kategoria {kategoria_id} usunięta'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Błąd bazy danych podczas usuwania: {str(e)}"}), 500

@bp.route('/transakcje', methods=['GET', 'POST'])
def handle_transakcje():
    if request.method == 'GET':
        wszystkie_transakcje = Transakcja.query.order_by(Transakcja.data_transakcji.desc()).all()
        return jsonify([t.to_dict() for t in wszystkie_transakcje])
    if request.method == 'POST':
        dane = request.get_json()
        if not dane or not all(k in dane for k in ['typ', 'kwota', 'opis', 'uzytkownik']):
            return jsonify({'error': 'Brakuje wymaganych pól (typ, kwota, opis, uzytkownik)'}), 400
        data_transakcji_obj = datetime.utcnow()
        if 'data_transakcji' in dane and dane['data_transakcji']:
            try:
                data_transakcji_obj = datetime.fromisoformat(dane['data_transakcji'].replace('Z', '+00:00'))
            except (ValueError, TypeError):
                data_transakcji_obj = datetime.utcnow()
        nowy_miesiac = data_transakcji_obj.strftime("%Y-%m")
        try:
            istniejaca_transakcja_w_miesiacu = Transakcja.query.filter(func.strftime('%Y-%m', Transakcja.data_transakcji) == nowy_miesiac).first()
            if not istniejaca_transakcja_w_miesiacu:
                szablony = SzablonTransakcji.query.all()
                for szablon in szablony:
                    data_dla_cyklicznej = datetime(data_transakcji_obj.year, data_transakcji_obj.month, 1)
                    nowy_automat = Transakcja(typ=szablon.typ, kwota=szablon.kwota, opis=szablon.opis, miesiac=nowy_miesiac, kategoria=szablon.kategoria, data_transakcji=data_dla_cyklicznej, uzytkownik="System" )
                    db.session.add(nowy_automat)
            kategorie_dla_ai = [k.nazwa for k in Kategoria.query.filter_by(typ=dane['typ']).all()]
            kategoria_finalna = kategoryzuj_z_gemini(dane['opis'], dane['typ'], kategorie_dla_ai)
            nowa_transakcja = Transakcja(typ=dane['typ'], kwota=float(dane['kwota']), opis=dane['opis'], miesiac=nowy_miesiac, kategoria=kategoria_finalna, uzytkownik=dane['uzytkownik'], data_transakcji=data_transakcji_obj)
            db.session.add(nowa_transakcja)
            db.session.commit()
            return jsonify(nowa_transakcja.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            traceback.print_exc()
            return jsonify({"error": f"Wewnętrzny błąd serwera: {str(e)}"}), 500

@bp.route('/transakcje/<int:transakcja_id>', methods=['DELETE', 'PUT'])
def handle_jedna_transakcja(transakcja_id):
    transakcja = Transakcja.query.get_or_404(transakcja_id)
    if request.method == 'DELETE':
        try:
            db.session.delete(transakcja)
            db.session.commit()
            return jsonify({'message': f'Transakcja {transakcja_id} usunięta'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": f"Błąd bazy danych: {str(e)}"}), 500
    if request.method == 'PUT':
        dane = request.get_json()
        if not dane:
            return jsonify({'error': 'Brak danych do aktualizacji'}), 400
        try:
            if 'opis' in dane and transakcja.opis != dane.get('opis') and 'kategoria' not in dane:
                kategorie_dla_ai = [k.nazwa for k in Kategoria.query.filter_by(typ=transakcja.typ).all()]
                transakcja.kategoria = kategoryzuj_z_gemini(dane['opis'], transakcja.typ, kategorie_dla_ai)
            elif 'kategoria' in dane:
                transakcja.kategoria = dane['kategoria']
            transakcja.opis = dane.get('opis', transakcja.opis)
            transakcja.kwota = float(dane.get('kwota', transakcja.kwota))
            if 'data_transakcji' in dane and dane['data_transakcji']:
                nowa_data = datetime.fromisoformat(dane['data_transakcji'].replace('Z', '+00:00'))
                transakcja.data_transakcji = nowa_data
                transakcja.miesiac = nowa_data.strftime("%Y-%m")
            transakcja.uzytkownik = dane.get('uzytkownik', transakcja.uzytkownik)
            db.session.commit()
            return jsonify(transakcja.to_dict()), 200
        except Exception as e:
            db.session.rollback()
            traceback.print_exc()
            return jsonify({"error": f"Wewnętrzny błąd serwera: {str(e)}"}), 500

@bp.route('/financial_summary', methods=['GET'])
def financial_summary():
    try:
        wszystkie_transakcje = Transakcja.query.order_by(Transakcja.miesiac.asc()).all()
        
        # ZMIANA: Uproszczona struktura danych, bez podziału na użytkowników
        miesieczne_dane = defaultdict(lambda: {
            'przychody': 0.0,
            'wydatki': 0.0,
            'wydatkiKategorie': defaultdict(float)
        })

        for t in wszystkie_transakcje:
            if t.typ == 'przychód':
                miesieczne_dane[t.miesiac]['przychody'] += t.kwota
            else:
                miesieczne_dane[t.miesiac]['wydatkiKategorie'][t.kategoria] += t.kwota
                miesieczne_dane[t.miesiac]['wydatki'] += t.kwota
        
        posortowane_miesiace = sorted(miesieczne_dane.keys())
        finalne_podsumowanie = {}
        saldo_poprzedniego_miesiaca = 0.0
        
        for miesiac in posortowane_miesiace:
            dane = miesieczne_dane[miesiac]
            bilans_miesiaca = dane['przychody'] - dane['wydatki']
            saldo_na_koniec_miesiaca = saldo_poprzedniego_miesiaca + bilans_miesiaca
            
            # ZMIANA: Usunięto podsumowanie per użytkownik, zwracamy czystsze dane
            finalne_podsumowanie[miesiac] = {
                'bilansOtwarcia': round(saldo_poprzedniego_miesiaca, 2),
                'przychody': round(dane['przychody'], 2),
                'wydatki': round(dane['wydatki'], 2),
                'bilansMiesiaca': round(bilans_miesiaca, 2),
                'wydatkiKategorie': [{'kategoria': k, 'suma': round(v, 2)} for k, v in sorted(dane['wydatkiKategorie'].items())],
                'saldoMiesiaca': round(saldo_na_koniec_miesiaca, 2),
            }
            saldo_poprzedniego_miesiaca = saldo_na_koniec_miesiaca
        return jsonify(finalne_podsumowanie)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@bp.route('/limity', methods=['GET', 'POST'])
def handle_limity():
    if request.method == 'GET':
        limity = KategoriaLimit.query.all()
        return jsonify({limit.kategoria: limit.limit for limit in limity})
    if request.method == 'POST':
        dane = request.get_json()
        if not dane or 'kategoria' not in dane or 'limit' not in dane:
            return jsonify({'error': 'Brakuje pól "kategoria" lub "limit"'}), 400
        limit = KategoriaLimit.query.filter_by(kategoria=dane['kategoria']).first()
        if limit:
            limit.limit = float(dane['limit'])
        else:
            limit = KategoriaLimit(kategoria=dane['kategoria'], limit=float(dane['limit']))
            db.session.add(limit)
        db.session.commit()
        return jsonify(limit.to_dict()), 201

@bp.route('/szablony', methods=['GET', 'POST'])
def handle_szablony():
    if request.method == 'GET':
        szablony = SzablonTransakcji.query.all()
        return jsonify([s.to_dict() for s in szablony])
    if request.method == 'POST':
        dane = request.get_json()
        if not all(k in dane for k in ['typ', 'kategoria', 'opis', 'kwota']):
            return jsonify({'error': 'Brakuje wymaganych pól'}), 400
        nowy_szablon = SzablonTransakcji(typ=dane['typ'], kategoria=dane['kategoria'], opis=dane['opis'], kwota=float(dane['kwota']))
        db.session.add(nowy_szablon)
        db.session.commit()
        return jsonify(nowy_szablon.to_dict()), 201

@bp.route('/szablony/<int:szablon_id>', methods=['DELETE'])
def delete_szablon(szablon_id):
    szablon = SzablonTransakcji.query.get_or_404(szablon_id)
    db.session.delete(szablon)
    db.session.commit()
    return jsonify({'message': 'Szablon usunięty'}), 200
