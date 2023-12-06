from  Human import Human
import sqlite3


class Admins(Human):
    __AccessCode = None

    def __init__(self, Surname, Name, MiddleName,  AccessCode):
        super().__init__(Surname, Name, MiddleName)
        self.AccessCode = AccessCode

    def InsertInAdmins(self):
        conn = sqlite3.connect('police.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Admins (SurName, emName, MiddleName, AccessCode) VALUES (?,?,?,?)",
            (self.Surname, self.Name, self.MiddleName, self.AccessCode))
        conn.commit()
        conn.close()