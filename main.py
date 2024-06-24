import sys
from PyQt5.QtWidgets import *
from login import Ui_MainWindow
from lib_gui import lib_gui_MainWindow
import psycopg2
from psycopg2 import Error

class LoginWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.login)

    def connect_bd(self, username, password):
        try:
            conn = psycopg2.connect(
                dbname='kr1',
                user=username,
                password=password,
                host='localhost'
            )

            return conn
        except psycopg2.Error:
            QMessageBox.warning(self, 'Ошибка!', 'Не удалось подключится к БД.')
            return None

    def aut_user(self, conn, username):
        if conn is None:
            return None

        values = ('lib1',
                  'rea1',
                  'adm1')

        cursor = conn.cursor()
        for value in values:
            cursor.execute(
                f"SELECT rolname FROM pg_roles WHERE pg_has_role(rolname, '{value}', 'member') and rolname = '{username}';")
            result = cursor.fetchone()
            if result is not None:
                role = value
                break
        cursor.close()
        return role

    def login(self):
        username = self.ui.lineEdit.text()
        password = self.ui.lineEdit_2.text()

        conn = self.connect_bd(username, password)
        role = self.aut_user(conn, username)
        if conn is not None:
            if role == 'lib1' or role == 'rea1' or role == 'adm1':
                self.act_win = lib_gui_Window(conn, self)
                self.act_win.show()
                self.hide()
            else:
                QMessageBox.warning(self, 'Ошибка!', 'Такой роли не существует.')
        else:
            QMessageBox.warning(self, 'Ошибка!', 'Неверный логин или пароль.')

class lib_gui_Window(QMainWindow):
    def __init__(self, conn, parent=None):
        super().__init__(parent)
        self.lib_gui_ui = lib_gui_MainWindow()
        self.lib_gui_ui.setupUi(self)

        self.conn = conn

        self.lib_gui_ui.comboBox.textActivated.connect(self.onActivated)
        self.setCombo()

        self.lib_gui_ui.pushButton_and_or_2.clicked.connect(lambda: self.change_button(self.lib_gui_ui.pushButton_and_or_2))
        self.lib_gui_ui.pushButton_and_or_3.clicked.connect(lambda: self.change_button(self.lib_gui_ui.pushButton_and_or_3))
        self.lib_gui_ui.pushButton_and_or_4.clicked.connect(lambda: self.change_button(self.lib_gui_ui.pushButton_and_or_4))
        self.lib_gui_ui.pushButton_and_or_5.clicked.connect(lambda: self.change_button(self.lib_gui_ui.pushButton_and_or_5))
        self.lib_gui_ui.pushButton_and_or_6.clicked.connect(lambda: self.change_button(self.lib_gui_ui.pushButton_and_or_6))
        self.lib_gui_ui.pushButton_and_or_7.clicked.connect(lambda: self.change_button(self.lib_gui_ui.pushButton_and_or_7))
        self.lib_gui_ui.pushButton_and_or_8.clicked.connect(lambda: self.change_button(self.lib_gui_ui.pushButton_and_or_8))
        self.lib_gui_ui.pushButton_and_or_9.clicked.connect(lambda: self.change_button(self.lib_gui_ui.pushButton_and_or_9))

        self.table = "author"
        self.colcount = 5;

        self.lib_gui_ui.pushButton_filter.clicked.connect(self.filter)
        self.lib_gui_ui.pushButton_add.clicked.connect(self.add)
        self.lib_gui_ui.pushButton_delete.clicked.connect(self.delete)
        self.lib_gui_ui.pushButton_update.clicked.connect(self.update)

    def change_button(self, button):
        if button.text() == "AND":
            button.setText("OR")
        else:
            button.setText("AND")

    def setCombo(self):
        self.lib_gui_ui.comboBox.addItem("Авторы")
        self.lib_gui_ui.comboBox.addItem("Жанры")
        self.lib_gui_ui.comboBox.addItem("Библиотекари")
        self.lib_gui_ui.comboBox.addItem("Литература")
        self.lib_gui_ui.comboBox.addItem("Движение книг")
        self.lib_gui_ui.comboBox.addItem("Пени")
        self.lib_gui_ui.comboBox.addItem("Издательство")
        self.lib_gui_ui.comboBox.addItem("Читатели")

    def onActivated(self):
        text = self.lib_gui_ui.comboBox.currentText()
        if text == 'Авторы':
            self.table = "author"
            self.lib_gui_ui.tableWidget.setSortingEnabled(False)
            self.showAutor()
            self.lib_gui_ui.tableWidget.setSortingEnabled(True)
        elif text == 'Жанры':
            self.table = "genre"
            self.lib_gui_ui.tableWidget.setSortingEnabled(False)
            self.showGenre()
            self.lib_gui_ui.tableWidget.setSortingEnabled(True)
        elif text == 'Библиотекари':
            self.table = "librarian"
            self.lib_gui_ui.tableWidget.setSortingEnabled(False)
            self.showLibrarian()
            self.lib_gui_ui.tableWidget.setSortingEnabled(True)
        elif text == 'Литература':
            self.table = "literature"
            self.lib_gui_ui.tableWidget.setSortingEnabled(False)
            self.showLiterature()
            self.lib_gui_ui.tableWidget.setSortingEnabled(True)
        elif text == 'Движение книг':
            self.table = "literature_movement"
            self.lib_gui_ui.tableWidget.setSortingEnabled(False)
            self.showLiterature_movement()
            self.lib_gui_ui.tableWidget.setSortingEnabled(True)
        elif text == 'Пени':
            self.table = "penalties"
            self.lib_gui_ui.tableWidget.setSortingEnabled(False)
            self.showPenalties()
            self.lib_gui_ui.tableWidget.setSortingEnabled(True)
        elif text == 'Издательство':
            self.table = "publishing_house"
            self.lib_gui_ui.tableWidget.setSortingEnabled(False)
            self.showPublishing_house()
            self.lib_gui_ui.tableWidget.setSortingEnabled(True)
        elif text == 'Читатели':
            self.table = "reader"
            self.lib_gui_ui.tableWidget.setSortingEnabled(False)
            self.showReader()
            self.lib_gui_ui.tableWidget.setSortingEnabled(True)

    def showAutor(self):
        self.colcount = 5
        self.lib_gui_ui.tableWidget.setColumnCount(self.colcount)
        row_labels = ["id", "Фамилия", "Имя", "Отчество", "Дата рождения"]
        self.lib_gui_ui.tableWidget.setHorizontalHeaderLabels(row_labels)

        self.buttons_show = [self.lib_gui_ui.pushButton_and_or_2, self.lib_gui_ui.pushButton_and_or_3,
                             self.lib_gui_ui.pushButton_and_or_4, self.lib_gui_ui.pushButton_and_or_5]
        for button in self.buttons_show:
            button.show()

        self.buttons_hide = [self.lib_gui_ui.pushButton_and_or_6, self.lib_gui_ui.pushButton_and_or_7,
                             self.lib_gui_ui.pushButton_and_or_8, self.lib_gui_ui.pushButton_and_or_9]
        for button in self.buttons_hide:
            button.hide()

        self.textEdit_show = [self.lib_gui_ui.textEdit_1, self.lib_gui_ui.textEdit_2,
                              self.lib_gui_ui.textEdit_3, self.lib_gui_ui.textEdit_4,
                              self.lib_gui_ui.textEdit_5]
        for textEdit in self.textEdit_show:
            textEdit.show()

        self.textEdit_hide = [self.lib_gui_ui.textEdit_6, self.lib_gui_ui.textEdit_7,
                              self.lib_gui_ui.textEdit_8, self.lib_gui_ui.textEdit_9]
        for textEdit in self.textEdit_hide:
            textEdit.hide()

        self.textBrowser_show = [self.lib_gui_ui.textBrowser_1, self.lib_gui_ui.textBrowser_2,
                                 self.lib_gui_ui.textBrowser_3, self.lib_gui_ui.textBrowser_4,
                                 self.lib_gui_ui.textBrowser_5]
        for textBrowser in self.textBrowser_show:
            textBrowser.show()

        self.textBrowser_hide = [self.lib_gui_ui.textBrowser_6, self.lib_gui_ui.textBrowser_7,
                                 self.lib_gui_ui.textBrowser_8, self.lib_gui_ui.textBrowser_9]
        for textBrowser in self.textBrowser_hide:
            textBrowser.hide()

        self.textEdit_setText = [self.lib_gui_ui.textEdit_1, self.lib_gui_ui.textEdit_2,
                                 self.lib_gui_ui.textEdit_3, self.lib_gui_ui.textEdit_4,
                                 self.lib_gui_ui.textEdit_5]
        for textEdit in self.textEdit_setText:
            textEdit.setText("")

        self.lib_gui_ui.textBrowser_1.setText(row_labels[0])
        self.lib_gui_ui.textBrowser_2.setText(row_labels[1])
        self.lib_gui_ui.textBrowser_3.setText(row_labels[2])
        self.lib_gui_ui.textBrowser_4.setText(row_labels[3])
        self.lib_gui_ui.textBrowser_5.setText(row_labels[4])

        cursor = self.conn.cursor()
        cursor.execute(f"SELECT * FROM author")
        bib = cursor.fetchall()

        self.lib_gui_ui.tableWidget.setRowCount(len(bib))
        for i in range(len(bib)):
            for j in range(self.colcount):
                self.lib_gui_ui.tableWidget.setItem(i, j, QTableWidgetItem(str(bib[i][j])))

        self.lib_gui_ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    def showGenre(self):
        self.colcount = 2
        self.lib_gui_ui.tableWidget.setColumnCount(self.colcount)
        row_labels = ["id", "Жанр"]
        self.lib_gui_ui.tableWidget.setHorizontalHeaderLabels(row_labels)

        self.buttons_show = [self.lib_gui_ui.pushButton_and_or_2]
        for button in self.buttons_show:
            button.show()

        self.buttons_hide = [self.lib_gui_ui.pushButton_and_or_3,
                             self.lib_gui_ui.pushButton_and_or_4, self.lib_gui_ui.pushButton_and_or_5,
                             self.lib_gui_ui.pushButton_and_or_6, self.lib_gui_ui.pushButton_and_or_7,
                             self.lib_gui_ui.pushButton_and_or_8, self.lib_gui_ui.pushButton_and_or_9]
        for button in self.buttons_hide:
            button.hide()

        self.textEdit_show = [self.lib_gui_ui.textEdit_1, self.lib_gui_ui.textEdit_2]
        for textEdit in self.textEdit_show:
            textEdit.show()

        self.textEdit_hide = [self.lib_gui_ui.textEdit_3, self.lib_gui_ui.textEdit_4,
                              self.lib_gui_ui.textEdit_5, self.lib_gui_ui.textEdit_6,
                              self.lib_gui_ui.textEdit_7, self.lib_gui_ui.textEdit_8,
                              self.lib_gui_ui.textEdit_9]
        for textEdit in self.textEdit_hide:
            textEdit.hide()

        self.textBrowser_show = [self.lib_gui_ui.textBrowser_1, self.lib_gui_ui.textBrowser_2]
        for textBrowser in self.textBrowser_show:
            textBrowser.show()

        self.textBrowser_hide = [self.lib_gui_ui.textBrowser_3, self.lib_gui_ui.textBrowser_4,
                                 self.lib_gui_ui.textBrowser_5, self.lib_gui_ui.textBrowser_6,
                                 self.lib_gui_ui.textBrowser_7, self.lib_gui_ui.textBrowser_8,
                                 self.lib_gui_ui.textBrowser_9]
        for textBrowser in self.textBrowser_hide:
            textBrowser.hide()

        self.textEdit_setText = [self.lib_gui_ui.textEdit_1, self.lib_gui_ui.textEdit_2]
        for textEdit in self.textEdit_setText:
            textEdit.setText("")

        self.lib_gui_ui.textBrowser_1.setText(row_labels[0])
        self.lib_gui_ui.textBrowser_2.setText(row_labels[1])

        cursor = self.conn.cursor()
        cursor.execute(f"SELECT * FROM genre")
        bib = cursor.fetchall()

        self.lib_gui_ui.tableWidget.setRowCount(len(bib))
        for i in range(len(bib)):
            for j in range(self.colcount):
                self.lib_gui_ui.tableWidget.setItem(i, j, QTableWidgetItem(str(bib[i][j])))

        self.lib_gui_ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    def showLibrarian(self):
        colcount = 6
        self.lib_gui_ui.tableWidget.setColumnCount(colcount)
        row_labels = ["id", "Фамилия", "Имя", "Отчество", "Дата рождения", "Телефон"]
        self.lib_gui_ui.tableWidget.setHorizontalHeaderLabels(row_labels)

        self.buttons_show = [self.lib_gui_ui.pushButton_and_or_2, self.lib_gui_ui.pushButton_and_or_3,
                             self.lib_gui_ui.pushButton_and_or_4, self.lib_gui_ui.pushButton_and_or_5,
                             self.lib_gui_ui.pushButton_and_or_6]
        for button in self.buttons_show:
            button.show()

        self.buttons_hide = [self.lib_gui_ui.pushButton_and_or_7,
                             self.lib_gui_ui.pushButton_and_or_8, self.lib_gui_ui.pushButton_and_or_9]
        for button in self.buttons_hide:
            button.hide()

        self.textEdit_show = [self.lib_gui_ui.textEdit_1, self.lib_gui_ui.textEdit_2,
                              self.lib_gui_ui.textEdit_3, self.lib_gui_ui.textEdit_4,
                              self.lib_gui_ui.textEdit_5, self.lib_gui_ui.textEdit_6]
        for textEdit in self.textEdit_show:
            textEdit.show()

        self.textEdit_hide = [self.lib_gui_ui.textEdit_7,
                              self.lib_gui_ui.textEdit_8, self.lib_gui_ui.textEdit_9]
        for textEdit in self.textEdit_hide:
            textEdit.hide()

        self.textBrowser_show = [self.lib_gui_ui.textBrowser_1, self.lib_gui_ui.textBrowser_2,
                                 self.lib_gui_ui.textBrowser_3, self.lib_gui_ui.textBrowser_4,
                                 self.lib_gui_ui.textBrowser_5, self.lib_gui_ui.textBrowser_6]
        for textBrowser in self.textBrowser_show:
            textBrowser.show()

        self.textBrowser_hide = [self.lib_gui_ui.textBrowser_7,
                                 self.lib_gui_ui.textBrowser_8, self.lib_gui_ui.textBrowser_9]
        for textBrowser in self.textBrowser_hide:
            textBrowser.hide()

        self.textEdit_setText = [self.lib_gui_ui.textEdit_1, self.lib_gui_ui.textEdit_2,
                                 self.lib_gui_ui.textEdit_3, self.lib_gui_ui.textEdit_4,
                                 self.lib_gui_ui.textEdit_5, self.lib_gui_ui.textEdit_6]
        for textEdit in self.textEdit_setText:
            textEdit.setText("")

        self.lib_gui_ui.textBrowser_1.setText(row_labels[0])
        self.lib_gui_ui.textBrowser_2.setText(row_labels[1])
        self.lib_gui_ui.textBrowser_3.setText(row_labels[2])
        self.lib_gui_ui.textBrowser_4.setText(row_labels[3])
        self.lib_gui_ui.textBrowser_5.setText(row_labels[4])
        self.lib_gui_ui.textBrowser_5.setText(row_labels[5])

        cursor = self.conn.cursor()
        cursor.execute(f"SELECT * FROM librarian")
        bib = cursor.fetchall()

        self.lib_gui_ui.tableWidget.setRowCount(len(bib))
        for i in range(len(bib)):
            for j in range(colcount):
                self.lib_gui_ui.tableWidget.setItem(i, j, QTableWidgetItem(str(bib[i][j])))

        self.lib_gui_ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    def showLiterature(self):
        colcount = 8
        self.lib_gui_ui.tableWidget.setColumnCount(colcount)
        row_labels = ["id", "Название", "Жанр", "Автор", "Издательство", "Дата печати", "Возраст", "Стоимость"]
        self.lib_gui_ui.tableWidget.setHorizontalHeaderLabels(row_labels)

        self.buttons_show = [self.lib_gui_ui.pushButton_and_or_2, self.lib_gui_ui.pushButton_and_or_3,
                             self.lib_gui_ui.pushButton_and_or_4, self.lib_gui_ui.pushButton_and_or_5,
                             self.lib_gui_ui.pushButton_and_or_6, self.lib_gui_ui.pushButton_and_or_7,
                             self.lib_gui_ui.pushButton_and_or_8]
        for button in self.buttons_show:
            button.show()

        self.buttons_hide = [self.lib_gui_ui.pushButton_and_or_9]
        for button in self.buttons_hide:
            button.hide()

        self.textEdit_show = [self.lib_gui_ui.textEdit_1, self.lib_gui_ui.textEdit_2,
                              self.lib_gui_ui.textEdit_3, self.lib_gui_ui.textEdit_4,
                              self.lib_gui_ui.textEdit_5, self.lib_gui_ui.textEdit_6,
                              self.lib_gui_ui.textEdit_7, self.lib_gui_ui.textEdit_8,]
        for textEdit in self.textEdit_show:
            textEdit.show()

        self.textEdit_hide = [self.lib_gui_ui.textEdit_9]
        for textEdit in self.textEdit_hide:
            textEdit.hide()

        self.textBrowser_show = [self.lib_gui_ui.textBrowser_1, self.lib_gui_ui.textBrowser_2,
                                 self.lib_gui_ui.textBrowser_3, self.lib_gui_ui.textBrowser_4,
                                 self.lib_gui_ui.textBrowser_5, self.lib_gui_ui.textBrowser_6,
                                 self.lib_gui_ui.textBrowser_7, self.lib_gui_ui.textBrowser_8]
        for textBrowser in self.textBrowser_show:
            textBrowser.show()

        self.textBrowser_hide = [self.lib_gui_ui.textBrowser_9]
        for textBrowser in self.textBrowser_hide:
            textBrowser.hide()

        self.textEdit_setText = [self.lib_gui_ui.textEdit_1, self.lib_gui_ui.textEdit_2,
                                 self.lib_gui_ui.textEdit_3, self.lib_gui_ui.textEdit_4,
                                 self.lib_gui_ui.textEdit_5, self.lib_gui_ui.textEdit_6,
                                 self.lib_gui_ui.textEdit_7, self.lib_gui_ui.textEdit_8]
        for textEdit in self.textEdit_setText:
            textEdit.setText("")

        self.lib_gui_ui.textBrowser_1.setText(row_labels[0])
        self.lib_gui_ui.textBrowser_2.setText(row_labels[1])
        self.lib_gui_ui.textBrowser_3.setText(row_labels[2])
        self.lib_gui_ui.textBrowser_4.setText(row_labels[3])
        self.lib_gui_ui.textBrowser_5.setText(row_labels[4])
        self.lib_gui_ui.textBrowser_6.setText(row_labels[5])
        self.lib_gui_ui.textBrowser_7.setText(row_labels[6])
        self.lib_gui_ui.textBrowser_8.setText(row_labels[7])


        cursor = self.conn.cursor()
        cursor.execute(f"SELECT * FROM literature")
        bib = cursor.fetchall()

        self.lib_gui_ui.tableWidget.setRowCount(len(bib))
        for i in range(len(bib)):
            for j in range(colcount):
                self.lib_gui_ui.tableWidget.setItem(i, j, QTableWidgetItem(str(bib[i][j])))

        self.lib_gui_ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    def showLiterature_movement(self):
        colcount = 7
        self.lib_gui_ui.tableWidget.setColumnCount(colcount)
        row_labels = ["id", "Библиотекарь", "Читатель", "Литература", "Дата выдачи", "Дата предполагаемого возврата", "Дата фактического возврата"]
        self.lib_gui_ui.tableWidget.setHorizontalHeaderLabels(row_labels)

        self.buttons_show = [self.lib_gui_ui.pushButton_and_or_2, self.lib_gui_ui.pushButton_and_or_3,
                             self.lib_gui_ui.pushButton_and_or_4, self.lib_gui_ui.pushButton_and_or_5,
                             self.lib_gui_ui.pushButton_and_or_6, self.lib_gui_ui.pushButton_and_or_7]
        for button in self.buttons_show:
            button.show()

        self.buttons_hide = [self.lib_gui_ui.pushButton_and_or_8, self.lib_gui_ui.pushButton_and_or_9]
        for button in self.buttons_hide:
            button.hide()

        self.textEdit_show = [self.lib_gui_ui.textEdit_1, self.lib_gui_ui.textEdit_2,
                              self.lib_gui_ui.textEdit_3, self.lib_gui_ui.textEdit_4,
                              self.lib_gui_ui.textEdit_5, self.lib_gui_ui.textEdit_6,
                              self.lib_gui_ui.textEdit_7]
        for textEdit in self.textEdit_show:
            textEdit.show()

        self.textEdit_hide = [self.lib_gui_ui.textEdit_8,self.lib_gui_ui.textEdit_9]
        for textEdit in self.textEdit_hide:
            textEdit.hide()

        self.textBrowser_show = [self.lib_gui_ui.textBrowser_1, self.lib_gui_ui.textBrowser_2,
                                 self.lib_gui_ui.textBrowser_3, self.lib_gui_ui.textBrowser_4,
                                 self.lib_gui_ui.textBrowser_5, self.lib_gui_ui.textBrowser_6,
                                 self.lib_gui_ui.textBrowser_7]
        for textBrowser in self.textBrowser_show:
            textBrowser.show()

        self.textBrowser_hide = [self.lib_gui_ui.textBrowser_8, self.lib_gui_ui.textBrowser_9]
        for textBrowser in self.textBrowser_hide:
            textBrowser.hide()

        self.textEdit_setText = [self.lib_gui_ui.textEdit_1, self.lib_gui_ui.textEdit_2,
                                 self.lib_gui_ui.textEdit_3, self.lib_gui_ui.textEdit_4,
                                 self.lib_gui_ui.textEdit_5, self.lib_gui_ui.textEdit_6,
                                 self.lib_gui_ui.textEdit_7]
        for textEdit in self.textEdit_setText:
            textEdit.setText("")

        self.lib_gui_ui.textBrowser_1.setText(row_labels[0])
        self.lib_gui_ui.textBrowser_2.setText(row_labels[1])
        self.lib_gui_ui.textBrowser_3.setText(row_labels[2])
        self.lib_gui_ui.textBrowser_4.setText(row_labels[3])
        self.lib_gui_ui.textBrowser_5.setText(row_labels[4])
        self.lib_gui_ui.textBrowser_6.setText(row_labels[5])
        self.lib_gui_ui.textBrowser_7.setText(row_labels[6])



        cursor = self.conn.cursor()
        cursor.execute(f"SELECT * FROM literature_movement")
        bib = cursor.fetchall()

        self.lib_gui_ui.tableWidget.setRowCount(len(bib))
        for i in range(len(bib)):
            for j in range(colcount):
                self.lib_gui_ui.tableWidget.setItem(i, j, QTableWidgetItem(str(bib[i][j])))

        self.lib_gui_ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    def showPenalties(self):
        colCount = 7
        self.lib_gui_ui.tableWidget.setColumnCount(colCount)
        row_labels = ["id", "Читатель", "Библиотекарь", "Движение книги", "Сумма", "Основание", "Статус оплаты"]
        self.lib_gui_ui.tableWidget.setHorizontalHeaderLabels(row_labels)

        self.buttons_show = [self.lib_gui_ui.pushButton_and_or_2, self.lib_gui_ui.pushButton_and_or_3,
                             self.lib_gui_ui.pushButton_and_or_4, self.lib_gui_ui.pushButton_and_or_5,
                             self.lib_gui_ui.pushButton_and_or_6, self.lib_gui_ui.pushButton_and_or_7]
        for button in self.buttons_show:
            button.show()

        self.buttons_hide = [self.lib_gui_ui.pushButton_and_or_8, self.lib_gui_ui.pushButton_and_or_9]
        for button in self.buttons_hide:
            button.hide()

        self.textEdit_show = [self.lib_gui_ui.textEdit_1, self.lib_gui_ui.textEdit_2,
                              self.lib_gui_ui.textEdit_3, self.lib_gui_ui.textEdit_4,
                              self.lib_gui_ui.textEdit_5, self.lib_gui_ui.textEdit_6,
                              self.lib_gui_ui.textEdit_7]
        for textEdit in self.textEdit_show:
            textEdit.show()

        self.textEdit_hide = [self.lib_gui_ui.textEdit_8,self.lib_gui_ui.textEdit_9]
        for textEdit in self.textEdit_hide:
            textEdit.hide()

        self.textBrowser_show = [self.lib_gui_ui.textBrowser_1, self.lib_gui_ui.textBrowser_2,
                                 self.lib_gui_ui.textBrowser_3, self.lib_gui_ui.textBrowser_4,
                                 self.lib_gui_ui.textBrowser_5, self.lib_gui_ui.textBrowser_6,
                                 self.lib_gui_ui.textBrowser_7]
        for textBrowser in self.textBrowser_show:
            textBrowser.show()

        self.textBrowser_hide = [self.lib_gui_ui.textBrowser_8, self.lib_gui_ui.textBrowser_9]
        for textBrowser in self.textBrowser_hide:
            textBrowser.hide()

        self.textEdit_setText = [self.lib_gui_ui.textEdit_1, self.lib_gui_ui.textEdit_2,
                                 self.lib_gui_ui.textEdit_3, self.lib_gui_ui.textEdit_4,
                                 self.lib_gui_ui.textEdit_5, self.lib_gui_ui.textEdit_6,
                                 self.lib_gui_ui.textEdit_7]
        for textEdit in self.textEdit_setText:
            textEdit.setText("")

        self.lib_gui_ui.textBrowser_1.setText(row_labels[0])
        self.lib_gui_ui.textBrowser_2.setText(row_labels[1])
        self.lib_gui_ui.textBrowser_3.setText(row_labels[2])
        self.lib_gui_ui.textBrowser_4.setText(row_labels[3])
        self.lib_gui_ui.textBrowser_5.setText(row_labels[4])
        self.lib_gui_ui.textBrowser_6.setText(row_labels[5])
        self.lib_gui_ui.textBrowser_7.setText(row_labels[6])



        cursor = self.conn.cursor()
        cursor.execute(f"SELECT * FROM penalties")
        bib = cursor.fetchall()

        self.lib_gui_ui.tableWidget.setRowCount(len(bib))
        for i in range(len(bib)):
            for j in range(colCount):
                self.lib_gui_ui.tableWidget.setItem(i, j, QTableWidgetItem(str(bib[i][j])))

        self.lib_gui_ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    def showPublishing_house(self):
        colcount = 5
        self.lib_gui_ui.tableWidget.setColumnCount(colcount)
        row_labels = ["id", "Название", "Адресс", "Телефон", "Электронная почта"]
        self.lib_gui_ui.tableWidget.setHorizontalHeaderLabels(row_labels)

        self.buttons_show = [self.lib_gui_ui.pushButton_and_or_2, self.lib_gui_ui.pushButton_and_or_3,
                             self.lib_gui_ui.pushButton_and_or_4, self.lib_gui_ui.pushButton_and_or_5]
        for button in self.buttons_show:
            button.show()

        self.buttons_hide = [self.lib_gui_ui.pushButton_and_or_6, self.lib_gui_ui.pushButton_and_or_7,
                             self.lib_gui_ui.pushButton_and_or_8, self.lib_gui_ui.pushButton_and_or_9]
        for button in self.buttons_hide:
            button.hide()

        self.textEdit_show = [self.lib_gui_ui.textEdit_1, self.lib_gui_ui.textEdit_2,
                              self.lib_gui_ui.textEdit_3, self.lib_gui_ui.textEdit_4,
                              self.lib_gui_ui.textEdit_5]
        for textEdit in self.textEdit_show:
            textEdit.show()

        self.textEdit_hide = [self.lib_gui_ui.textEdit_6, self.lib_gui_ui.textEdit_7,
                              self.lib_gui_ui.textEdit_8, self.lib_gui_ui.textEdit_9]
        for textEdit in self.textEdit_hide:
            textEdit.hide()

        self.textBrowser_show = [self.lib_gui_ui.textBrowser_1, self.lib_gui_ui.textBrowser_2,
                                 self.lib_gui_ui.textBrowser_3, self.lib_gui_ui.textBrowser_4,
                                 self.lib_gui_ui.textBrowser_5]
        for textBrowser in self.textBrowser_show:
            textBrowser.show()

        self.textBrowser_hide = [self.lib_gui_ui.textBrowser_6, self.lib_gui_ui.textBrowser_7,
                                 self.lib_gui_ui.textBrowser_8, self.lib_gui_ui.textBrowser_9]
        for textBrowser in self.textBrowser_hide:
            textBrowser.hide()

        self.textEdit_setText = [self.lib_gui_ui.textEdit_1, self.lib_gui_ui.textEdit_2,
                                 self.lib_gui_ui.textEdit_3, self.lib_gui_ui.textEdit_4,
                                 self.lib_gui_ui.textEdit_5]
        for textEdit in self.textEdit_setText:
            textEdit.setText("")

        self.lib_gui_ui.textBrowser_1.setText(row_labels[0])
        self.lib_gui_ui.textBrowser_2.setText(row_labels[1])
        self.lib_gui_ui.textBrowser_3.setText(row_labels[2])
        self.lib_gui_ui.textBrowser_4.setText(row_labels[3])
        self.lib_gui_ui.textBrowser_5.setText(row_labels[4])

        cursor = self.conn.cursor()
        cursor.execute(f"SELECT * FROM publishing_house")
        bib = cursor.fetchall()

        self.lib_gui_ui.tableWidget.setRowCount(len(bib))
        for i in range(len(bib)):
            for j in range(colcount):
                self.lib_gui_ui.tableWidget.setItem(i, j, QTableWidgetItem(str(bib[i][j])))

        self.lib_gui_ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    def showReader(self):
        colcount = 9
        self.lib_gui_ui.tableWidget.setColumnCount(colcount)
        row_labels = ["id", "Фамилия", "Имя", "Отчество", "Дата рождения", "Дата регистрации", "Алресс", "Телефон", "Пасспорт"]
        self.lib_gui_ui.tableWidget.setHorizontalHeaderLabels(row_labels)

        self.buttons_show = [self.lib_gui_ui.pushButton_and_or_2, self.lib_gui_ui.pushButton_and_or_3,
                             self.lib_gui_ui.pushButton_and_or_4, self.lib_gui_ui.pushButton_and_or_5,
                             self.lib_gui_ui.pushButton_and_or_6, self.lib_gui_ui.pushButton_and_or_7,
                             self.lib_gui_ui.pushButton_and_or_8, self.lib_gui_ui.pushButton_and_or_9]
        for button in self.buttons_show:
            button.show()

        self.textEdit_show = [self.lib_gui_ui.textEdit_1, self.lib_gui_ui.textEdit_2,
                              self.lib_gui_ui.textEdit_3, self.lib_gui_ui.textEdit_4,
                              self.lib_gui_ui.textEdit_5, self.lib_gui_ui.textEdit_6,
                              self.lib_gui_ui.textEdit_7, self.lib_gui_ui.textEdit_8,
                              self.lib_gui_ui.textEdit_9]
        for textEdit in self.textEdit_show:
            textEdit.show()

        self.textBrowser_show = [self.lib_gui_ui.textBrowser_1, self.lib_gui_ui.textBrowser_2,
                                 self.lib_gui_ui.textBrowser_3, self.lib_gui_ui.textBrowser_4,
                                 self.lib_gui_ui.textBrowser_5, self.lib_gui_ui.textBrowser_6,
                                 self.lib_gui_ui.textBrowser_7, self.lib_gui_ui.textBrowser_8,
                                 self.lib_gui_ui.textBrowser_9]
        for textBrowser in self.textBrowser_show:
            textBrowser.show()


        self.textEdit_setText = [self.lib_gui_ui.textEdit_1, self.lib_gui_ui.textEdit_2,
                                 self.lib_gui_ui.textEdit_3, self.lib_gui_ui.textEdit_4,
                                 self.lib_gui_ui.textEdit_5, self.lib_gui_ui.textEdit_6,
                                 self.lib_gui_ui.textEdit_7, self.lib_gui_ui.textEdit_8,
                                 self.lib_gui_ui.textEdit_9]
        for textEdit in self.textEdit_setText:
            textEdit.setText("")

        self.lib_gui_ui.textBrowser_1.setText(row_labels[0])
        self.lib_gui_ui.textBrowser_2.setText(row_labels[1])
        self.lib_gui_ui.textBrowser_3.setText(row_labels[2])
        self.lib_gui_ui.textBrowser_4.setText(row_labels[3])
        self.lib_gui_ui.textBrowser_5.setText(row_labels[4])
        self.lib_gui_ui.textBrowser_6.setText(row_labels[5])
        self.lib_gui_ui.textBrowser_7.setText(row_labels[6])
        self.lib_gui_ui.textBrowser_8.setText(row_labels[7])
        self.lib_gui_ui.textBrowser_9.setText(row_labels[8])

        cursor = self.conn.cursor()
        cursor.execute(f"SELECT * FROM reader")
        bib = cursor.fetchall()

        self.lib_gui_ui.tableWidget.setRowCount(len(bib))
        for i in range(len(bib)):
            for j in range(colcount):
                self.lib_gui_ui.tableWidget.setItem(i, j, QTableWidgetItem(str(bib[i][j])))

        self.lib_gui_ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    def filter(self):
        try:
            cursor = self.conn.cursor()

            sql_colum_name = (f"SELECT column_name FROM information_schema.columns WHERE table_name = '" + self.table + "' ORDER BY ordinal_position;")

            cursor.execute(sql_colum_name)
            colum_name = cursor.fetchall()

            sql = (f"SELECT * FROM " + self.table + " WHERE (")

            if self.lib_gui_ui.textEdit_1.toPlainText():
                sql = sql + str(colum_name[0])[2:-3] + " = '" + str(self.lib_gui_ui.textEdit_1.toPlainText()) + "'"

            if self.lib_gui_ui.textEdit_2.toPlainText():
                if self.lib_gui_ui.textEdit_1.toPlainText():
                    sql = sql + " " + str(self.lib_gui_ui.pushButton_and_or_2.text()) + " "
                sql = sql + str(colum_name[1])[2:-3] + " = '" + str(self.lib_gui_ui.textEdit_2.toPlainText()) + "'"

            if self.lib_gui_ui.textEdit_3.toPlainText():
                if self.lib_gui_ui.textEdit_2.toPlainText():
                    sql = sql + " " + str(self.lib_gui_ui.pushButton_and_or_3.text()) + " "
                sql = sql + str(colum_name[2])[2:-3] + " = '" + str(self.lib_gui_ui.textEdit_3.toPlainText()) + "'"

            if self.lib_gui_ui.textEdit_4.toPlainText():
                if self.lib_gui_ui.textEdit_3.toPlainText():
                    sql = sql + " " + str(self.lib_gui_ui.pushButton_and_or_4.text()) + " "
                sql = sql + str(colum_name[3])[2:-3] + " = '" + str(self.lib_gui_ui.textEdit_4.toPlainText()) + "'"

            if self.lib_gui_ui.textEdit_5.toPlainText():
                if self.lib_gui_ui.textEdit_4.toPlainText():
                    sql = sql + " " + str(self.lib_gui_ui.pushButton_and_or_5.text()) + " "
                sql = sql + str(colum_name[4])[2:-3] + " = '" + str(self.lib_gui_ui.textEdit_5.toPlainText()) + "'"

            if self.lib_gui_ui.textEdit_6.toPlainText():
                if self.lib_gui_ui.textEdit_5.toPlainText():
                    sql = sql + " " + str(self.lib_gui_ui.pushButton_and_or_6.text()) + " "
                sql = sql + str(colum_name[5])[2:-3] + " = '" + str(self.lib_gui_ui.textEdit_6.toPlainText()) + "'"

            if self.lib_gui_ui.textEdit_7.toPlainText():
                if self.lib_gui_ui.textEdit_6.toPlainText():
                    sql = sql + " " + str(self.lib_gui_ui.pushButton_and_or_7.text()) + " "
                sql = sql + str(colum_name[6])[2:-3] + " = '" + str(self.lib_gui_ui.textEdit_7.toPlainText()) + "'"

            if self.lib_gui_ui.textEdit_8.toPlainText():
                if self.lib_gui_ui.textEdit_7.toPlainText():
                    sql = sql + " " + str(self.lib_gui_ui.pushButton_and_or_8.text()) + " "
                sql = sql + str(colum_name[7])[2:-3] + " = '" + str(self.lib_gui_ui.textEdit_8.toPlainText()) + "'"

            if self.lib_gui_ui.textEdit_9.toPlainText():
                if self.lib_gui_ui.textEdit_8.toPlainText():
                    sql = sql + " " + str(self.lib_gui_ui.pushButton_and_or_9.text()) + " "
                sql = sql + str(colum_name[8])[2:-3] + " = '" + str(self.lib_gui_ui.textEdit_9.toPlainText()) + "'"

            sql = sql + ");"

            cursor.execute(sql)
            filter_result = cursor.fetchall()

            self.lib_gui_ui.tableWidget.setRowCount(len(filter_result))
            for i in range(len(filter_result)):
                for j in range(self.colcount):
                    self.lib_gui_ui.tableWidget.setItem(i, j, QTableWidgetItem(str(filter_result[i][j])))
            self.lib_gui_ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)


        except(Exception, Error) as error:
            QMessageBox.warning(self, 'Ошибка!', str(error))

    def add(self):
        try:
            cursor = self.conn.cursor()
            sql = (f"INSERT INTO  " + self.table + " VALUES ('")

            if self.lib_gui_ui.textEdit_1.toPlainText():
                sql = sql + self.lib_gui_ui.textEdit_1.toPlainText()
            if self.lib_gui_ui.textEdit_2.toPlainText():
                sql = sql  + "', '" + self.lib_gui_ui.textEdit_2.toPlainText()
            if self.lib_gui_ui.textEdit_3.isVisible() and self.lib_gui_ui.textEdit_3.toPlainText():
                sql = sql  + "', '" + self.lib_gui_ui.textEdit_3.toPlainText()
            if self.lib_gui_ui.textEdit_4.isVisible() and self.lib_gui_ui.textEdit_4.toPlainText():
                sql = sql  + "', '" + self.lib_gui_ui.textEdit_4.toPlainText()
            if self.lib_gui_ui.textEdit_5.isVisible() and self.lib_gui_ui.textEdit_5.toPlainText():
                sql = sql  + "', '" + self.lib_gui_ui.textEdit_5.toPlainText()
            if self.lib_gui_ui.textEdit_6.isVisible() and self.lib_gui_ui.textEdit_6.toPlainText():
                sql = sql  + "', '" + self.lib_gui_ui.textEdit_6.toPlainText()
            if self.lib_gui_ui.textEdit_7.isVisible() and self.lib_gui_ui.textEdit_7.toPlainText():
                sql = sql  + "', '" + self.lib_gui_ui.textEdit_7.toPlainText()
            if self.lib_gui_ui.textEdit_8.isVisible() and self.lib_gui_ui.textEdit_8.toPlainText():
                sql = sql  + "', '" + self.lib_gui_ui.textEdit_8.toPlainText()
            if self.lib_gui_ui.textEdit_9.isVisible() and self.lib_gui_ui.textEdit_9.toPlainText():
                sql = sql  + "', '" + self.lib_gui_ui.textEdit_9.toPlainText()

            sql = sql + "');"

            cursor.execute(sql)
            self.conn.commit()

        except(Exception, Error) as error:
            QMessageBox.warning(self, 'Ошибка!', str(error))

    def delete(self):
        try:
            cursor = self.conn.cursor()

            sql_colum_name = (
                        f"SELECT column_name FROM information_schema.columns WHERE table_name = '" + self.table + "' ORDER BY ordinal_position;")

            cursor.execute(sql_colum_name)
            colum_name = cursor.fetchall()

            sql = (f"DELETE FROM " + self.table + " WHERE (")

            if self.lib_gui_ui.textEdit_1.toPlainText():
                sql = sql + str(colum_name[0])[2:-3] + " = '" + str(self.lib_gui_ui.textEdit_1.toPlainText()) + "'"

            if self.lib_gui_ui.textEdit_2.toPlainText():
                if self.lib_gui_ui.textEdit_1.toPlainText():
                    sql = sql + " " + str(self.lib_gui_ui.pushButton_and_or_2.text()) + " "
                sql = sql + str(colum_name[1])[2:-3] + " = '" + str(self.lib_gui_ui.textEdit_2.toPlainText()) + "'"

            if self.lib_gui_ui.textEdit_3.toPlainText():
                if self.lib_gui_ui.textEdit_2.toPlainText():
                    sql = sql + " " + str(self.lib_gui_ui.pushButton_and_or_3.text()) + " "
                sql = sql + str(colum_name[2])[2:-3] + " = '" + str(self.lib_gui_ui.textEdit_3.toPlainText()) + "'"

            if self.lib_gui_ui.textEdit_4.toPlainText():
                if self.lib_gui_ui.textEdit_3.toPlainText():
                    sql = sql + " " + str(self.lib_gui_ui.pushButton_and_or_4.text()) + " "
                sql = sql + str(colum_name[3])[2:-3] + " = '" + str(self.lib_gui_ui.textEdit_4.toPlainText()) + "'"

            if self.lib_gui_ui.textEdit_5.toPlainText():
                if self.lib_gui_ui.textEdit_4.toPlainText():
                    sql = sql + " " + str(self.lib_gui_ui.pushButton_and_or_5.text()) + " "
                sql = sql + str(colum_name[4])[2:-3] + " = '" + str(self.lib_gui_ui.textEdit_5.toPlainText()) + "'"

            if self.lib_gui_ui.textEdit_6.toPlainText():
                if self.lib_gui_ui.textEdit_5.toPlainText():
                    sql = sql + " " + str(self.lib_gui_ui.pushButton_and_or_6.text()) + " "
                sql = sql + str(colum_name[5])[2:-3] + " = '" + str(self.lib_gui_ui.textEdit_6.toPlainText()) + "'"

            if self.lib_gui_ui.textEdit_7.toPlainText():
                if self.lib_gui_ui.textEdit_6.toPlainText():
                    sql = sql + " " + str(self.lib_gui_ui.pushButton_and_or_7.text()) + " "
                sql = sql + str(colum_name[6])[2:-3] + " = '" + str(self.lib_gui_ui.textEdit_7.toPlainText()) + "'"

            if self.lib_gui_ui.textEdit_8.toPlainText():
                if self.lib_gui_ui.textEdit_7.toPlainText():
                    sql = sql + " " + str(self.lib_gui_ui.pushButton_and_or_8.text()) + " "
                sql = sql + str(colum_name[7])[2:-3] + " = '" + str(self.lib_gui_ui.textEdit_8.toPlainText()) + "'"

            if self.lib_gui_ui.textEdit_9.toPlainText():
                if self.lib_gui_ui.textEdit_8.toPlainText():
                    sql = sql + " " + str(self.lib_gui_ui.pushButton_and_or_9.text()) + " "
                sql = sql + str(colum_name[8])[2:-3] + " = '" + str(self.lib_gui_ui.textEdit_9.toPlainText()) + "'"

            sql = sql + ");"

            cursor.execute(sql)

        except(Exception, Error) as error:
            QMessageBox.warning(self, 'Ошибка!', str(error))

    def update(self):
        try:
            cursor = self.conn.cursor()

            sql_colum_name = (
                        f"SELECT column_name FROM information_schema.columns WHERE table_name = '" + self.table + "' ORDER BY ordinal_position;")

            cursor.execute(sql_colum_name)
            colum_name = cursor.fetchall()

            sql = (f"UPDATE " + self.table + " SET ")

            if self.lib_gui_ui.textEdit_1.toPlainText():
                sql = sql + str(colum_name[0])[2:-3] + " = '" + str(self.lib_gui_ui.textEdit_1.toPlainText()) + "'"

            if self.lib_gui_ui.textEdit_2.toPlainText():
                if self.lib_gui_ui.textEdit_1.toPlainText():
                    sql = sql + ", "
                sql = sql + str(colum_name[1])[2:-3] + " = '" + str(self.lib_gui_ui.textEdit_2.toPlainText()) + "'"

            if self.lib_gui_ui.textEdit_3.toPlainText():
                if self.lib_gui_ui.textEdit_2.toPlainText():
                    sql = sql + ", "
                sql = sql + str(colum_name[2])[2:-3] + " = '" + str(self.lib_gui_ui.textEdit_3.toPlainText()) + "'"

            if self.lib_gui_ui.textEdit_4.toPlainText():
                if self.lib_gui_ui.textEdit_3.toPlainText():
                    sql = sql + ", "
                sql = sql + str(colum_name[3])[2:-3] + " = '" + str(self.lib_gui_ui.textEdit_4.toPlainText()) + "'"

            if self.lib_gui_ui.textEdit_5.toPlainText():
                if self.lib_gui_ui.textEdit_4.toPlainText():
                    sql = sql + ", "
                sql = sql + str(colum_name[4])[2:-3] + " = '" + str(self.lib_gui_ui.textEdit_5.toPlainText()) + "'"

            if self.lib_gui_ui.textEdit_6.toPlainText():
                if self.lib_gui_ui.textEdit_5.toPlainText():
                    sql = sql + ", "
                sql = sql + str(colum_name[5])[2:-3] + " = '" + str(self.lib_gui_ui.textEdit_6.toPlainText()) + "'"

            if self.lib_gui_ui.textEdit_7.toPlainText():
                if self.lib_gui_ui.textEdit_6.toPlainText():
                    sql = sql + ", "
                sql = sql + str(colum_name[6])[2:-3] + " = '" + str(self.lib_gui_ui.textEdit_7.toPlainText()) + "'"

            if self.lib_gui_ui.textEdit_8.toPlainText():
                if self.lib_gui_ui.textEdit_7.toPlainText():
                    sql = sql + ", "
                sql = sql + str(colum_name[7])[2:-3] + " = '" + str(self.lib_gui_ui.textEdit_8.toPlainText()) + "'"

            if self.lib_gui_ui.textEdit_9.toPlainText():
                if self.lib_gui_ui.textEdit_8.toPlainText():
                    sql = sql + ", "
                sql = sql + str(colum_name[8])[2:-3] + " = '" + str(self.lib_gui_ui.textEdit_9.toPlainText()) + "'"

            sql = sql + " WHERE (" + str(colum_name[0])[2:-3] + " = '" + (self.lib_gui_ui.tableWidget.item(self.lib_gui_ui.tableWidget.currentRow(), 0).text()) + "');"

            cursor.execute(sql)

        except(Exception, Error) as error:
            QMessageBox.warning(self, 'Ошибка!', str(error))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
