# Etap 1: Budowanie zależności
# Używamy lekkiego obrazu Pythona jako bazy
FROM python:3.12-slim as builder

# Ustawiamy katalog roboczy w kontenerze
WORKDIR /opt/venv

# Kopiujemy tylko plik z zależnościami, aby wykorzystać cache Dockera
COPY requirements.txt .

# Tworzymy wirtualne środowisko i instalujemy pakiety
RUN python -m venv . && \
    . bin/activate && \
    pip install --no-cache-dir -r requirements.txt

# Etap 2: Finalny obraz aplikacji
# Zaczynamy od nowa z tym samym lekkim obrazem
FROM python:3.12-slim

# Ustawiamy katalog roboczy dla aplikacji
WORKDIR /app

# Kopiujemy wirtualne środowisko z zależnościami z poprzedniego etapu
COPY --from=builder /opt/venv /opt/venv

# Kopiujemy resztę plików aplikacji
COPY . .

# Ustawiamy zmienną środowiskową PATH, aby wskazywała na nasze wirtualne środowisko
ENV PATH="/opt/venv/bin:$PATH"

# Ustawiamy komendę, która uruchomi aplikację, gdy kontener wystartuje
# Ta wersja komendy poprawnie odczytuje zmienną $PORT
CMD ["sh", "-c", "gunicorn app:app --bind 0.0.0.0:$PORT"]
