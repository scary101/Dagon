from  Human import Human
import sqlite3

class Applicant(Human):
    __PasNomer = None
    __PasSeria = None
    __DateBorn = None

    def __init__(self, Surname, Name, MiddleName, PasSeria, PasNomer, DateBorn):
        super().__init__(Surname, Name, MiddleName)
        self.PasSeria = PasSeria
        self.PasNomer = PasNomer
        self.DateBorn = DateBorn

    def InsertInApplicant(self):
        conn = sqlite3.connect('police.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO  Applicant (SurName, emName, MiddleName, PasSeria, PasNomer, DateBorn) VALUES (?,?,?,?,?,?)",
            (self.Surname, self.Name, self.MiddleName, self.PasSeria, self.PasNomer, self.DateBorn))
        conn.commit()
        conn.close()