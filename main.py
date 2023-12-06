import datetime
import sqlite3
from itertools import chain
import os
from tabulate import tabulate
from Employee import Employee
from Applicant import Applicant
from Statements import Statements

try:
    os.mkdir("Applications")
except:
    pass

path = os.getcwd() + "\\Applications"


def CreateDataBase():
    conn = sqlite3.connect('police.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Employee(
            ID_employee INTEGER PRIMARY KEY AUTOINCREMENT ,
            SurName TEXT NOT NULL,
            emName TEXT NOT NULL,
            MiddleName TEXT,
            Rank TEXT NOT NULL,
            Post TEXT NOT NULL,
            AccessCode INTEGER NOT NULL
        )
    ''')

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS Applicant(
                ID_Applicant INTEGER PRIMARY KEY AUTOINCREMENT,
                SurName TEXT NOT NULL,
                emName TEXT NOT NULL,
                MiddleName TEXT,
                PasSeria INTEGER NOT NULL,
                PasNomer TEXT UNIQUE NOT NULL,
                DateBorn TEXT NOT NULL
            )
        ''')

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS Statements(
                ID_Statements INTEGER PRIMARY KEY AUTOINCREMENT ,
                Section TEXT NOT NULL,
                FilingDate TEXT NOT NULL,
                PasNomer TEXT NOT NULL,
                Status TEXT NOT NULL
            )
        ''')

    cursor.execute('''
                CREATE TABLE IF NOT EXISTS Admins(
                    ID_Admins INTEGER PRIMARY KEY AUTOINCREMENT,
                    SurName TEXT NOT NULL,
                    emName TEXT NOT NULL,
                    MiddleName TEXT,
                    AccessCode INTEGER NOT NULL
                )
            ''')

    conn.commit()
    conn.close()


def Viewtable(NameTable):
    conn = sqlite3.connect('police.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {NameTable}")
    rows = cursor.fetchall()
    print(tabulate(rows, headers=[i[0] for i in cursor.description]))
    conn.commit()
    conn.close()

def ViewtableApp(PasNomer):
    conn = sqlite3.connect('police.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM Statements WHERE PasNomer = {PasNomer}")
    rows = cursor.fetchall()
    print(tabulate(rows, headers=[i[0] for i in cursor.description]))
    conn.commit()
    conn.close()




def CheckKod(Table):
    conn = sqlite3.connect('police.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT SurName FROM {Table}")
    login = list(chain.from_iterable(cursor.fetchall()))
    while True:
        user_login = input("Введите свой логи: ")
        if user_login in login:
            cursor.execute(f"SELECT AccessCode FROM {Table}")
            kod = list(chain.from_iterable(cursor.fetchall()))
            while True:
                password = int((input("Введите код доступа: ")))
                if password in kod:
                    cursor.execute(f"SELECT emName, MiddleName FROM {Table} WHERE AccessCode = {password}")
                    fullName = cursor.fetchall()
                    fullName = ' '.join([idx for tup in fullName for idx in tup])
                    print(f"Здравия желаю товарищ {fullName}, Добро пожаловть в базу данных!")
                    break
                else:
                    print("Неверный код доступа")
            break
        else:
            print("Сотрудник не найден в базе данных")



def RegistryApplicant():
    conn = sqlite3.connect('police.db')
    cursor = conn.cursor()
    cursor.execute("SELECT PasNomer FROM Applicant")
    AllPasNomer = list(chain.from_iterable(cursor.fetchall()))

    print("Для подачи заявления, для начала укажите свои данные. ФИО, серия и номер паспорта, дату рождение")
    SurName = input("Ввеиде свою фамилию: ")
    Name = input("Ввеиде своё имя: ")
    MiddleName = input("Ввеиде своё отчество: ")
    PasSeria = None
    PasNomer = None
    DateBorn = None
    isRun = True
    while isRun == True:
        PasSeria = input("Ввеиде серию паспорта: ")
        Check = ChisInStr(PasSeria)
        if len(str(PasSeria)) == 4 and Check == False:
            break
        else:
            print("Неккоректная серия паспорта!")

    while isRun == True:
        PasNomer = input("Ввеиде номер паспорта: ")
        Check = ChisInStr(PasNomer)
        if len(PasNomer) == 6 and PasNomer not in AllPasNomer and Check == False:
            break
        else:
            print("Неккоректный номер паспорта!")

    while isRun == True:
        DateBorn = input("Ввеиде дату рождения по образцу \"00.00.0000\": ")
        Check = ChisInStr(DateBorn)
        if len(DateBorn) == 10 and Check == False:
            break
        else:
            print("Неккоректная дата!")

    applicant = Applicant(SurName, Name, MiddleName, PasSeria, PasNomer, DateBorn)
    applicant.InsertInApplicant()
    conn.commit()
    conn.close()
    return PasNomer



def ChisInStr(stroka):
    if '0' or '1' or '2' or '3' or '4' or '5' or '6' or '7' or '8' or '9' in stroka:
        return False
    else:
        return True


def WriteStatements():
    data = str(datetime.date.today())
    PasNomer = RegistryApplicant()
    print("Начните писать заявление, указывая все подробности")
    text = input()
    zayava = "Дата подачи заявления" + data + '\n' + "Номер паспорта" + str(PasNomer) + '\n' + text
    path1 = path + "\\" + PasNomer + ".txt"
    file = open(path1, "w+")
    file.write(zayava)


def AddEmployee():
    Surname = Proverka(input("Введите фамилию сотрудника: "))
    Name = Proverka(input("Введите имя сотрудника: "))
    MiddleName = Proverka(input("Введите отчество сотрудика: "))
    Rank = Proverka(input("Введите звание сотрудика: "))
    Post = Proverka(input("Введите пост сотрудника:  "))
    while True:
        AccessCode = input("Введите уникальный код сотрудника: ")
        check = ChisInStr(AccessCode)
        if check == False:
            break
        else:
            continue


    employee = Employee(Surname, Name, MiddleName, Rank, Post, AccessCode)
    employee.InsertInEmployee()


def OpenStatements():
    folder_path = path
    file_paths = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]
    for i in file_paths:
        file_path = i
        file_name = os.path.basename(file_path)
        print(file_name)
    while True:
        a = input("Для просмотра заявления, введите его позицию - ")
        Chek = ChisInStr(a)
        if Chek == False:
            try:
                with open(file_paths[int(a) - 1], 'r') as file:
                    content = file.read()
                    print(content)
            except:
                print("Файл не найден")
            b = input("Желаете продолжить просмотр? "
                      "\n1. Выйти в меню"
                      "\n2. Продолжить"
                      "\nВаш ответ: ")
            if b == '1':
                break
            else:
                continue
        else:
            print("Некоректный ввод!")


def EditTable(NameTable):
    a = input("Выберите действие над таблицей "
              "\n1. Удаление "
              "\n2. Обновление"
              "\nВаш ответ: ")
    match a:
        case "1":
            print("Удаление данных")
            while True:
                Viewtable(NameTable)
                conn = sqlite3.connect('police.db')
                cursor = conn.cursor()
                b = input("Введите ID для удаления: ")
                cursor.execute(f"DELETE FROM {NameTable} WHERE  ID_{NameTable} = {b}")
                conn.commit()
                conn.close()
                print("Успешно удалено")
                c = input("Хотите продолжить? Да или Нет")
                if c == "Да":
                    continue
                else:
                    break

        case "2":
            print("Обновления данных в базе ")
            while True:
                Viewtable(NameTable)
                conn = sqlite3.connect('police.db')
                cursor = conn.cursor()
                cursor.execute(f"PRAGMA table_info({NameTable})")
                columns_data = cursor.fetchall()
                columns = [column[1] for column in columns_data]
                while True:
                    c = input("Выберите колонку для обновления: ")
                    if c in columns:
                        ID = input("Выберите номер заявления: ")
                        new = input("Введите новое значение: ")
                        sql_update_query = f"""Update {NameTable} set {c} = ? where ID_{NameTable} = ?"""
                        data = (new, ID)
                        cursor.execute(sql_update_query, data)

                        conn.commit()
                        conn.close()
                        break
                    else:
                        print("Колонка не найдена!")

                c = input("Хотите продолжить? Да или Нет")
                if c == "Да":
                    continue
                else:
                    break

        case _:
            print("Действие не найдено!")


def AddStatements():
    print("Добавление заявления в базу данных:")
    while True:
        Section = input("Введите статью: ")
        FilingDate = input("Ввеиде дату приема заявления по образцу \"00.00.0000\": ")
        Status = input("Введите статус дела: ")
        PasNomer = input("Введите номер паспорта заявителя: ")
        state = Statements(Section, FilingDate, Status, PasNomer)
        state.InsertInStatements()
        b = input("Хотите продолжить? Да, Нет")
        if b == "Да":
            continue
        else:
            break




def Proverka(stroka):
    while True:
        while True:
            if any(char.isdigit() for char in stroka):
                stroka = input("Некоретктный ввод! \nВведите снова: ")
            else:
                break

        return stroka



CreateDataBase()
while True:
    print("База ЮЗАО по г. Москве")
    user = input("Кто вы?"
                 "\n1. Сотрудник"
                 "\n2. Заявитель"
                 "\n3. Админ"
                 "\n4. Выйти из БД"
                 "\nВаш ответ: ")

    if user == '1':
        print("Добрый день! Для подтверждения уровня доступа введите свой логин и ключ доступа")
        CheckKod("Employee")
        print("Выберите дальнейшие действия")
        while True:
            inp = input("1. Просмотр базы данных"
                        "\n2. Редактирование базы данных"
                        "\n3. Просмотр заявлений"
                        "\n4. Обработка заявления"
                        "\nВаш ответ: ")

            match inp:
                case '1':
                    while True:
                        NameTable = None
                        table = input("Выберите таблицу для просмотра"
                                      "\n1. Заявители"
                                      "\n2. Заявления"
                                      "\nВаш ответ: ")
                        if table == '1':
                            NameTable = "Statements"
                        elif table == '2':
                            NameTable = "Applicant"
                        Viewtable(NameTable)
                        a = input("Выйти в меню? Да/Нет - ")
                        if a == "Да":
                            break
                        else:
                            continue

                case '2':
                    while True:
                        NameTable = None
                        table = input("Выберите таблицу для редоктирования"
                                      "\n1. Заявители"
                                      "\n2. Заявления"
                                      "\nВаш ответ: ")
                        if table == '1':
                            NameTable = "Statements"
                        elif table == '2':
                            NameTable = "Applicant"
                        EditTable(NameTable)
                        a = input("Выйти в меню? Да/Нет - ")
                        if a == "Да":
                            break
                        else:
                            continue

                case '4':
                    while True:
                        AddStatements()
                        a = input("Выйти в меню? Да/Нет - ")
                        if a == "Да":
                            break
                        else:
                            continue
                case '3':
                    while True:
                        OpenStatements()
                        a = input("Выйти в меню? Да/Нет - ")
                        if a == "Да":
                            break
                        else:
                            continue
                case _:
                    print("Действие не найдено")


    elif user == '2':
        while True:
            inp = input("Добрый день! Желаете подать заявление или узнать статус?"
                        "\n1. Подать заявление"
                        "\n2. Узнать статус"
                        "\n3. Выйти в меню"
                        "\nВаш ответ: ")

            if inp == "1":
                WriteStatements()

            elif inp == "2":
                while True:
                    nomer_user = input("Для того, чтобы узнать статус заявления введите номер паспорта - ")
                    conn = sqlite3.connect('police.db')
                    cursor = conn.cursor()
                    cursor.execute(f"SELECT * FROM Statements")
                    PasNomer = list(chain.from_iterable(cursor.fetchall()))
                    if nomer_user in PasNomer:
                        ViewtableApp(nomer_user)
                        a = input("Выйти в меню? Да/Нет - ")
                        if a == "Да":
                            break
                        else:
                            continue
                    else:
                        print("Заявитель не найден!")

            elif inp == "3":
                break

            else:
                print("Действие не найдено!")

    elif user == '3':
        CheckKod("Admins")
        while True:
            vib = input("Выберите действие:"
                        "\n1. Добавить сотрулника"
                        "\n2. Редактировать таблицу Сотрудников"
                        "\nВаш выбор:")

            if vib == '1':
                AddEmployee()
            elif vib == "2":
                EditTable('Employee')
            else:
                print("Действие не найдено!")

            a = input("Выйти в меню? Да/Нет - ")
            if a == "Да":
                break
            else:
                continue

    elif user == "4":
        break

    else:
        print("Уровень доступа не найден!")