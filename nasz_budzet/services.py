import google.generativeai as genai
import os
import json
import traceback
from PIL import Image
import io

# NOWA FUNKCJA DO PRZETWARZANIA PARAGONÓW
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
        # Załaduj obraz z bajtów
        img = Image.open(io.BytesIO(image_bytes))

        # Używamy najnowszego, potężnego modelu multimodalnego
        model = genai.GenerativeModel('gemini-2.5-flash')

        # Precyzyjne polecenie dla AI, proszące o zwrotkę w formacie JSON
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

        # Wyślij obraz i polecenie do Gemini
        response = model.generate_content([prompt, img])

        # Wyczyść odpowiedź i spróbuj sparsować JSON
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
        return "Inne" if typ_transakcji == 'wydatek' else "Inne przychody"

    if not dostepne_kategorie:
        if typ_transakcji == 'wydatek':
            dostepne_kategorie = ["Jedzenie", "Paliwo", "Raty i Podatki", "Inne", "Fastfoody", "Rozrywka", "Dzieci", "Ubrania", "Zdrowie i Uroda"]
        else:
            dostepne_kategorie = ["Wypłata", "Premia", "Sprzedaż", "Zwrot podatku", "Prezent", "Inne przychody"]

    lista_kategorii_str = ", ".join(dostepne_kategorie)
    kategoria_domyslna = "Inne" if typ_transakcji == 'wydatek' else "Inne przychody"

    prompt = (
            "Jesteś precyzyjnym asystentem do analizy paragonów fiskalnych z Polski. "
            "Twoim zadaniem jest przeanalizowanie tego zdjęcia paragonu i wyodrębnienie z niego trzech informacji:\n"
            "1. Nazwa sprzedawcy/sklepu (np. 'Biedronka', 'Lidl sp. z o.o.', 'ORLEN S.A.'). To najważniejsza informacja, postaraj się ją znaleźć.\n"
            "2. Data transakcji w formacie RRRR-MM-DD. Jeśli znajdziesz datę w innym formacie, przekonwertuj ją.\n"
            "3. Całkowita kwota do zapłaty (jako liczba, użyj kropki jako separatora dziesiętnego). Szukaj słów kluczowych 'SUMA', 'RAZEM', 'PLN'.\n\n"
            "Zwróć odpowiedź *wyłącznie* w formacie JSON, używając następujących kluczy: "
            "{\"opis\": \"<nazwa_sprzedawcy>\", \"data\": \"<data_RRRR-MM-DD>\", \"kwota\": <kwota_liczba>}.\n"
            "Nawet jeśli nie jesteś pewien na 100%, zwróć swoją najlepszą próbę odczytania danych, a nie null. "
            "Nie dodawaj żadnych dodatkowych wyjaśnień ani formatowania, tylko czysty JSON."
    )

    try:
        # Używamy nowszego i bardziej uniwersalnego modelu
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)

        if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
            sugerowana_kategoria = response.candidates[0].content.parts[0].text.strip()
            if sugerowana_kategoria in dostepne_kategorie:
                print(f"Info AI: Gemini zasugerował kategorię '{sugerowana_kategoria}' dla opisu '{opis_transakcji}'.")
                return sugerowana_kategoria

        print(f"Ostrzeżenie AI: Gemini zwrócił nieznaną lub pustą odpowiedź. Używam '{kategoria_domyslna}'.")
        return kategoria_domyslna

    except Exception as e:
        print(f"BŁĄD AI: Wystąpił problem podczas komunikacji z Gemini: {e}")
        return f"{kategoria_domyslna} (błąd API)"
