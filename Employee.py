from  Human import Human
import sqlite3


class Employee(Human):
    __Rank = None
    __Post = None
    __AccessCode = None

    def __init__(self, Surname, Name, MiddleName, Rank, Post, AccessCode):
        super().__init__(Surname, Name, MiddleName)
        self.Rank = Rank
        self.Post = Post
        self.AccessCode = AccessCode

    def InsertInEmployee(self):
        conn = sqlite3.connect('police.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Employee (SurName, emName, MiddleName, Rank, Post, AccessCode) VALUES (?,?,?,?,?,?)",
            (self.Surname, self.Name, self.MiddleName, self.Rank, self.Post, self.AccessCode))
        conn.commit()
        conn.close()