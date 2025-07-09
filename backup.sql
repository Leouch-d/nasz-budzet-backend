BEGIN TRANSACTION;

-- Tworzenie tabel
CREATE TABLE kategorie (
    id INTEGER NOT NULL,
    nazwa VARCHAR(100) NOT NULL,
    typ VARCHAR(20) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (nazwa)
);

CREATE TABLE transakcje (
    id INTEGER NOT NULL,
    typ VARCHAR(20) NOT NULL,
    miesiac VARCHAR(7) NOT NULL,
    kategoria VARCHAR(100),
    opis VARCHAR(255),
    kwota FLOAT NOT NULL,
    data_transakcji DATETIME NOT NULL,
    uzytkownik VARCHAR(50) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE kategoria_limit (
    kategoria VARCHAR(100) NOT NULL,
    "limit" FLOAT NOT NULL,
    PRIMARY KEY (kategoria)
);

CREATE TABLE szablony_transakcji (
    id INTEGER NOT NULL,
    typ VARCHAR(20) NOT NULL,
    kategoria VARCHAR(100) NOT NULL,
    opis VARCHAR(255) NOT NULL,
    kwota FLOAT NOT NULL,
    PRIMARY KEY (id)
);

-- Wstawianie danych
-- Kategorie
INSERT INTO "kategorie" ("id", "nazwa", "typ") VALUES (1, 'Podatki/Raty/Opłaty', 'wydatek');
INSERT INTO "kategorie" ("id", "nazwa", "typ") VALUES (2, 'Jedzenie', 'wydatek');
INSERT INTO "kategorie" ("id", "nazwa", "typ") VALUES (3, 'Inne', 'wydatek');
INSERT INTO "kategorie" ("id", "nazwa", "typ") VALUES (4, 'Lekarze i leki', 'wydatek');
INSERT INTO "kategorie" ("id", "nazwa", "typ") VALUES (5, 'Rozrywka', 'wydatek');
INSERT INTO "kategorie" ("id", "nazwa", "typ") VALUES (6, 'Paliwo', 'wydatek');
INSERT INTO "kategorie" ("id", "nazwa", "typ") VALUES (7, 'Przychody', 'przychód');

-- Limity
INSERT INTO "kategoria_limit" ("kategoria", "limit") VALUES ('Jedzenie', 2500.00);
INSERT INTO "kategoria_limit" ("kategoria", "limit") VALUES ('Paliwo', 1000.00);

-- Szablony transakcji (Automaty)
INSERT INTO "szablony_transakcji" ("id", "typ", "kategoria", "opis", "kwota") VALUES (1, 'wydatek', 'Podatki/Raty/Opłaty', 'Internet', 120.00);
INSERT INTO "szablony_transakcji" ("id", "typ", "kategoria", "opis", "kwota") VALUES (2, 'wydatek', 'Podatki/Raty/Opłaty', 'Kredyt', 1229.04);
INSERT INTO "szablony_transakcji" ("id", "typ", "kategoria", "opis", "kwota") VALUES (3, 'wydatek', 'Podatki/Raty/Opłaty', 'Raty Alior do 08.2026', 180.39);
INSERT INTO "szablony_transakcji" ("id", "typ", "kategoria", "opis", "kwota") VALUES (4, 'wydatek', 'Podatki/Raty/Opłaty', 'Raty Alior do 10.2026', 48.42);
INSERT INTO "szablony_transakcji" ("id", "typ", "kategoria", "opis", "kwota") VALUES (5, 'wydatek', 'Podatki/Raty/Opłaty', 'Raty Alior do 10.2026', 54.44);
INSERT INTO "szablony_transakcji" ("id", "typ", "kategoria", "opis", "kwota") VALUES (6, 'wydatek', 'Podatki/Raty/Opłaty', 'Raty Alior do 05.2026', 182.45);
INSERT INTO "szablony_transakcji" ("id", "typ", "kategoria", "opis", "kwota") VALUES (7, 'wydatek', 'Podatki/Raty/Opłaty', 'Śmieci', 195.00);
INSERT INTO "szablony_transakcji" ("id", "typ", "kategoria", "opis", "kwota") VALUES (8, 'wydatek', 'Podatki/Raty/Opłaty', 'Kredyt do 06.2027', 180.77);
INSERT INTO "szablony_transakcji" ("id", "typ", "kategoria", "opis", "kwota") VALUES (9, 'wydatek', 'Podatki/Raty/Opłaty', 'Santander kredyt do 12.2026', 227.00);
INSERT INTO "szablony_transakcji" ("id", "typ", "kategoria", "opis", "kwota") VALUES (10, 'wydatek', 'Podatki/Raty/Opłaty', 'Telefony (3)', 90.00);
INSERT INTO "szablony_transakcji" ("id", "typ", "kategoria", "opis", "kwota") VALUES (11, 'wydatek', 'Rozrywka', 'netflix', 33.00);
INSERT INTO "szablony_transakcji" ("id", "typ", "kategoria", "opis", "kwota") VALUES (12, 'wydatek', 'Rozrywka', 'Youtube premium', 60.00);
-- Szablony przychodów (NOWOŚĆ)
INSERT INTO "szablony_transakcji" ("id", "typ", "kategoria", "opis", "kwota") VALUES (13, 'przychód', 'Przychody', 'Pensja RSB', 6300.00);
INSERT INTO "szablony_transakcji" ("id", "typ", "kategoria", "opis", "kwota") VALUES (14, 'przychód', 'Przychody', '800+', 2400.00);
INSERT INTO "szablony_transakcji" ("id", "typ", "kategoria", "opis", "kwota") VALUES (15, 'przychód', 'Przychody', 'Pensja Rodzice', 500.00);
INSERT INTO "szablony_transakcji" ("id", "typ", "kategoria", "opis", "kwota") VALUES (16, 'przychód', 'Przychody', 'RKO', 1000.00);
INSERT INTO "szablony_transakcji" ("id", "typ", "kategoria", "opis", "kwota") VALUES (17, 'przychód', 'Przychody', 'Alimenty', 1000.00);


-- Transakcje
-- Czerwiec 2025
INSERT INTO "transakcje" ("id", "typ", "miesiac", "kategoria", "opis", "kwota", "data_transakcji", "uzytkownik") VALUES (1, 'wydatek', '2025-06', 'Inne', 'balans', 5865.54, '2025-06-30 20:00:00', 'Jacek');

-- Lipiec 2025
-- Przychody (NOWOŚĆ)
INSERT INTO "transakcje" ("id", "typ", "miesiac", "kategoria", "opis", "kwota", "data_transakcji", "uzytkownik") VALUES (31, 'przychód', '2025-07', 'Przychody', 'Pensja RSB', 6300.00, '2025-07-01 00:00:00', 'System');
INSERT INTO "transakcje" ("id", "typ", "miesiac", "kategoria", "opis", "kwota", "data_transakcji", "uzytkownik") VALUES (32, 'przychód', '2025-07', 'Przychody', '800+', 2400.00, '2025-07-01 00:00:00', 'System');
INSERT INTO "transakcje" ("id", "typ", "miesiac", "kategoria", "opis", "kwota", "data_transakcji", "uzytkownik") VALUES (33, 'przychód', '2025-07', 'Przychody', 'Pensja Rodzice', 500.00, '2025-07-01 00:00:00', 'System');
INSERT INTO "transakcje" ("id", "typ", "miesiac", "kategoria", "opis", "kwota", "data_transakcji", "uzytkownik") VALUES (34, 'przychód', '2025-07', 'Przychody', 'RKO', 1000.00, '2025-07-01 00:00:00', 'System');
INSERT INTO "transakcje" ("id", "typ", "miesiac", "kategoria", "opis", "kwota", "data_transakcji", "uzytkownik") VALUES (35, 'przychód', '2025-07', 'Przychody', 'Alimenty', 1000.00, '2025-07-01 00:00:00', 'System');

-- Podatki/Raty/Opłaty
INSERT INTO "transakcje" ("id", "typ", "miesiac", "kategoria", "opis", "kwota", "data_transakcji", "uzytkownik") VALUES (2, 'wydatek', '2025-07', 'Podatki/Raty/Opłaty', 'Komornik', 675.53, '2025-07-02 14:08:00', 'Maja');
INSERT INTO "transakcje" ("id", "typ", "miesiac", "kategoria", "opis", "kwota", "data_transakcji", "uzytkownik") VALUES (3, 'wydatek', '2025-07', 'Podatki/Raty/Opłaty', 'Internet', 120.00, '2025-07-01 00:00:00', 'System');
INSERT INTO "transakcje" ("id", "typ", "miesiac", "kategoria", "opis", "kwota", "data_transakcji", "uzytkownik") VALUES (4, 'wydatek', '2025-07', 'Podatki/Raty/Opłaty', 'Kredyt', 1229.04, '2025-07-01 00:00:00', 'System');
INSERT INTO "transakcje" ("id", "typ", "miesiac", "kategoria", "opis", "kwota", "data_transakcji", "uzytkownik") VALUES (5, 'wydatek', '2025-07', 'Podatki/Raty/Opłaty', 'Raty Alior do 08.2026', 180.39, '2025-07-01 00:00:00', 'System');
INSERT INTO "transakcje" ("id", "typ", "miesiac", "kategoria", "opis", "kwota", "data_transakcji", "uzytkownik") VALUES (6, 'wydatek', '2025-07', 'Podatki/Raty/Opłaty', 'Raty Alior do 10.2026', 48.42, '2025-07-01 00:00:00', 'System');
INSERT INTO "transakcje" ("id", "typ", "miesiac", "kategoria", "opis", "kwota", "data_transakcji", "uzytkownik") VALUES (7, 'wydatek', '2025-07', 'Podatki/Raty/Opłaty', 'Raty Alior do 10.2026', 54.44, '2025-07-01 00:00:00', 'System');
INSERT INTO "transakcje" ("id", "typ", "miesiac", "kategoria", "opis", "kwota", "data_transakcji", "uzytkownik") VALUES (8, 'wydatek', '2025-07', 'Podatki/Raty/Opłaty', 'Raty Alior do 05.2026', 182.45, '2025-07-01 00:00:00', 'System');
INSERT INTO "transakcje" ("id", "typ", "miesiac", "kategoria", "opis", "kwota", "data_transakcji", "uzytkownik") VALUES (9, 'wydatek', '2025-07', 'Podatki/Raty/Opłaty', 'Śmieci', 195.00, '2025-07-01 00:00:00', 'System');
INSERT INTO "transakcje" ("id", "typ", "miesiac", "kategoria", "opis", "kwota", "data_transakcji", "uzytkownik") VALUES (10, 'wydatek', '2025-07', 'Podatki/Raty/Opłaty', 'Kredyt do 06.2027', 180.77, '2025-07-01 00:00:00', 'System');
INSERT INTO "transakcje" ("id", "typ", "miesiac", "kategoria", "opis", "kwota", "data_transakcji", "uzytkownik") VALUES (11, 'wydatek', '2025-07', 'Podatki/Raty/Opłaty', 'Santander kredyt do 12.2026', 227.00, '2025-07-01 00:00:00', 'System');
INSERT INTO "transakcje" ("id", "typ", "miesiac", "kategoria", "opis", "kwota", "data_transakcji", "uzytkownik") VALUES (12, 'wydatek', '2025-07', 'Podatki/Raty/Opłaty', 'Telefony (3)', 90.00, '2025-07-01 00:00:00', 'System');

-- Jedzenie
INSERT INTO "transakcje" ("id", "typ", "miesiac", "kategoria", "opis", "kwota", "data_transakcji", "uzytkownik") VALUES (13, 'wydatek', '2025-07', 'Jedzenie', 'makro', 440.06, '2025-07-08 15:22:00', 'Jacek');
INSERT INTO "transakcje" ("id", "typ", "miesiac", "kategoria", "opis", "kwota", "data_transakcji", "uzytkownik") VALUES (14, 'wydatek', '2025-07', 'Jedzenie', 'lidl', 37.24, '2025-07-08 15:21:00', 'Jacek');
INSERT INTO "transakcje" ("id", "typ", "miesiac", "kategoria", "opis", "kwota", "data_transakcji", "uzytkownik") VALUES (15, 'wydatek', '2025-07', 'Jedzenie', 'lidl', 16.84, '2025-07-08 15:21:00', 'Jacek');
INSERT INTO "transakcje" ("id", "typ", "miesiac", "kategoria", "opis", "kwota", "data_transakcji", "uzytkownik") VALUES (16, 'wydatek', '2025-07', 'Jedzenie', 'lidl', 20.96, '2025-07-08 15:20:00', 'Jacek');
INSERT INTO "transakcje" ("id", "typ", "miesiac", "kategoria", "opis", "kwota", "data_transakcji", "uzytkownik") VALUES (17, 'wydatek', '2025-07', 'Jedzenie', 'Lidl sp. z o. o. sp. k.', 27.93, '2025-07-03 22:00:00', 'Jacek');
INSERT INTO "transakcje" ("id", "typ", "miesiac", "kategoria", "opis", "kwota", "data_transakcji", "uzytkownik") VALUES (18, 'wydatek', '2025-07', 'Jedzenie', 'Lidl', 445.29, '2025-07-03 22:00:00', 'Maja');
INSERT INTO "transakcje" ("id", "typ", "miesiac", "kategoria", "opis", "kwota", "data_transakcji", "uzytkownik") VALUES (19, 'wydatek', '2025-07', 'Jedzenie', 'Zakupy zabka', 38.53, '2025-07-03 03:02:00', 'Maja');
INSERT INTO "transakcje" ("id", "typ", "miesiac", "kategoria", "opis", "kwota", "data_transakcji", "uzytkownik") VALUES (20, 'wydatek', '2025-07', 'Jedzenie', 'Lidl sp. z o. o. sp. k.', 41.98, '2025-07-02 22:00:00', 'Maja');
INSERT INTO "transakcje" ("id", "typ", "miesiac", "kategoria", "opis", "kwota", "data_transakcji", "uzytkownik") VALUES (21, 'wydatek', '2025-07', 'Jedzenie', 'Lidl', 268.61, '2025-07-02 11:03:00', 'Jacek');

-- Inne
INSERT INTO "transakcje" ("id", "typ", "miesiac", "kategoria", "opis", "kwota", "data_transakcji", "uzytkownik") VALUES (22, 'wydatek', '2025-07', 'Inne', 'TJX Poland Sp. z o.o.', 248.95, '2025-07-04 00:00:00', 'Jacek');
INSERT INTO "transakcje" ("id", "typ", "miesiac", "kategoria", "opis", "kwota", "data_transakcji", "uzytkownik") VALUES (23, 'wydatek', '2025-07', 'Inne', 'SAMBOR', 113.92, '2025-07-03 00:00:00', 'Maja');

-- Lekarze i leki
INSERT INTO "transakcje" ("id", "typ", "miesiac", "kategoria", "opis", "kwota", "data_transakcji", "uzytkownik") VALUES (24, 'wydatek', '2025-07', 'Lekarze i leki', 'Psychiatra Antek', 250.00, '2025-07-02 09:04:00', 'Jacek');

-- Rozrywka
INSERT INTO "transakcje" ("id", "typ", "miesiac", "kategoria", "opis", "kwota", "data_transakcji", "uzytkownik") VALUES (25, 'wydatek', '2025-07', 'Rozrywka', 'Steam', 37.98, '2025-07-02 22:00:00', 'Jacek');
INSERT INTO "transakcje" ("id", "typ", "miesiac", "kategoria", "opis", "kwota", "data_transakcji", "uzytkownik") VALUES (26, 'wydatek', '2025-07', 'Rozrywka', 'Gierka Steam', 45.77, '2025-07-02 10:58:00', 'Jacek');
INSERT INTO "transakcje" ("id", "typ", "miesiac", "kategoria", "opis", "kwota", "data_transakcji", "uzytkownik") VALUES (27, 'wydatek', '2025-07', 'Rozrywka', 'netflix', 33.00, '2025-07-01 00:00:00', 'System');
INSERT INTO "transakcje" ("id", "typ", "miesiac", "kategoria", "opis", "kwota", "data_transakcji", "uzytkownik") VALUES (28, 'wydatek', '2025-07', 'Rozrywka', 'Youtube premium', 60.00, '2025-07-01 00:00:00', 'System');

-- Paliwo
INSERT INTO "transakcje" ("id", "typ", "miesiac", "kategoria", "opis", "kwota", "data_transakcji", "uzytkownik") VALUES (29, 'wydatek', '2025-07', 'Paliwo', 'orlen', 79.36, '2025-07-08 15:23:00', 'Jacek');
INSERT INTO "transakcje" ("id", "typ", "miesiac", "kategoria", "opis", "kwota", "data_transakcji", "uzytkownik") VALUES (30, 'wydatek', '2025-07', 'Paliwo', 'ORLEN S.A.', 96.66, '2025-07-01 22:00:00', 'Jacek');

COMMIT;
