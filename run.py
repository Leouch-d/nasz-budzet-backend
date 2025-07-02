# run.py
# Ten plik służy tylko i wyłącznie do uruchomienia naszej aplikacji.

from nasz_budzet import create_app

# Tworzymy instancję aplikacji za pomocą naszej fabryki
app = create_app()

if __name__ == '__main__':
    # Uruchamiamy serwer deweloperski
    # host='0.0.0.0' sprawia, że serwer jest dostępny z innych urządzeń w Twojej sieci
    # (np. z telefonu z Expo Go), a nie tylko z lokalnego komputera.
    app.run(host='0.0.0.0', port=5000, debug=True)

