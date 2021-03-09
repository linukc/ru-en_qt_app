from PyQt5.QtSql import QSqlDatabase, QSqlQuery
import exception as e


# а в коде использовать только DataBase.getwords()
class DataBase():
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
        #query.addBindValue(name)
        if not query.exec_():
            raise e.WrongDbQuery(query.lastError().text())
        #query.exec_('SELECT * FROM login')
        #while query.next():
            #print(query.value("id"))

    def userExist(self, login, password=None):
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
        
        ru = []
        en = []
        while query.next():
            ru.append(query.value("ru"))
            en.append(query.value("en"))
        
        return ru, en

    def closeConnection(self):
        self.db.close()
