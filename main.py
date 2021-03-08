import sys
import exception as e
import database
from string import ascii_letters as en_letters

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui_main import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.lang = {'ru': 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ', 'en': en_letters}
        self.first_lang = 'ru'
        self.second_lang = 'en'
        self.AddTranslationButton.clicked.connect(self.EnableAddingTranslation)
        self.CancelAddingTranslationButton.clicked.connect(self.CancelTranslationAdding)
        self.SubmitTranslationButton.clicked.connect(self.AddTranslation)
        #создать таблицу после логина юзера (т к от его название его таблицы = логин + пароль)
        #db = database.MainWindowDataBase(self)

    def EnableAddingTranslation(self):
        if not self.SearchLine.text():
            raise e.EmptyLine()
        elif not all([symb in self.lang.get(self.first_lang) for symb in self.SearchLine.text()]):
            raise e.Wrong_Search_Language()
        else:
            self.TranslationLine.setEnabled(True)
            self.SubmitTranslationButton.setEnabled(True)
            self.CancelAddingTranslationButton.setEnabled(True)

    def AddTranslation(self):
        if not self.SearchLine.text() or not self.TranslationLine.text():
            raise e.EmptyLine()
        elif not all([symb in self.lang.get(self.first_lang) for symb in self.SearchLine.text()]):
            raise e.Wrong_Search_Language()
        elif not all([symb in self.lang.get(self.second_lang) for symb in self.TranslationLine.text()]):
            raise e.Wrong_Translation_Language
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
        

def except_hook(cls, exception, traceback):
    if e.MainWindow_BaseError in cls.__bases__:
        QMessageBox.critical(None, cls.error_title, cls.error_msg, QMessageBox.Cancel)
        #main_window.statusBar().showMessage(cls.error_msg, 5000)
    elif e.LoginWindow_BaseError in cls.__bases__:
        pass
    elif e.TestWindow_BaseError in cls.__bases__:
        pass
    else:
        sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())