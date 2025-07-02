import google.generativeai as genai
import os

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
        f"Jesteś ekspertem od finansów osobistych w Polsce. Twoim zadaniem jest przypisanie jednej, "
        f"najbardziej pasującej kategorii do opisu transakcji. Masz do wyboru tylko i wyłącznie "
        f"kategorie z tej listy: {lista_kategorii_str}. Oto opis transakcji: \"{opis_transakcji}\". "
        f"Zwróć jako odpowiedź *tylko i wyłącznie* nazwę jednej kategorii z podanej listy. "
        f"Bez żadnych dodatkowych słów i wyjaśnień."
    )

    try:
        # ZMIANA: Używamy nowszego i bardziej uniwersalnego modelu, aby uniknąć błędów połączenia.
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

