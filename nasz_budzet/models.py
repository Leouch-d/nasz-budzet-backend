from . import db
from datetime import datetime

# Usunięto ręczne definicje sekwencji, ponieważ SQLAlchemy
# i sterownik psycopg2 automatycznie zarządzają tym w PostgreSQL,
# gdy 'id = db.Column(db.Integer, primary_key=True)'.

class Kategoria(db.Model):
    """
    Model reprezentujący kategorię wydatku lub przychodu.
    """
    __tablename__ = 'kategorie'
    
    # Uproszczona definicja klucza głównego.
    # SQLAlchemy automatycznie skonfiguruje auto-inkrementację (SERIAL) w PostgreSQL.
    id = db.Column(db.Integer, primary_key=True)
    nazwa = db.Column(db.String(100), nullable=False, unique=True)
    typ = db.Column(db.String(20), nullable=False) # 'wydatek' lub 'przychód'

    def to_dict(self):
        """Konwertuje obiekt kategorii na słownik."""
        return {
            'id': self.id,
            'nazwa': self.nazwa,
            'typ': self.typ,
        }

class Transakcja(db.Model):
    """
    Model reprezentujący pojedynczą transakcję finansową.
    """
    __tablename__ = 'transakcje'

    # Uproszczona definicja klucza głównego.
    id = db.Column(db.Integer, primary_key=True)
    typ = db.Column(db.String(20), nullable=False)
    miesiac = db.Column(db.String(7), nullable=False) 
    kategoria = db.Column(db.String(100), nullable=True)
    opis = db.Column(db.String(255), nullable=True)
    kwota = db.Column(db.Float, nullable=False)
    data_transakcji = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    uzytkownik = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        """Konwertuje obiekt transakcji na słownik (JSON)."""
        return {
            'id': self.id,
            'typ': self.typ,
            'miesiac': self.miesiac,
            'kategoria': self.kategoria,
            'opis': self.opis,
            'kwota': self.kwota,
            'data_transakcji': self.data_transakcji.isoformat(),
            'uzytkownik': self.uzytkownik
        }

class KategoriaLimit(db.Model):
    """
    Model reprezentujący limit wydatków dla danej kategorii.
    """
    __tablename__ = 'kategoria_limit'
    kategoria = db.Column(db.String(100), primary_key=True)
    limit = db.Column(db.Float, nullable=False)
    
    def to_dict(self): 
        """Konwertuje obiekt limitu na słownik."""
        return {'kategoria': self.kategoria, 'limit': self.limit}

class SzablonTransakcji(db.Model):
    """
    Model reprezentujący szablon dla transakcji cyklicznych.
    """
    __tablename__ = 'szablony_transakcji'

    # Uproszczona definicja klucza głównego.
    id = db.Column(db.Integer, primary_key=True)
    typ = db.Column(db.String(20), nullable=False)
    kategoria = db.Column(db.String(100), nullable=False)
    opis = db.Column(db.String(255), nullable=False)
    kwota = db.Column(db.Float, nullable=False)
    
    def to_dict(self): 
        """Konwertuje obiekt szablonu na słownik."""
        return { 
            'id': self.id, 
            'typ': self.typ, 
            'kategoria': self.kategoria, 
            'opis': self.opis, 
            'kwota': self.kwota 
        }
