import sqlite3
from sqlite3 import Error


class Database:

    def __init__(self, db_file):
        try:
            self.conn = sqlite3.connect(db_file)
            self.cur = self.conn.cursor()
        except Error as e:
            print(e)

        self.sql_create_kategorie_czesci = """ CREATE TABLE IF NOT EXISTS Kategorie_Czesci (
                                                id_kategorii integer PRIMARY KEY,
                                                nazwa text NOT NULL
                                            ); """

        self.sql_create_czesci_motoryzacyjne = """CREATE TABLE IF NOT EXISTS Czesci_Motoryzacyjne (
                                            id_czesci integer PRIMARY KEY,
                                            id_kategorii integer NOT NULL,
                                            nazwa text NOT NULL,
                                            opis text NOT NULL,
                                            FOREIGN KEY (id_kategorii) REFERENCES Kategorie_Czesci (id_kategorii)
                                        );"""

        self.sql_create_pojazdy = """ CREATE TABLE IF NOT EXISTS Pojazdy (
                                                id_pojazdu integer PRIMARY KEY,
                                                numer_rej text NOT NULL
                                            ); """

        self.sql_create_mechanicy = """CREATE TABLE IF NOT EXISTS Mechanicy (
                                            id_mechanika integer PRIMARY KEY,
                                            nazwisko text NOT NULL
                                        );"""

        self.sql_create_naprawy = """CREATE TABLE IF NOT EXISTS Naprawy (
                                            id_naprawy integer PRIMARY KEY,
                                            id_pojazdu integer NOT NULL,
                                            id_mechanika integer NOT NULL,
                                            data text NOT NULL,
                                            status text NOT NULL,
                                            FOREIGN KEY (id_pojazdu) REFERENCES Pojazdy (id_pojazdu),
                                            FOREIGN KEY (id_mechanika) REFERENCES Mechanicy (id_mechanika)
                                        );"""

    def create_table(self, create_table_sql):
        try:
            self.cur.execute(create_table_sql)
        except Error as e:
            print(e)
        return None

    def select_all(self, table):
        try:
            self.cur.execute("SELECT * FROM " + table)
            return self.cur.fetchall()
        except Error as e:
            print(str(e))


    def insert_into(self, table, values):
        if table == "Kategorie_Czesci":
            sql = "INSERT INTO Kategorie_Czesci(nazwa) VALUES (?)"
        elif table == "Czesci_Motoryzacyjne":
            sql = "INSERT INTO Czesci_Motoryzacyjne(id_kategorii,nazwa,opis) VALUES (?,?,?)"
        elif table == "Pojazdy":
            sql = "INSERT INTO Pojazdy(numer_rej) VALUES (?)"
        elif table == "Naprawy":
            sql = "INSERT INTO Naprawy(id_pojazdu,id_mechanika,data,status) VALUES (?,?,?,?)"
        elif table == "Mechanicy":
            sql = "INSERT INTO Mechanicy(nazwisko) VALUES (?)"
        else:
            return None
        try:
            self.cur.execute(sql, values)
        except Error as e:
            return "Zle wprowadzone dane! Blad " + str(e)
        return self.cur.lastrowid

    def update(self, table, id, values):
        """
        update in TABLE new VALUES where ID
        """
        if table == "Kategorie_Czesci":
            sql = "UPDATE Kategorie_Czesci SET nazwa = ? WHERE id_kategorii = " + id
        elif table == "Czesci_Motoryzacyjne":
            sql = "UPDATE Czesci_Motoryzacyjne SET id_kategorii = ?, nazwa = ?, opis = ? WHERE id_kategorii = " + id
        elif table == "Pojazdy":
            sql = "UPDATE Pojazdy SET numer_rej = ? WHERE id_pojazdu = " + id
        elif table == "Naprawy":
            sql = "UPDATE Naprawy SET id_pojazdu = ?, id_mechanika = ?, data = ?, status = ? WHERE id_naprawy = " + id
        elif table == "Mechanicy":
            sql = "UPDATE Mechanicy SET nazwisko = ? WHERE id_mechanika = " + id
        else:
            return None
        try:
            self.cur.execute(sql, values)
        except Error as e:
            return "Błąd!: " + str(e)

    def delete(self, table, id_name, id):
        sql = 'DELETE FROM ' + table + ' WHERE '+ id_name + '=' + id
        self.cur.execute(sql)

    def delete_all(self, table):
        sql = 'DELETE FROM ' + table
        self.cur.execute(sql)

    def table_has_records(self, table):
        self.cur.execute("SELECT * FROM " + table)
        data = self.cur.fetchall()
        if len(data) == 0:
            return False
        return True

    def initial_configuration(self):
        self.create_table(self.sql_create_kategorie_czesci)
        self.create_table(self.sql_create_czesci_motoryzacyjne)
        self.create_table(self.sql_create_pojazdy)
        self.create_table(self.sql_create_mechanicy)
        self.create_table(self.sql_create_naprawy)
        if self.table_has_records("Kategorie_Czesci") == False:
            self.insert_into("Kategorie_Czesci", ["Blacharka"])
        if self.table_has_records("Czesci_Motoryzacyjne") == False:
            self.insert_into("Czesci_Motoryzacyjne", [1, "Zderzak", "Golf"])
        if self.table_has_records("Pojazdy") == False:
            self.insert_into("Pojazdy", ["DW 6634J"])
        if self.table_has_records("Mechanicy") == False:
            self.insert_into("Mechanicy", ["Kowalczyk"])
        if self.table_has_records("Naprawy") == False:
            self.insert_into("Naprawy", [1, 1, "09.05.2019", "Przyjęty"])



    def end_db_connection(self):
        self.conn.commit()
        self.conn.close()