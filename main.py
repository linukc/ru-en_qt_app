import sys
import exception as e
import database
from string import ascii_letters, digits
import random

from PyQt5 import uic
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QAbstractItemView
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem, QCheckBox, QHBoxLayout
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
        self.CheckBoxes_group = None
        self.checkboxes_state_on_whole_dict = [QtCore.Qt.Unchecked] * len(self.first_dict)
        self.searching_indexes = None
        self.searching_mode = False
        #только такой порядок, потому что внутри 2 метода происходит временная отвязка
        self.FirstTable.cellChanged.connect(self.Checkbox_clicked)
        self.SetTablesLayout()
        #

        self.AddTranslationButton.clicked.connect(self.EnableAddingTranslation)
        self.CancelAddingTranslationButton.clicked.connect(self.CancelTranslationAdding)
        self.SubmitTranslationButton.clicked.connect(self.AddTranslation)
        self.SwapTablesButton.clicked.connect(self.SwapTables)
        self.StartTestButton.clicked.connect(self.StartTest)
        self.SearchLine.textChanged.connect(self.SearchWord)
        self.FirstTable.verticalScrollBar().valueChanged.connect(self.synchronize_scroll_bars)
        self.SelectAllCheckBox.stateChanged.connect(self.AllCheckBox_Pressed)
        #добавить кнопку выхода
        #выделить методы лишние по смыслу в _ 
    
    def AllCheckBox_Pressed(self):
        if self.SelectAllCheckBox.isChecked():
            state = QtCore.Qt.Checked
        else:
            state = QtCore.Qt.Unchecked
        for cb in self.CheckBoxes_group:
                cb.setCheckState(state)
        self.FirstTable.scrollToTop()

    def synchronize_scroll_bars(self):
        sliderValue = self.FirstTable.verticalScrollBar().value()
        self.SecondTable.verticalScrollBar().setValue(sliderValue)

    def Checkbox_clicked(self, row, column):
        self.FirstTable.scrollTo(self.FirstTable.model().index(row, column), QAbstractItemView.PositionAtCenter)
        self.synchronize_scroll_bars()
        
        if self.searching_mode:
            row = self.searching_indexes.get(row)
        if self.checkboxes_state_on_whole_dict[row] == QtCore.Qt.Checked:
            self.checkboxes_state_on_whole_dict[row] = QtCore.Qt.Unchecked
        else:
            self.checkboxes_state_on_whole_dict[row] = QtCore.Qt.Checked

    def SetTablesLayout(self, first_table_data=None, second_table_data=None):
        if not first_table_data or not second_table_data:
            first_table_data = self.first_dict
            second_table_data = self.second_dict
        
        self.CheckBoxes_group = []
        self.FirstTable.cellChanged.disconnect(self.Checkbox_clicked)
        j = 0
        column_count = 2
        #self.SelectAllCheckBox.setCheckState(QtCore.Qt.Unchecked)
        for lang, data, table in zip([self.first_lang, self.second_lang], 
                                     [first_table_data, second_table_data], 
                                     [self.FirstTable, self.SecondTable]):
            table.setColumnCount(column_count)
            table.setRowCount(len(data))
            for i in range(len(data)):
                table.setItem(i, 0, QTableWidgetItem(data[i]))
                if j == 0:
                    checkbox = QTableWidgetItem()
                    checkbox.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                    if self.searching_mode:
                        checkbox.setCheckState(self.checkboxes_state_on_whole_dict[self.searching_indexes.get(i)])
                    else:
                        checkbox.setCheckState(self.checkboxes_state_on_whole_dict[i])
                    checkbox.setData(QtCore.Qt.UserRole, checkbox.checkState())
                    self.CheckBoxes_group.append(checkbox)
                    table.setItem(i, 1, checkbox) 
            table.resizeColumnsToContents()
            j += 1
            column_count = 1
        self.FirstTable.scrollToTop()
        self.FirstTable.cellChanged.connect(self.Checkbox_clicked)

    def SearchWord(self):
        #можно делать оптимизацию поиска - например искать уже в оптенциальных словах если человек продолжает дополнять слово буквами
        # если нету слова то моказывает все а должен ничего
        # баг если вводить в поиск несуществующее слово
        goal_word = self.SearchLine.text()
        if not alphabet_text(goal_word, self.lang.get(self.first_lang)):
            raise e.Wrong_Search_Language()
        if goal_word:
            words = [word for word in self.first_dict if goal_word in word]
            if not words:
                raise e.WordIsMissing()
            words_indices = [self.first_dict.index(word) for word in self.first_dict if goal_word in word]
            self.searching_indexes = {i:j for i, j in enumerate(words_indices)}
            first_dict = [self.first_dict[i] for i in words_indices]
            second_dict = [self.second_dict[i] for i in words_indices]
            self.searching_mode = True
            self.SetTablesLayout(first_dict, second_dict)
        else:
            self.searching_mode = False
            self.SetTablesLayout()

    def EnableAddingTranslation(self):
        if not self.SearchLine.text():
            raise e.EmptyLine()
        elif not alphabet_text(self.SearchLine.text(), self.lang.get(self.first_lang)):
            raise e.Wrong_Search_Language()
        elif self.FirstTable.rowCount():
            raise e.ExistedWord()
        else:
            self.SearchLine.setDisabled(True)
            self.TranslationLine.setEnabled(True)
            self.SubmitTranslationButton.setEnabled(True)
            self.CancelAddingTranslationButton.setEnabled(True)


    def AddTranslation(self):
        if not self.TranslationLine.text():
            raise e.EmptyLine()
        elif not alphabet_text(self.TranslationLine.text(), self.lang.get(self.second_lang)):
            raise e.Wrong_Translation_Language()
        else:
            self.CancelTranslationAdding()

    def CancelTranslationAdding(self):
        self.SearchLine.setText('')
        self.TranslationLine.setText('')
        self.SearchLine.setEnabled(True)
        self.TranslationLine.setDisabled(True)
        self.SubmitTranslationButton.setDisabled(True)
        self.CancelAddingTranslationButton.setDisabled(True)
        
    def SwapTables(self):
        self.FirstTable.clear()
        self.SecondTable.clear()
        self.first_lang, self.second_lang = self.second_lang, self.first_lang
        self.first_dict, self.second_dict = self.second_dict, self.first_dict
        self.SetTablesLayout()

    def StartTest(self):
        pass

    def add():
        pass
        #добавить кнопку sign out и отключение от базы с обнулением переменных инита


def alphabet_text(text, alphabet):
    return all([symb in alphabet for symb in text])


def except_hook(cls, exception, traceback):
    if e.MainWindow_BaseError in cls.__bases__:
        login_window.MainWindow.statusBar().showMessage(cls.error_msg, 3000)
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