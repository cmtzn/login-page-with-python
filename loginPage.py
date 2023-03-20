from PyQt5 import *
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import *


import mysql.connector as sql
mydb = sql.connect(
    host = 'localhost',
    user = 'root',
    password = 'root',
    database = 'libarydb'
)

import sys

class myLogin(QDialog):
    def __init__(self):
        super(myLogin, self).__init__()
        uic.loadUi('loginpage.ui', self)
        self.loginbut.clicked.connect(self.searchButfunc)
        self.closebut.clicked.connect(self.closebutfunc)
    
    def searchButfunc(self):
        username = self.usernametxt.toPlainText().strip().lower()
        password = self.passwordtxt.text().strip()
        mycursor = mydb.cursor()
        mycursor.execute("select lower(username),password from login_tb")
        result = mycursor.fetchall()
        signal = 0
        for x in result:
            if username in x:
                data = list(x)
                name = data[0]
                pwd = data[1]
                signal = 1
                if username == name and password == pwd:
                         self.hide()  # Hide the login page UI
                         self.main_menu = searchEmployee()  # Create an instance of the main menu class
                         self.main_menu.show()  # Show the main menu UI 
                         

                else:
                    from PyQt5.QtWidgets import QMessageBox
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setWindowTitle("Login Unsuccessful")
                    msg.setText("Username or Password do not match....")
                    msg.exec_()

        if signal == 0:
            from PyQt5.QtWidgets import QMessageBox
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Login Error1")
            msg.setText("Invalid Login, Try Again.")
            msg.exec_()
    
    def closebutfunc(self):
        QApplication.quit() 

class searchEmployee(QDialog):
    def __init__(self):
        super(searchEmployee, self).__init__()
        uic.loadUi('Employeelist.ui', self)
        self.searchBut.clicked.connect(self.searchButfunc) #self. means making global variable
    
    def searchButfunc(self):
        username = self.employeeNametxt.toPlainText().strip().lower()
        print(username)
        import mysql.connector as sql
        mydb = sql.connect(
            host = 'localhost',
            user = 'root',
            password = 'root',
            database = 'empdb1'
        )

        mycursor = mydb.cursor()
        mycursor.execute("select lower(name),address from customers")
        result = mycursor.fetchall()
        signal = 0
        for x in result:
            if username in x:
                data = list(x)
                name = data[0]
                address = data[1]
                signal = 1
                self.searchResulttxt.clear()
                self.searchResulttxt.appendPlainText("Name: "+name+"\n")
                self.searchResulttxt.appendPlainText("Address: "+address)
        if signal == 0:
            self.searchResulttxt.clear()
            self.searchResulttxt.appendPlainText("No Data Found For This Employee!")


app = QApplication([])
win = myLogin()
win.show()
sys.exit(app.exec())