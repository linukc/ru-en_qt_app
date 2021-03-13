from PyQt5.QtSql import QSqlDatabase, QSqlQuery
import exception as e


class DataBase():
    #слова и переводы в базе хранятся в отдельных таблицах вида логин+пароль
    #connection к одной и той же базе остается на протяжении работы для любого юзера и закрывается только после остановки программы
    #можно придумать архитекутру хранения данных поэлегантнее
    def __init__(self, type_='QSQLITE', path='db/db.sqlite'):
        self.type_ = type_
        self.path = path
        self.login_table = 'login'# создать таблицу данных если это первый пользователь
        

    def setUpConnection(self):
        self.db = QSqlDatabase.addDatabase(self.type_)
        self.db.setDatabaseName(self.path)
        if not self.db.open():
            raise e.NotConnectionToDB()

    def createTable(self, name):
        query = QSqlQuery(db=self.db)
        query.prepare(f'CREATE TABLE {name} (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, ru STRING, en STRING)')
        if not query.exec_():
            raise e.WrongDbQuery(query.lastError().text())

    def isUserExist(self, login, password=None):
        query = QSqlQuery(db=self.db)
        sql = f"SELECT id FROM {self.login_table} WHERE login='{login}'"
        if password:
            sql += f" AND password='{password}'"
        query.prepare(sql)
        if not query.exec_():
            raise e.WrongDbQuery(query.lastError().text())
        return query.first()

    def getDictionary(self, table):
        query = QSqlQuery(db=self.db)
        sql = f"SELECT ru, en FROM {table}"
        query.prepare(sql)
        if not query.exec_():
            raise e.WrongDbQuery(query.lastError().text())      
        ru, en = [], []
        while query.next():
            ru.append(query.value("ru"))
            en.append(query.value("en"))   
        return ru, en

    def addWordTranslation(self, table, data):
        query = QSqlQuery(db=self.db)
        ru = data.get("ru")
        en = data.get("en")
        sql = f"INSERT INTO {table} (ru, en) VALUES ('{ru}', '{en}')"
        query.prepare(sql)
        if not query.exec_():
            raise e.WrongDbQuery(query.lastError().text())

    def closeConnection(self):
        self.db.close()
