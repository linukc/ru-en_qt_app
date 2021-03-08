import sys
import exception as e
import database
from string import ascii_letters, digits

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QWidget
from ui_main import Ui_MainWindow
from ui_login import Ui_Form as Ui_Login


class LoginWindow(QWidget, Ui_Login):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.allowed_symbols = ascii_letters + digits
        self.SignInButton.clicked.connect(self.SignIn)
        self.SignUpButton.clicked.connect(self.SignUp)

    def SignBase(self):
        login = self.LoginLine.text()
        password = self.PasswordLine.text()
        if not login or not password:
            raise e.EmptyLine_LW()
        elif not alphabet_text(login, self.allowed_symbols):
            raise e.LoginForbiddenSymbols()
        elif not alphabet_text(password, self.allowed_symbols):
            raise e.PasswordForbiddenSymbols()

    def SignIn(self):
        self.SignBase()
        self.open_MainWindow()

    def SignUp(self):
        self.SignBase()

    def open_MainWindow(self):
        self.MainWindow = MainWindow(self)
        self.hide()
        self.MainWindow.show()


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args):
        super().__init__()
        self.setupUi(self)
        self.lang = {'ru': 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ', 'en': ascii_letters}
        self.first_lang = 'ru'
        self.second_lang = 'en'
        self.AddTranslationButton.clicked.connect(self.EnableAddingTranslation)
        self.CancelAddingTranslationButton.clicked.connect(self.CancelTranslationAdding)
        self.SubmitTranslationButton.clicked.connect(self.AddTranslation)
        self.SwapTablesButton.clicked.connect(self.SwapTables)
        self.SearchLine.textChanged.connect(self.SearchWord)
        #создать таблицу после логина юзера (т к от его название его таблицы = логин + пароль)
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

    def CancelTranslationAdding(self):
        self.SearchLine.setText('')
        self.TranslationLine.setText('')
        self.TranslationLine.setDisabled(True)
        self.SubmitTranslationButton.setDisabled(True)
        self.CancelAddingTranslationButton.setDisabled(True)
        
    def SwapTables(self):
        self.first_lang, self.second_lang = self.second_lang, self.first_lang

    def SearchWord(self):
        word = self.SearchLine.text()
        #print(word)


def alphabet_text(text, alphabet):
    return all([symb in alphabet for symb in text])


def except_hook(cls, exception, traceback):
    if e.MainWindow_BaseError in cls.__bases__:
        login_window.MainWindow.statusBar().showMessage(cls.error_msg, 5000)
    elif e.LoginWindow_BaseError in cls.__bases__:
        QMessageBox.critical(None, cls.error_title, cls.error_msg, QMessageBox.Cancel)
    elif e.TestWindow_BaseError in cls.__bases__:
        pass
    else:
        sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    login_window = LoginWindow()
    login_window.show()

    sys.excepthook = except_hook
    sys.exit(app.exec_())