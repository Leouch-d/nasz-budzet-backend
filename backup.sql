PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE kategorie (
	id INTEGER NOT NULL, 
	nazwa VARCHAR(100) NOT NULL, 
	typ VARCHAR(20) NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (nazwa)
);
INSERT INTO kategorie VALUES(1,'inne','wydatek');
INSERT INTO kategorie VALUES(3,'Rozrywka','wydatek');
INSERT INTO kategorie VALUES(4,'Jedzenie','wydatek');
INSERT INTO kategorie VALUES(5,'Podatki','wydatek');
INSERT INTO kategorie VALUES(6,'Raty','wydatek');
INSERT INTO kategorie VALUES(7,'Paliwo','wydatek');
INSERT INTO kategorie VALUES(8,'Pensja','przychód');
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
INSERT INTO transakcje VALUES(1,'wydatek','2025-06','Pensja','Pensja',1000.0,'2025-06-01 00:00:00.000000','System');
INSERT INTO transakcje VALUES(2,'przychód','2025-06','Pensja','Pensja',10000.0,'2025-06-01 00:00:00.000000','System');
INSERT INTO transakcje VALUES(3,'wydatek','2025-06','Jedzenie','lidl',1000.0,'2025-06-30 08:23:35.957000','Maja');
INSERT INTO transakcje VALUES(4,'wydatek','2025-06','Jedzenie','biedronka',500.0,'2025-06-30 08:41:38.151000','Jacek');
INSERT INTO transakcje VALUES(5,'wydatek','2025-06','Jedzenie','biedronka',100.0,'2025-06-30 12:47:13.232000','Jacek');
INSERT INTO transakcje VALUES(6,'przychód','2025-07','Pensja','Pensja RSB',6300.0,'2025-07-01 00:00:00.000000','System');
INSERT INTO transakcje VALUES(7,'wydatek','2025-05','Jedzenie','biedra',2000.0,'2025-05-02 03:27:00.000000','Jacek');
INSERT INTO transakcje VALUES(8,'wydatek','2025-07','inne','test',200.0,'2025-07-02 07:44:56.637000','Maja');
INSERT INTO transakcje VALUES(9,'wydatek','2025-07','Raty','rata testowa',100.0,'2025-07-02 08:01:26.097000','Jacek');
INSERT INTO transakcje VALUES(10,'wydatek','2025-07','Raty','rata testowa',100.0,'2025-07-02 08:21:54.300000','Jacek');
INSERT INTO transakcje VALUES(11,'wydatek','2025-07','Raty','rata testowa',100.0,'2025-07-02 08:22:53.376000','Jacek');
INSERT INTO transakcje VALUES(12,'wydatek','2025-07','Podatki','rata testowa',1000.0,'2025-07-02 06:23:02.421000','Jacek');
INSERT INTO transakcje VALUES(13,'wydatek','2025-07','Inne','bioedra',100.0,'2025-07-02 09:19:46.075000','Jacek');
INSERT INTO transakcje VALUES(14,'wydatek','2025-07','Inne','sklep',240.0,'2025-07-02 00:00:00.000000','Jacek');
INSERT INTO transakcje VALUES(15,'przychód','2024-12','Pensja','Pensja RSB',6300.0,'2024-12-01 00:00:00.000000','System');
INSERT INTO transakcje VALUES(16,'wydatek','2024-12','Raty','rata testowa',100.0,'2024-12-01 00:00:00.000000','System');
INSERT INTO transakcje VALUES(17,'wydatek','2024-12','Inne','Etam',100.0,'2024-12-21 00:00:00.000000','Jacek');
INSERT INTO transakcje VALUES(18,'wydatek','2025-07','Inne','jedzenie',1000.0,'2025-07-02 11:50:36.137000','Jacek');
INSERT INTO transakcje VALUES(19,'wydatek','2025-07','Jedzenie','Biedronka',1000.0,'2025-07-02 09:50:54.238000','Jacek');
INSERT INTO transakcje VALUES(20,'wydatek','2025-07','Inne','wre',2134.0,'2025-07-02 12:29:25.792000','Jacek');
INSERT INTO transakcje VALUES(21,'wydatek','2025-07','Inne','biedronka',100.0,'2025-07-02 14:20:02.497000','Jacek');
INSERT INTO transakcje VALUES(22,'wydatek','2025-05','Inne','Selia Duty Free',22.0,'2025-05-18 00:00:00.000000','Jacek');
INSERT INTO transakcje VALUES(23,'wydatek','2025-07','Inne','POLREGIO S.A.',6.5,'2025-07-01 00:00:00.000000','Jacek');
INSERT INTO transakcje VALUES(24,'przychód','2020-01','Pensja','Pensja RSB',6300.0,'2020-01-01 00:00:00.000000','System');
INSERT INTO transakcje VALUES(25,'wydatek','2020-01','Raty','rata testowa',100.0,'2020-01-01 00:00:00.000000','System');
INSERT INTO transakcje VALUES(26,'wydatek','2020-01','Inne','PROMES S.C.',31.2100000000000008,'2020-01-19 00:00:00.000000','Jacek');
INSERT INTO transakcje VALUES(27,'wydatek','2020-01','Inne','PROMES S.C.',31.2100000000000008,'2020-01-19 00:00:00.000000','Jacek');
CREATE TABLE kategoria_limit (
	kategoria VARCHAR(100) NOT NULL, 
	"limit" FLOAT NOT NULL, 
	PRIMARY KEY (kategoria)
);
INSERT INTO kategoria_limit VALUES('Jedzenie',2500.0);
CREATE TABLE szablony_transakcji (
	id INTEGER NOT NULL, 
	typ VARCHAR(20) NOT NULL, 
	kategoria VARCHAR(100) NOT NULL, 
	opis VARCHAR(255) NOT NULL, 
	kwota FLOAT NOT NULL, 
	PRIMARY KEY (id)
);
INSERT INTO szablony_transakcji VALUES(1,'przychód','Pensja','Pensja RSB',6300.0);
INSERT INTO szablony_transakcji VALUES(2,'wydatek','Raty','rata testowa',100.0);
COMMIT;
