import sys
import exception as e
import database
from string import ascii_letters, digits

from PyQt5 import uic
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem, QCheckBox, QHBoxLayout, QWidget, QAbstractItemView
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

        self.first_dict, self.second_dict = self.login_window.db.getDictionary(self.login_window.login+self.login_window.password)
        self.checkeditem = len(self.first_dict) * [False]
        self.SetTablesLayout()
        self.FirstTable.cellChanged.connect(self.Checkbox_clicked)
        

        self.AddTranslationButton.clicked.connect(self.EnableAddingTranslation)
        self.CancelAddingTranslationButton.clicked.connect(self.CancelTranslationAdding)
        self.SubmitTranslationButton.clicked.connect(self.AddTranslation)
        self.SwapTablesButton.clicked.connect(self.SwapTables)
        self.StartTestButton.clicked.connect(self.StartTest)
        self.SearchLine.textChanged.connect(self.SearchWord)
        #db = database.MainWindowDataBase(self)
        #добавить кнопку выхода

    def Checkbox_clicked(self, row, column):
        #self.FirstTable.scrollTo(self.FirstTable.model().index(row, column))
        #добавить изменение скролбара до центра если это возможно (по краям проверки) и вынести из функции чтобы не искажать смысл
        self.FirstTable.scrollTo(self.FirstTable.model().index(row, column), QAbstractItemView.PositionAtCenter)

        print(row, column)
        item = self.FirstTable.item(row, column)
        print(item.checkState())

    def SetTablesLayout(self):
        j = 0
        column_count = 2
        for lang, data, table in zip([self.first_lang, self.second_lang], 
                                                  [self.first_dict, self.second_dict], 
                                                  [self.FirstTable, self.SecondTable]):
            table.setColumnCount(column_count)
            table.setRowCount(len(data))
            for i in range(len(data)):
                table.setItem(i, 0, QTableWidgetItem(data[i]))
                if j == 0:
                    checkbox = QTableWidgetItem()
                    checkbox.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                    checkbox.setCheckState(QtCore.Qt.Unchecked)
                    checkbox.setData(QtCore.Qt.UserRole, checkbox.checkState())
                    table.setItem(i, 1, checkbox) 
            table.resizeColumnsToContents()
            j += 1
            column_count = 1


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
        self.FirstTable.clear()
        self.SecondTable.clear()
        self.first_lang, self.second_lang = self.second_lang, self.first_lang
        self.first_dict, self.second_dict = self.second_dict, self.first_dict
        self.SetTablesLayout()

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