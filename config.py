# Opis: Plik konfiguracyjny aplikacji.
# ======================================================================
import os
from dotenv import load_dotenv

# Wczytuje zmienne z pliku .env
load_dotenv()

class Config:
    """Główna klasa konfiguracyjna."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-tajny-klucz-ktorego-nikt-nie-zgadnie'
    # W przyszłości dodamy tutaj np. dane do połączenia z bazą danych.
