import sqlite3
from sqlite3 import Error
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty, ListProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from database import Database


class WindowManager(ScreenManager):
    pass


db = Database("sqlitebase.db")
kv = Builder.load_file("baza.kv")
sm = WindowManager()


class MainWindow(Screen):
    pass

class KategorieCzesciWindow(Screen):

    rows = ListProperty([("id_kategorii", "nazwa")])
    table = "Kategorie_Czesci"

    def get_data(self):
        self.rows = db.select_all(self.table)
        print(self.rows)

    def add_new(self, values):
        db.insert_into(self.table, values)

    def edit_value(self, id, values):
        db.update(self.table, id, values)

    def delete_value(self, id):
        db.delete(self.table, "id_kategorii", id)

    def save_database(self):
        db.conn.commit()

    pass

class CzesciMotoryzacyjneWindow(Screen):

    rows = ListProperty([("id_czesci", "id_kategorii", "nazwa", "opis")])
    table = "Czesci_Motoryzacyjne"

    def get_data(self):
        self.rows = db.select_all(self.table)
        print(self.rows)

    def add_new(self, values):
        db.insert_into(self.table, values)

    def edit_value(self, id, values):
        db.update(self.table, id, values)

    def delete_value(self, id):
        db.delete(self.table, "id_czesci", id)

    def save_database(self):
        db.conn.commit()

    pass


class PojazdyWindow(Screen):

    rows = ListProperty([("id_pojazdu", "numer_rej")])
    table = "Pojazdy"

    def get_data(self):
        self.rows = db.select_all(self.table)
        print(self.rows)

    def add_new(self, values):
        db.insert_into(self.table, values)

    def edit_value(self, id, values):
        db.update(self.table, id, values)

    def delete_value(self, id):
        db.delete(self.table, "id_pojazdu", id)

    def save_database(self):
        db.conn.commit()

    pass


class MechanicyWindow(Screen):

    rows = ListProperty([("id_mechanika", "nazwisko")])
    table = "Mechanicy"

    def get_data(self):
        self.rows = db.select_all(self.table)
        print(self.rows)

    def add_new(self, values):
        db.insert_into(self.table, values)

    def edit_value(self, id, values):
        db.update(self.table, id, values)

    def delete_value(self, id):
        db.delete(self.table, "id_mechanika", id)

    def save_database(self):
        db.conn.commit()

    pass


class NaprawyWindow(Screen):

    rows = ListProperty([("id_naprawy", "id_pojazdu", "id_mechanika", "data", "status")])
    table = "Naprawy"

    def get_data(self):
        self.rows = db.select_all(self.table)
        print(self.rows)

    def add_new(self, values):
        db.insert_into(self.table, values)

    def edit_value(self, id, values):
        db.update(self.table, id, values)

    def delete_value(self, id):
        db.delete(self.table, "id_naprawy", id)

    def save_database(self):
        db.conn.commit()

    pass

def add_input():
    pop = Popup(title='Invalid Login',
                  content=(Label(text='Invalid username or password.'), Label(text='2 username or password.'), Label(text='2 username or password.')),
                  size_hint=(None, None), size=(400, 400))
    pop.open()

screens = [MainWindow(name="Main"), KategorieCzesciWindow(name="Kategorie_Czesci"), CzesciMotoryzacyjneWindow(name="Czesci_Motoryzacyjne"),
           PojazdyWindow(name="Pojazdy"), MechanicyWindow(name="Mechanicy"), NaprawyWindow(name="Naprawy")]
for screen in screens:
    sm.add_widget(screen)
sm.current = "Main"


class MyMainApp(App):
    def build(self):
        db.initial_configuration()
        return sm

if __name__ == '__main__':
    MyMainApp().run()


