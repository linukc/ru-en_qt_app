# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(0, 140, 801, 411))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.FirstTable = QtWidgets.QTableWidget(self.horizontalLayoutWidget_2)
        self.FirstTable.setEnabled(True)
        self.FirstTable.setObjectName("FirstTable")
        self.FirstTable.setColumnCount(0)
        self.FirstTable.setRowCount(0)
        self.horizontalLayout_2.addWidget(self.FirstTable)
        self.SwapTablesButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.SwapTablesButton.setObjectName("SwapTablesButton")
        self.horizontalLayout_2.addWidget(self.SwapTablesButton)
        self.SecondTable = QtWidgets.QTableWidget(self.horizontalLayoutWidget_2)
        self.SecondTable.setObjectName("SecondTable")
        self.SecondTable.setColumnCount(0)
        self.SecondTable.setRowCount(0)
        self.horizontalLayout_2.addWidget(self.SecondTable)
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 30, 801, 87))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.SubmitTranslationButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.SubmitTranslationButton.setEnabled(False)
        self.SubmitTranslationButton.setObjectName("SubmitTranslationButton")
        self.verticalLayout_6.addWidget(self.SubmitTranslationButton)
        self.CancelAddingTranslationButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.CancelAddingTranslationButton.setEnabled(False)
        self.CancelAddingTranslationButton.setObjectName("CancelAddingTranslationButton")
        self.verticalLayout_6.addWidget(self.CancelAddingTranslationButton)
        self.gridLayout_3.addLayout(self.verticalLayout_6, 1, 3, 1, 1)
        self.SearchLine = QtWidgets.QLineEdit(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SearchLine.sizePolicy().hasHeightForWidth())
        self.SearchLine.setSizePolicy(sizePolicy)
        self.SearchLine.setObjectName("SearchLine")
        self.gridLayout_3.addWidget(self.SearchLine, 1, 0, 1, 1)
        self.AddTranslationButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.AddTranslationButton.setEnabled(True)
        self.AddTranslationButton.setObjectName("AddTranslationButton")
        self.gridLayout_3.addWidget(self.AddTranslationButton, 1, 1, 1, 1)
        self.TranslationLine = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.TranslationLine.setEnabled(False)
        self.TranslationLine.setObjectName("TranslationLine")
        self.gridLayout_3.addWidget(self.TranslationLine, 1, 2, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.SwapTablesButton.setText(_translate("MainWindow", "<->"))
        self.SubmitTranslationButton.setText(_translate("MainWindow", "ОК"))
        self.CancelAddingTranslationButton.setText(_translate("MainWindow", "Отмена"))
        self.AddTranslationButton.setText(_translate("MainWindow", "Добавить"))
