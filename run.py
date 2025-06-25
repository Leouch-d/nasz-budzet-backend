# run.py
# Ten plik służy tylko i wyłącznie do uruchomienia naszej aplikacji.

from nasz_budzet import app

if __name__ == '__main__':
    app.run(debug=True, port=5000)
