from PyQt5 import uic
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QAbstractItemView
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem, QCheckBox, QHBoxLayout

from ui_main import Ui_MainWindow
from ui_login import Ui_Form as Ui_Login
from ui_test import Ui_Form as Ui_Test

import sys
import exception as e
import database
import random
from string import ascii_letters, digits


class LoginWindow(QWidget, Ui_Login):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.allowed_symbols = ascii_letters + digits
        self.login = None
        self.password = None
        self.db = database.DataBase()
        self.db.setUpConnection()

        self.SignInButton.clicked.connect(self.signIn)
        self.SignUpButton.clicked.connect(self.signUp)
    
    def setUser(self):
        self.login = self._login
        self.password = self._password
        self.LoginLine.setText("")
        self.PasswordLine.setText("")

    def signIn(self):
        self._loginChecks()
        if self.db.isUserExist(self._login, self._password):
            self.setUser()
            self.openMainWindow()
        else:
            raise e.WrongLoginOrPassword()

    def signUp(self):
        self._loginChecks()
        if not self.db.isUserExist(self._login):
            self.setUser()
            self.db.createTable(self.login+self.password)
            self.openMainWindow()
        else:
            raise e.ExistedUser()

    def openMainWindow(self):
        self.MainWindow = MainWindow(self)
        self.LoginLine.setText("")
        self.PasswordLine.setText("")
        self.hide()
        self.MainWindow.show()

    def closeEvent(self, event=None):
        self.db.closeConnection()

    def _loginChecks(self):
        self._login = self.LoginLine.text()
        self._password = self.PasswordLine.text()
        if not self._login or not self._password:
            raise e.EmptyLine_LW()
        elif not are_symbols_in_alphabet(self._login, self.allowed_symbols):
            raise e.LoginForbiddenSymbols()
        elif not are_symbols_in_alphabet(self._password, self.allowed_symbols):
            raise e.PasswordForbiddenSymbols()


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args):
        super().__init__()
        self.setupUi(self)
        self._login_window = args[0]
        self.lang = {'ru': 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ', 'en': ascii_letters}
        self.first_lang = 'ru'
        self.second_lang = 'en'
        self.first_dict, self.second_dict = self._login_window.db.getDictionary(self._login_window.login+self._login_window.password)
        self.checkboxes_state_on_whole_dict = [QtCore.Qt.Unchecked] * len(self.first_dict)
        self._first_dict_search = []
        self._second_dict_search = []
        self._checkBoxes_group = None
        self._searching_indexes = None
        self.searching_mode = False
        
        #только такой порядок, потому что внутри второго метода происходит временная отвязка
        self.FirstTable.cellChanged.connect(self._changeCheckboxState)
        self._setTablesLayout()
        #
        self.AddTranslationButton.clicked.connect(self._enableAddingTranslation)
        self.CancelAddingTranslationButton.clicked.connect(self._cancelTranslationAdding)
        self.SubmitTranslationButton.clicked.connect(self.addTranslation)
        self.SwapTablesButton.clicked.connect(self.swapTables)
        self.StartTestButton.clicked.connect(self.startTest)
        self.SearchLine.textChanged.connect(self.searchWord)
        self.FirstTable.verticalScrollBar().valueChanged.connect(self._synchronizeScrollBars)
        self.SelectAllCheckBox.stateChanged.connect(self.selectAll)
        self.SignOutButton.clicked.connect(self.signOut)

    def addTranslation(self):
        translation = self.TranslationLine.text()
        if not translation:
            raise e.EmptyLine()
        elif not are_symbols_in_alphabet(translation, self.lang.get(self.second_lang)):
            raise e.Wrong_Translation_Language()
        else:
            word = self.SearchLine.text()
            self._login_window.db.AddPair_WordTranslation(self._login_window.login+self._login_window.password,
                                                         {self.first_lang: word, self.second_lang: translation})
            self.first_dict.append(word)
            self.second_dict.append(translation)
            self.checkboxes_state_on_whole_dict.append(QtCore.Qt.Unchecked)
            if self.searching_mode:
                self.searching_mode = False
                self._first_dict_search = []
                self._second_dict_search = []
            #обязательно в таком порядке чтобы не триггерить изменение текста и функцию поиска
            self._setTablesLayout()
            self._cancelTranslationAdding()
            #
    
    def searchWord(self):
        #можно делать оптимизацию поиска - например искать уже в оптенциальных словах если человек продолжает дополнять слово буквами
        goal_word = self.SearchLine.text()
        if not are_symbols_in_alphabet(goal_word, self.lang.get(self.first_lang)):
            raise e.Wrong_Search_Language()
        if goal_word:
            words = [word for word in self.first_dict if goal_word in word]
            if not words:
                raise e.WordIsMissing()
            words_indices = [self.first_dict.index(word) for word in self.first_dict if goal_word in word]
            self._searching_indexes = {i:j for i, j in enumerate(words_indices)}
            self._first_dict_search = [self.first_dict[i] for i in words_indices]
            self._second_dict_search = [self.second_dict[i] for i in words_indices]
            self.searching_mode = True
        else:
            self.searching_mode = False
            self._first_dict_search = []
            self._second_dict_search = []
        self._setTablesLayout()

    def selectAll(self):
        if self.SelectAllCheckBox.isChecked():
            state = QtCore.Qt.Checked
        else:
            state = QtCore.Qt.Unchecked
        for cb in self._checkBoxes_group:
                cb.setCheckState(state)
        self.FirstTable.scrollToTop()

    def swapTables(self):
        self.FirstTable.clear()
        self.SecondTable.clear()
        self.first_lang, self.second_lang = self.second_lang, self.first_lang
        self.first_dict, self.second_dict = self.second_dict, self.first_dict
        if self.searching_mode:
            self._first_dict_search, self._second_dict_search = self._second_dict_search, self._first_dict_search
        self._setTablesLayout()

    def startTest(self):
        self._generateTest()
        self.hide()
        self.test_window = TestWindow(self)
        self.test_window.show()

    def signOut(self):
        self.hide()
        self._login_window.show()

    def closeEvent(self, event=None):
        self._login_window.db.closeConnection()

    @staticmethod
    def _generateAnswer(answer, other):
        while True:
            variants = random.sample(other, 4)   
            if answer not in variants:
                idx = random.randint(0, 3)
                variants[idx] = answer
                return variants  
    
    def _generateTest(self):
        indexes = [i for i, state in enumerate(self.checkboxes_state_on_whole_dict) if state == QtCore.Qt.Checked]
        if len(indexes) < 1:
            raise e.SmallTestSet()
        fd = list(map(lambda i: self.first_dict[i], indexes))
        sd = list(map(lambda i: self.second_dict[i], indexes))
        self.test_data = {}
        for i, word in enumerate(fd, 1):
            self.test_data[i] = [word, self._generateAnswer(sd[i-1], self.second_dict), sd[i-1]]

    def _enableAddingTranslation(self):
        if not self.SearchLine.text():
            raise e.EmptyLine()
        elif not are_symbols_in_alphabet(self.SearchLine.text(), self.lang.get(self.first_lang)):
            raise e.Wrong_Search_Language()
        elif self.SearchLine.text() in self.first_dict:
            raise e.ExistedWord()
        else:
            self.SearchLine.setDisabled(True)
            self.TranslationLine.setEnabled(True)
            self.SubmitTranslationButton.setEnabled(True)
            self.CancelAddingTranslationButton.setEnabled(True)

    def _cancelTranslationAdding(self):
        self.SearchLine.setText('')
        self.TranslationLine.setText('')
        self.SearchLine.setEnabled(True)
        self.TranslationLine.setDisabled(True)
        self.SubmitTranslationButton.setDisabled(True)
        self.CancelAddingTranslationButton.setDisabled(True)

    def _setTablesLayout(self):
        if self.searching_mode:
            first_table_data = self._first_dict_search
            second_table_data = self._second_dict_search
        else:
            first_table_data = self.first_dict
            second_table_data = self.second_dict

        self._checkBoxes_group = []
        self.FirstTable.cellChanged.disconnect(self._changeCheckboxState)
        j = 0
        column_count = 2
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
                        checkbox.setCheckState(self.checkboxes_state_on_whole_dict[self._searching_indexes.get(i)])
                    else:
                        checkbox.setCheckState(self.checkboxes_state_on_whole_dict[i])
                    checkbox.setData(QtCore.Qt.UserRole, checkbox.checkState())
                    self._checkBoxes_group.append(checkbox)
                    table.setItem(i, 1, checkbox) 
            table.resizeColumnsToContents()
            j += 1
            column_count = 1
        self.FirstTable.scrollToTop()
        self.FirstTable.cellChanged.connect(self._changeCheckboxState)

    def _synchronizeScrollBars(self):
        sliderValue = self.FirstTable.verticalScrollBar().value()
        self.SecondTable.verticalScrollBar().setValue(sliderValue)

    def _changeCheckboxState(self, row, column):
        self.FirstTable.scrollTo(self.FirstTable.model().index(row, column), QAbstractItemView.PositionAtCenter)
        self._synchronizeScrollBars()
        
        if self.searching_mode:
            row = self._searching_indexes.get(row)
        if self.checkboxes_state_on_whole_dict[row] == QtCore.Qt.Checked:
            self.checkboxes_state_on_whole_dict[row] = QtCore.Qt.Unchecked
        else:
            self.checkboxes_state_on_whole_dict[row] = QtCore.Qt.Checked


class TestWindow(QMainWindow, Ui_Test):
    def __init__(self, *args):
        super().__init__()
        self.setupUi(self)
        self._main_window = args[0]
        self.page_id = 1
        self.count_of_right_answers = 0
        self._user_variant_button = None

        self.initPage(self.page_id)
        self.ForwardButton.clicked.connect(self.showNextQ)
        self.buttonGroup.buttonClicked.connect(self._userVariantHandler)

    def initPage(self, number):
        self.WordLabel.setText(self._main_window.test_data.get(number)[0])
        self.answer = self._main_window.test_data.get(number)[2]
        for button, variant in zip(self.buttonGroup.buttons(), self._main_window.test_data.get(number)[1]):
            button.setText(variant)
            button.setStyleSheet("background-color: none")
            if variant == self.answer:
                self.answer_button = button
        self.CounterLabel.setText(f"{self.page_id}/{len(self._main_window.test_data)}")

    def showNextQ(self):
        if not self._user_variant_button:
            raise e.NoAnswerSelected()
        self.answer_button.setStyleSheet("background-color: lightgreen")
        if self.answer_button.text() != self._user_variant_button.text():
            self._user_variant_button.setStyleSheet("background-color: red")
        else:
            self.count_of_right_answers += 1
        self._disableUI()
        if self.page_id < len(self._main_window.test_data):
            self.page_id += 1
            QtCore.QTimer.singleShot(1000, self._redirectToTheNextQ)
        else:
            self._showCurrentResult()
            QtCore.QTimer.singleShot(3000, self.closeEvent)
        self._enableUI()
            
    def closeEvent(self, event=None):
        self.hide()
        self._main_window.show()
    
    def _showCurrentResult(self):
        self.ResultLabel.setText(f"You have reached {self.count_of_right_answers} out of {self.page_id}")

    def _disableUI(self):
        for button in self.buttonGroup.buttons():
            button.setDisabled(True)
        self.ForwardButton.setDisabled(True)

    def _enableUI(self):
        for button in self.buttonGroup.buttons():
            button.setEnabled(True)
        self.ForwardButton.setEnabled(True)

    def _redirectToTheNextQ(self):
        self.initPage(self.page_id)

    def _userVariantHandler(self):
        for button in self.sender().buttons():
            if button.isChecked():
                self._user_variant_button = button 


def are_symbols_in_alphabet(text, alphabet):
    return all([symb in alphabet for symb in text])

def except_hook(cls, exception, traceback):
    if e.MainWindow_BaseError in cls.__bases__:
        login_window.MainWindow.statusBar().showMessage(cls.error_msg, 2000)
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