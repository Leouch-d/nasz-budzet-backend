# run.py
# Ten plik służy tylko do uruchomienia naszej aplikacji.
# Upewnij się, że jest on w głównym folderze projektu (nasz-budzet-backend).

from nasz_budzet import create_app

# Tworzymy instancję aplikacji za pomocą naszej fabryki
app = create_app()

if __name__ == '__main__':
    # Uruchamiamy serwer deweloperski
    app.run(host='0.0.0.0', port=5000, debug=True)
