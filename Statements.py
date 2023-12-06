import sqlite3

class Statements:
    __Section = None
    __FilingDate = None
    __Status = None
    __PasNomer = None
    def __init__(self, Section, FilingDate, Status, PasNomer):
        self.Section = Section
        self.FilingDate = FilingDate
        self.Status = Status
        self.PasNomer = PasNomer

    def InsertInStatements(self):
        conn = sqlite3.connect('police.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO  Statements (Section, FilingDate, Status, PasNomer) VALUES (?,?,?,?)",
            (self.Section, self.FilingDate, self.Status, self.PasNomer))
        conn.commit()
        conn.close()