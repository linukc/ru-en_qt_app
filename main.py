import sys
import exception as e
import database
from string import ascii_letters, digits

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem, QWidget
from ui_main import Ui_MainWindow
from ui_login import Ui_Form as Ui_Login


class LoginWindow(QWidget, Ui_Login):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.allowed_symbols = ascii_letters + digits
        self.login = None
        self.password = None
        self.db = database.DataBase()
        self.db.setUpConnection()

        self.SignInButton.clicked.connect(self.SignIn)
        self.SignUpButton.clicked.connect(self.SignUp)

    def SignChecks(self):
        self._login = self.LoginLine.text()
        self._password = self.PasswordLine.text()
        if not self._login or not self._password:
            raise e.EmptyLine_LW()
        elif not alphabet_text(self._login, self.allowed_symbols):
            raise e.LoginForbiddenSymbols()
        elif not alphabet_text(self._password, self.allowed_symbols):
            raise e.PasswordForbiddenSymbols()
    
    def SetUser(self):
        self.login = self._login
        self.password = self._password
        self.LoginLine.setText("")
        self.PasswordLine.setText("")

    def SignIn(self):
        self.SignChecks()
        if self.db.userExist(self._login, self._password):
            self.SetUser()
            self.open_MainWindow()
        else:
            raise e.WrongLoginOrPassword()

    def SignUp(self):
        self.SignChecks()
        if not self.db.userExist(self._login):
            self.SetUser()
            self.db.createTable(self.login+self.password)
            self.open_MainWindow()
        else:
            raise e.ExistedUser()

    def open_MainWindow(self):
        self.MainWindow = MainWindow(self)
        self.hide()
        self.MainWindow.show()


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args):
        super().__init__()
        self.setupUi(self)
        self.login_window = args[0]
        self.lang = {'ru': 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ', 'en': ascii_letters}
        self.first_lang = 'ru'
        self.second_lang = 'en'

        self.FirstTable.setColumnCount(2)
        ru_dict, en_dict = self.login_window.db.getDictionary(self.login_window.login+self.login_window.password)
        self.FirstTable.setRowCount(len(ru_dict))
        for i in range(len(ru_dict)):
            self.FirstTable.setItem(i, 0, QTableWidgetItem(ru_dict[i]))

        self.AddTranslationButton.clicked.connect(self.EnableAddingTranslation)
        self.CancelAddingTranslationButton.clicked.connect(self.CancelTranslationAdding)
        self.SubmitTranslationButton.clicked.connect(self.AddTranslation)
        self.SwapTablesButton.clicked.connect(self.SwapTables)
        self.StartTestButton.clicked.connect(self.StartTest)
        self.SearchLine.textChanged.connect(self.SearchWord)
        #db = database.MainWindowDataBase(self)
        #добавить кнопку выхода

    def EnableAddingTranslation(self):
        if not self.SearchLine.text():
            raise e.EmptyLine()
        elif not alphabet_text(self.SearchLine.text(), self.lang.get(self.first_lang)):
            raise e.Wrong_Search_Language()
        else:
            self.TranslationLine.setEnabled(True)
            self.SubmitTranslationButton.setEnabled(True)
            self.CancelAddingTranslationButton.setEnabled(True)

    def AddTranslation(self):
        if not self.SearchLine.text() or not self.TranslationLine.text():
            raise e.EmptyLine()
        elif not alphabet_text(self.SearchLine.text(), self.lang.get(self.first_lang)):
            raise e.Wrong_Search_Language()
        elif not alphabet_text(self.TranslationLine.text(), self.lang.get(self.second_lang)):
            raise e.Wrong_Translation_Language()
        else:
            self.CancelTranslationAdding()
            #слово уже может быть - тогда надо вставить его перевод

    def CancelTranslationAdding(self):
        self.SearchLine.setText('')
        self.TranslationLine.setText('')
        self.TranslationLine.setDisabled(True)
        self.SubmitTranslationButton.setDisabled(True)
        self.CancelAddingTranslationButton.setDisabled(True)
        
    def SwapTables(self):
        self.first_lang, self.second_lang = self.second_lang, self.first_lang

    def LoadTable(self, tableWidget):
        pass

    def StartTest(self):
        pass

    def SearchWord(self):
        word = self.SearchLine.text()
        if word and alphabet_text(word, self.lang.get(self.first_lang)):
            print(word)
        else:
            pass #показать все слова

    def add():
        pass
        #добавить кнопку sign out и отключение от базы с обнулением переменных инита


def alphabet_text(text, alphabet):
    return all([symb in alphabet for symb in text])


def except_hook(cls, exception, traceback):
    if e.MainWindow_BaseError in cls.__bases__:
        login_window.MainWindow.statusBar().showMessage(cls.error_msg, 5000)
    elif e.LoginWindow_BaseError in cls.__bases__:
        QMessageBox.critical(None, cls.error_title, cls.error_msg, QMessageBox.Cancel)
    elif e.TestWindow_BaseError in cls.__bases__:
        pass
    elif e.DB_BaseError in cls.__bases__:
        QMessageBox.critical(None, cls.error_title, cls.error_msg, QMessageBox.Cancel)
        sys.exit()
    else:
        sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    login_window = LoginWindow()
    login_window.show()

    sys.excepthook = except_hook
    sys.exit(app.exec_())