# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.gridLayoutWidget = QtWidgets.QWidget(Form)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(120, 50, 160, 80))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.LoginLine = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.LoginLine.setObjectName("LoginLine")
        self.gridLayout.addWidget(self.LoginLine, 0, 1, 1, 1)
        self.PasswordLine = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.PasswordLine.setObjectName("PasswordLine")
        self.gridLayout.addWidget(self.PasswordLine, 1, 1, 1, 1)
        self.LoginLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.LoginLabel.setObjectName("LoginLabel")
        self.gridLayout.addWidget(self.LoginLabel, 0, 0, 1, 1)
        self.PasswordLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.PasswordLabel.setObjectName("PasswordLabel")
        self.gridLayout.addWidget(self.PasswordLabel, 1, 0, 1, 1)
        self.horizontalLayoutWidget = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(120, 160, 160, 80))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.SignInButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.SignInButton.setObjectName("SignInButton")
        self.horizontalLayout.addWidget(self.SignInButton)
        self.SignUpButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.SignUpButton.setObjectName("SignUpButton")
        self.horizontalLayout.addWidget(self.SignUpButton)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.LoginLabel.setText(_translate("Form", "Login"))
        self.PasswordLabel.setText(_translate("Form", "Password"))
        self.SignInButton.setText(_translate("Form", "Sign in"))
        self.SignUpButton.setText(_translate("Form", "Sign up"))
