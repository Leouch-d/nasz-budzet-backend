# generate_tokens.py
# WERSJA ZAKTUALIZOWANA: Tworzy użytkowników, jeśli nie istnieją, a następnie generuje tokeny.

from nasz_budzet import create_app, db, bcrypt
from nasz_budzet.models import User
from flask_jwt_extended import create_access_token

# Utwórz kontekst aplikacji, aby mieć dostęp do bazy danych i konfiguracji
app = create_app()

with app.app_context():
    print("--- Generowanie tokenów dostępowych ---")

    # Lista użytkowników do utworzenia/sprawdzenia
    users_to_process = [
        {"username": "Jacek", "email": "jacekbielecki123@gmail.com", "password": "Acerv223hq!"},
        {"username": "Maja", "email": "majakokosza@gmail.com", "password": "Niewiem123"}
    ]

    for user_data in users_to_process:
        username = user_data["username"]
        
        # 1. Sprawdź, czy użytkownik istnieje
        user = User.query.filter_by(username=username).first()
        
        # 2. Jeśli nie istnieje, utwórz go
        if not user:
            print(f"INFO: Nie znaleziono użytkownika '{username}'. Tworzenie nowego konta...")
            try:
                hashed_password = bcrypt.generate_password_hash(user_data["password"]).decode('utf-8')
                new_user = User(
                    email=user_data["email"],
                    username=username,
                    password_hash=hashed_password
                )
                db.session.add(new_user)
                db.session.commit()
                # Pobierz nowo utworzonego użytkownika, aby mieć jego ID
                user = User.query.filter_by(username=username).first()
                print(f"SUKCES: Użytkownik '{username}' został utworzony.")
            except Exception as e:
                db.session.rollback()
                print(f"KRYTYCZNY BŁĄD: Nie udało się utworzyć użytkownika '{username}'. Błąd: {e}")
                continue # Przejdź do następnego użytkownika

        # 3. Wygeneruj token dla istniejącego lub nowo utworzonego użytkownika
        if user:
            identity = {'id': user.id, 'username': user.username}
            token = create_access_token(identity=identity)
            print(f"\n✅ Token dla {username} (skopiuj całą linię poniżej):")
            print(token)
        else:
            print(f"\nBŁĄD: Nie można wygenerować tokenu dla '{username}', ponieważ nie istnieje w bazie.")
        
    print("\n-----------------------------------------")
    print("Gotowe. Możesz teraz wkleić te tokeny do pliku login.tsx w aplikacji mobilnej.")