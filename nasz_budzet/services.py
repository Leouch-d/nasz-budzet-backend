import google.generativeai as genai
import os
import json
import traceback
from PIL import Image
import io

def przetworz_paragon_z_gemini(image_bytes):
    """
    Analizuje obraz paragonu za pomocą multimodalnego modelu Gemini,
    aby wyodrębnić kluczowe informacje o transakcji.

    Args:
        image_bytes (bytes): Surowe bajty pliku obrazu.

    Returns:
        dict: Słownik z wyodrębnionymi danymi ('opis', 'data', 'kwota')
              lub słownik z błędem.
    """
    if not os.getenv('GEMINI_API_KEY'):
        return {"error": "Brak klucza GEMINI_API_KEY w konfiguracji serwera."}

    try:
        img = Image.open(io.BytesIO(image_bytes))
        # Używamy modelu zoptymalizowanego pod kątem szybkości i wydajności.
        model = genai.GenerativeModel('gemini-1.5-flash')

        prompt = (
            "Jesteś precyzyjnym asystentem do analizy paragonów fiskalnych z Polski. "
            "Twoim zadaniem jest przeanalizowanie tego zdjęcia paragonu i wyodrębnienie z niego trzech informacji:\n"
            "1. Nazwa sprzedawcy/sklepu (np. 'Biedronka', 'Lidl sp. z o.o.', 'ORLEN S.A.').\n"
            "2. Data transakcji w formacie RRRR-MM-DD.\n"
            "3. Całkowita kwota do zapłaty (jako liczba, użyj kropki jako separatora dziesiętnego).\n\n"
            "Zwróć odpowiedź *wyłącznie* w formacie JSON, używając następujących kluczy: "
            "{\"opis\": \"<nazwa_sprzedawcy>\", \"data\": \"<data_RRRR-MM-DD>\", \"kwota\": <kwota_liczba>}.\n"
            "Jeśli którejś z informacji nie jesteś w stanie odczytać z absolutną pewnością, zwróć dla tego klucza wartość null. "
            "Nie dodawaj żadnych dodatkowych wyjaśnień ani formatowania, tylko czysty JSON."
        )

        response = model.generate_content([prompt, img])
        
        # Czasem AI opakowuje odpowiedź w bloki kodu markdown, więc je usuwamy.
        cleaned_response = response.text.strip().replace('```json', '').replace('```', '')
        
        print(f"Info AI (Paragon): Surowa odpowiedź Gemini: {cleaned_response}")

        parsed_json = json.loads(cleaned_response)
        return parsed_json

    except json.JSONDecodeError:
        traceback.print_exc()
        print(f"Błąd AI (Paragon): Nie udało się sparsować JSON z odpowiedzi: {cleaned_response}")
        return {"error": "AI zwróciło nieprawidłowy format danych."}
    except Exception as e:
        traceback.print_exc()
        print(f"BŁĄD AI (Paragon): Wystąpił problem podczas komunikacji z Gemini: {e}")
        return {"error": f"Wewnętrzny błąd serwera AI: {str(e)}"}


def kategoryzuj_z_gemini(opis_transakcji, typ_transakcji, dostepne_kategorie=None):
    """
    Wysyła opis transakcji do Gemini i prosi o przypisanie kategorii.
    Używa dynamicznej listy kategorii dostarczonej przez użytkownika.
    """
    if not os.getenv('GEMINI_API_KEY'):
        print("Ostrzeżenie: Brak klucza GEMINI_API_KEY. Używam kategorii domyślnej.")
        return "Inne" if typ_transakcji == 'wydatek' else "Inne przychody"

    if not dostepne_kategorie:
        # Domyślne kategorie na wypadek, gdyby lista nie została dostarczona
        if typ_transakcji == 'wydatek':
            dostepne_kategorie = ["Jedzenie", "Paliwo", "Raty i Podatki", "Inne", "Fastfoody", "Rozrywka", "Dzieci", "Ubrania", "Zdrowie i Uroda"]
        else:
            dostepne_kategorie = ["Wypłata", "Premia", "Sprzedaż", "Zwrot podatku", "Prezent", "Inne przychody"]

    lista_kategorii_str = ", ".join(f"'{k}'" for k in dostepne_kategorie)
    kategoria_domyslna = "Inne" if typ_transakcji == 'wydatek' else "Inne przychody"

    # --- POPRAWIONY PROMPT DO KATEGORYZACJI ---
    prompt = (
        f"Jesteś asystentem AI, którego zadaniem jest precyzyjna kategoryzacja transakcji finansowych. Na podstawie poniższego opisu transakcji, wybierz JEDNĄ, najbardziej pasującą kategorię z podanej listy.\n\n"
        f"**Opis transakcji:** \"{opis_transakcji}\"\n\n"
        f"**Dostępne kategorie:** [{lista_kategorii_str}]\n\n"
        f"Twoja odpowiedź musi być *dokładnie* jedną z nazw kategorii z powyższej listy. Nie dodawaj żadnych wyjaśnień, cytatów ani znaków interpunkcyjnych. Jeśli absolutnie żadna kategoria nie pasuje, zwróć słowo '{kategoria_domyslna}'."
    )

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)

        # Sprawdzanie, czy odpowiedź nie jest pusta
        if response.text:
            # Usuwamy ewentualne cudzysłowy i białe znaki
            sugerowana_kategoria = response.text.strip().replace("'", "").replace('"', '')
            
            # Sprawdzamy, czy zwrócona kategoria jest na liście dozwolonych
            if sugerowana_kategoria in dostepne_kategorie:
                print(f"Info AI: Gemini zasugerował kategorię '{sugerowana_kategoria}' dla opisu '{opis_transakcji}'.")
                return sugerowana_kategoria
            else:
                print(f"Ostrzeżenie AI: Gemini zwrócił nieznaną kategorię: '{sugerowana_kategoria}'. Używam '{kategoria_domyslna}'.")
                return kategoria_domyslna
        else:
             print(f"Ostrzeżenie AI: Gemini zwrócił pustą odpowiedź. Używam '{kategoria_domyslna}'.")
             return kategoria_domyslna

    except Exception as e:
        print(f"BŁĄD AI: Wystąpił problem podczas komunikacji z Gemini: {e}")
        traceback.print_exc()
        return f"{kategoria_domyslna} (błąd API)"
